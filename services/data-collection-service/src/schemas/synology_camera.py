from pydantic import BaseModel, Field, ConfigDict


class SynologyCamera(BaseModel):
    """schema for synology camera data"""

    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(...)
    name: str | None = Field(None, alias='newName')
    enabled: bool = False
    model: str = 'Unknown'
    vendor: str = 'Unknown'
    status: int | None
    resolution: str = 'Unknown'
    ip: str = Field('Unknown', alias='host')
