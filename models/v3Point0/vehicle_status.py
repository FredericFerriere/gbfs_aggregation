from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


# As per https://github.com/MobilityData/gbfs-json-schema/blob/master/v3.0/vehicle_status.json
class VehicleStatus(SQLModel, table=True):
    __tablename__ = "vehicle_status"

    vehicle_id: str = Field(primary_key=True)
    lat: Optional[float]
    lon: Optional[float]
    is_reserved: bool
    is_disabled: bool
    rental_uris: Optional[str]
    vehicle_type_id: Optional[str]
    last_reported: Optional[datetime]
    current_range_meters: Optional[int]
    current_fuel_percent: Optional[float]
    station_id: Optional[str]
    home_station_id: Optional[str]
    pricing_plan_id: Optional[str]
    vehicle_equipment: Optional[str]
    available_until: Optional[datetime]
    last_updated: datetime = Field(primary_key=True)  # file last update = shared between all objects from the import

    @staticmethod
    def get_field_types():
        required = {'vehicle_id': str, 'is_reserved': bool, 'is_disabled': bool}

        optional = {'lat': float, 'lon': float, 'rental_uris': str, 'vehicle_type_id': str, 'station_id': str,
                    'home_station_id': str, 'pricing_plan_id': str, 'vehicle_equipment': str,
                    'current_range_meters': int, 'current_fuel_percent': float,
                    'last_reported': datetime.fromisoformat, 'available_until': datetime.fromisoformat}
        return required, optional
