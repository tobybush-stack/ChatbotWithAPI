from pydantic import BaseModel

class Provider(BaseModel):
    id: int
    name: str
    status: str = "Idle"
    location: str | None = None

providers_table = [
    Provider(id=1, name="General Hospital"),
    Provider(id=2, name="North Clinic"),
    Provider(id=3, name="South Clinic"),
    Provider(id=4, name="Saint James Hospital")
]
