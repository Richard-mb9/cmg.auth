from typing import TypedDict, List


class CreateUserRequest(TypedDict):
    email: str
    password: str
    profiles: List[str]
