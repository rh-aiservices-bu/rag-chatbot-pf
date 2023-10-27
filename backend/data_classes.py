from pydantic import BaseModel

# Data classes
class DestinationEntry(BaseModel):
    """ Additional destination entry """
    kind: str = ""
    coordinates: tuple[float,float] = None
    uuid: str = ""

    class Config:
        """ Example """
        json_schema_extra = {
            "example": {
                "kind": "wheat",
                "coordinates": (10.0,22.1),
                "uuid": "c303282d-f2e6-46ca-a04a-35d3d873712d"
            }
        }