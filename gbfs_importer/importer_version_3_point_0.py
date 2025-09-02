from datetime import datetime
import logging

from gbfs_importer.importer_versioned import ImporterVersioned
from models.v3Point0.station_status import StationStatus
from models.v3Point0.vehicle_status import VehicleStatus
from db_handling.session_manager import SessionManager
from db_handling.db_utility import add_record
from models.gbfs_to_dict_converter import convert_gbfs_to_dict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ImporterVersionThreePointZero(ImporterVersioned):
    """
    To import GBFS files under 3.0 format
    """

    def process_sub_file(self, file_name: str, file_url: str):
        match file_name:
            case 'station_status':
                ImporterVersionThreePointZero.process_station_status(file_url)
            case 'vehicle_status':
                ImporterVersionThreePointZero.process_vehicle_status(file_url)
            case _:
                logger.log(level=logging.INFO, msg="file type {} not implemented for imports".format(file_name))
        return

    @staticmethod
    def process_station_status(file_url: str):
        data = ImporterVersioned.read_file(file_url)
        last_updated = datetime.fromisoformat(data['last_updated'])
        if not ImporterVersioned.need_update("station_status", last_updated):
            logger.log(level=logging.INFO, msg="skipping update for {}".format("station_status"))
            return
        station_status_list = data['data']['stations']
        for el in station_status_list:
            ImporterVersionThreePointZero.add_station_status(last_updated, el)

        return

    @staticmethod
    def process_vehicle_status(file_url: str):
        data = ImporterVersioned.read_file(file_url)
        last_updated = datetime.fromisoformat(data['last_updated'])
        if not ImporterVersioned.need_update("vehicle_status", last_updated):
            logger.log(level=logging.INFO, msg="skipping update for {}".format("vehicle_status"))
            return
        vehicle_status_list = data['data']['vehicles']
        for el in vehicle_status_list:
            ImporterVersionThreePointZero.add_vehicle_status(last_updated, el)
        return

    @staticmethod
    def add_station_status(last_updated, station_status_data):
        required, optional = StationStatus.get_field_types()
        full_data = convert_gbfs_to_dict(station_status_data, required, optional)
        full_data['last_updated'] = last_updated
        new_station_status = StationStatus(**full_data)
        with SessionManager.create_session() as session:
            add_record(session, new_station_status)

    @staticmethod
    def add_vehicle_status(last_updated, vehicle_status_data):
        required, optional = VehicleStatus.get_field_types()

        full_data = convert_gbfs_to_dict(vehicle_status_data, required, optional)
        full_data['last_updated'] = last_updated
        new_vehicle_status = VehicleStatus(**full_data)
        with SessionManager.create_session() as session:
            add_record(session, new_vehicle_status)
