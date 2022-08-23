from typing import TypedDict


class ListUsersFilters(TypedDict):
    profiles: str
    email: str 
    id: str
    enable: str
    page_size: str
    page: str