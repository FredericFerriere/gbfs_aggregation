from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


# As per https://github.com/MobilityData/gbfs-json-schema/blob/master/v3.0/station_status.json
class StationStatus(SQLModel, table=True):
    __tablename__ = "station_status"

    station_id: str = Field(primary_key=True)
    num_vehicles_available: int
    vehicle_types_available: Optional[str]
    num_vehicles_disabled: Optional[int]
    num_docks_available: Optional[int]
    num_docks_disabled: Optional[int]
    is_installed: bool
    is_renting: bool
    is_returning: bool
    last_reported: datetime
    vehicle_docks_available: Optional[str]
    last_updated: datetime = Field(primary_key=True)  # file last update = shared between all objects from the import

    @staticmethod
    def get_field_types():
        required = {'station_id': str, 'num_vehicles_available': int,
                    'is_installed': bool, 'is_renting': bool,
                    'is_returning': bool, 'last_reported': datetime.fromisoformat}

        optional = {'vehicle_types_available': str,
                    'num_vehicles_disabled': int,
                    'num_docks_available': int,
                    'vehicle_docks_available': str,
                    'num_docks_disabled': int}
        return required, optional
