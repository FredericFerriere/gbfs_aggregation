from datetime import datetime, timedelta

import pandas as pd

from sqlmodel import select
from fastapi import APIRouter, HTTPException

from db_handling.session_manager import SessionManager
from models.v3Point0.station_status import StationStatus
from gbfs_importer.generic_importer import GenericImporter

v3_router = APIRouter()


@v3_router.get('/stations/{station_id}/hourly_window/num_vehicles_available')
async def num_vehicles_available_by_station_last_hour(station_id: str):
    """
    Returns the number of vehicles available for the station_id over the last hour
    :param station_id:
    :return: Format = list of dict of the form {station_id: str, status_time: datetime, num_vehicles_available: int}
    """
    if GenericImporter.version != "3.0":
        raise HTTPException(status_code=404, detail="Trying to access v3.0 endpoint but data stored in {} format"
                            .format(GenericImporter.version))

    upper_time = datetime.now()
    lower_time = upper_time - timedelta(hours=1)
    with SessionManager.create_session() as session:
        statement = select(StationStatus) .where(StationStatus.station_id == station_id
                                           ).where(StationStatus.last_updated>=lower_time
                                                   ).where(StationStatus.last_updated<=upper_time
                                                           ).order_by(StationStatus.last_updated)
        db_results = session.exec(statement)
        if not db_results:
            raise HTTPException(status_code=404, detail="no data found for station_id: {}".format(station_id))

        res = [{'station_id': el.station_id,
                'status_time': el.last_updated,
                'num_vehicles_available': el.num_vehicles_available} for el in db_results]
        return res


@v3_router.get('/stations/{station_id}/hourly_average/num_vehicles_available')
async def num_vehicles_available_by_station_hourly_average(station_id: str):
    """
    Returns the average number of vehicles available per hour for the last 24 hour
    :param station_id:
    :return: Format example= {
                              "num_vehicles_available": {
                                "2025-08-03T18:00:00": 8,
                                "2025-08-03T19:00:00": 8,
                                "2025-08-03T20:00:00": 8
                              }
                            }

    """
    if GenericImporter.version != "3.0":
        raise HTTPException(status_code=404, detail="Trying to access v3.0 endpoint but data stored in {} format"
                            .format(GenericImporter.version))

    upper_time = datetime.now()
    lower_time = upper_time - timedelta(hours=24)
    with (SessionManager.create_session() as session):
        statement = select(StationStatus.station_id,
                           StationStatus.num_vehicles_available,
                           StationStatus.last_updated
                           ).where(StationStatus.station_id == station_id
                                   ).where(StationStatus.last_updated>=lower_time
                                           ).where(StationStatus.last_updated<=upper_time)

        db_results = session.exec(statement)
        data = [{'last_updated': last_updated, 'num_vehicles_available': num_vehicles_available}
                for _, num_vehicles_available, last_updated in db_results]
        data_dict = {'last_updated': [el['last_updated'] for el in data],
                     'num_vehicles_available': [el['num_vehicles_available'] for el in data]
                     }
        df = pd.DataFrame.from_dict(data_dict)
        df['last_updated'] = df['last_updated'].apply(lambda x: datetime(x.year, x.month, x.day, x.hour))
        df_agg = df.groupby('last_updated').mean()

        return df_agg
