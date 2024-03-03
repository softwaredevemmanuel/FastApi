from typing import List, Optional, Generic, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from datetime import datetime


T = TypeVar('T')


class ProfileSchema(BaseModel):
    id: Optional[int] = None
    reference: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    other_name: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[str] = None
    organization_id: Optional[int] = None
    email: Optional[str] = None
    phone_number: Optional[int] = None
    display_image: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes=True

class RequestProfile(BaseModel):
    profile_parameter: ProfileSchema = Field(...)

class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result:Optional[T]


class EmailCheckRequest(BaseModel):
    email: str


# This section does not have any optional values
class UserSchema(BaseModel):
    id: Optional[int] = None
    email: str
    password: str
    profile_id: Optional[int] = None
    login_status: bool = False  # Default value set to False
    status: Optional[str] = "pending"  
    enabled: Optional[bool] = False  

    class Config:
        orm_mode = True
        from_attributes=True


class RequestUser(BaseModel):
    user_parameter: UserSchema = Field(...)
