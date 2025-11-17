from typing import List, Optional
from bson import ObjectId
from .models import BookCreate, BookUpdate

async def create_book(db, book: BookCreate) -> dict:
    obj = book.dict()
    result = await db.books.insert_one(obj)
    created = await db.books.find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return created

async def list_books(db, skip: int = 0, limit: int = 100) -> List[dict]:
    cursor = db.books.find().skip(skip).limit(limit)
    items = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        items.append(doc)
    return items

async def get_book(db, id: str) -> Optional[dict]:
    if not ObjectId.is_valid(id):
        return None
    doc = await db.books.find_one({"_id": ObjectId(id)})
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

async def update_book(db, id: str, data: BookUpdate) -> Optional[dict]:
    if not ObjectId.is_valid(id):
        return None
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if not update_data:
        return await get_book(db, id)
    await db.books.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    return await get_book(db, id)

async def delete_book(db, id: str) -> bool:
    if not ObjectId.is_valid(id):
        return False
    res = await db.books.delete_one({"_id": ObjectId(id)})
    return res.deleted_count == 1
