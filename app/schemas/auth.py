from pydantic import BaseModel
from typing import Optional
from enum import Enum

class UserType(str, Enum):
    OWNER = "owner"
    CLINIC = "clinic"

class AuthenticatedUser(BaseModel):
    id: str
    email: str
    userType: UserType 