from typing import TypedDict


class AuthRequest(TypedDict):
    email: str
    password: str
