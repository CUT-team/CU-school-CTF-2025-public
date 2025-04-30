import datetime
from .base import ModelBase

class JobRead(ModelBase):
    id: str
    table_name: str
    status: str
    results: list[dict] | None
    message: str | None
    created_at: datetime.datetime
    completed_at: datetime.datetime | None