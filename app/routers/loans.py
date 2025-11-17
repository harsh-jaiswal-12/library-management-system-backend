from fastapi import APIRouter, Depends, HTTPException, status
from ..db import get_database
from bson import ObjectId

router = APIRouter()

def get_db():
    return get_database()


@router.post("/borrow", status_code=status.HTTP_201_CREATED)
async def borrow_book(user_id: str, book_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(user_id) or not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid id(s)")
    book = await db.books.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.get("copies", 0) <= 0:
        raise HTTPException(status_code=400, detail="No copies available")
    # decrement copies
    await db.books.update_one({"_id": ObjectId(book_id)}, {"$inc": {"copies": -1}})
    loan = {"user_id": ObjectId(user_id), "book_id": ObjectId(book_id)}
    res = await db.loans.insert_one(loan)
    out = await db.loans.find_one({"_id": res.inserted_id})
    out["_id"] = str(out["_id"])
    out["user_id"] = str(out["user_id"])
    out["book_id"] = str(out["book_id"])
    return out


@router.post("/return", status_code=status.HTTP_200_OK)
async def return_book(loan_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(loan_id):
        raise HTTPException(status_code=400, detail="Invalid loan id")
    loan = await db.loans.find_one({"_id": ObjectId(loan_id)})
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    # increment copies
    await db.books.update_one({"_id": loan["book_id"]}, {"$inc": {"copies": 1}})
    await db.loans.delete_one({"_id": ObjectId(loan_id)})
    return {"detail": "returned"}
