from typing import List, TypedDict


class ListUsersResponse(TypedDict):
    id: int
    email: str
    enable: bool
    profiles: List[str]
