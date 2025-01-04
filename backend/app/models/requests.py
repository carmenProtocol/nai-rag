from typing import List
from pydantic import BaseModel


class UserQuery(BaseModel):
    query: str
    urls: List[str]


class UserQueryWithContext(BaseModel):
    query: str
    urls: List[str]
    previous_summary: str 