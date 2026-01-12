from pydantic import BaseModel


class DropdownResponse(BaseModel):
    id: int
    name: str
    roll_number: str = None

    class Config:
        from_attributes = True
