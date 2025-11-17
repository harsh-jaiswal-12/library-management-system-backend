from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    copies: int = 1
    description: Optional[str] = None


class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    isbn: Optional[str]
    copies: Optional[int]
    description: Optional[str]


class BookOut(BaseModel):
    id: str = Field(..., alias="_id")
    title: str
    author: str
    isbn: Optional[str]
    copies: int
    description: Optional[str]

    class Config:
        allow_population_by_field_name = True


class UserCreate(BaseModel):
    name: str
    email: str


class UserOut(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: str

    class Config:
        allow_population_by_field_name = True
