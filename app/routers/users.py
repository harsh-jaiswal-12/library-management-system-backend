from fastapi import APIRouter, Depends, HTTPException, status
from ..models import UserCreate, UserOut
from ..db import get_database
from typing import List

router = APIRouter()

def get_db():
    return get_database()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db=Depends(get_db)):
    obj = user.dict()
    res = await db.users.insert_one(obj)
    created = await db.users.find_one({"_id": res.inserted_id})
    created["_id"] = str(created["_id"])
    return created


@router.get("/", response_model=List[UserOut])
async def list_users(db=Depends(get_db)):
    cursor = db.users.find()
    out = []
    async for u in cursor:
        u["_id"] = str(u["_id"])
        out.append(u)
    return out


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str, db=Depends(get_db)):
    from bson import ObjectId
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    u = await db.users.find_one({"_id": ObjectId(user_id)})
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    u["_id"] = str(u["_id"])
    return u
