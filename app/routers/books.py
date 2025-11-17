from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .. import models
from .. import crud
from ..db import get_database

router = APIRouter()

def get_db():
    return get_database()


@router.post("/", response_model=models.BookOut, status_code=status.HTTP_201_CREATED)
async def create_book(book: models.BookCreate, db=Depends(get_db)):
    created = await crud.create_book(db, book)
    return created


@router.get("/", response_model=List[models.BookOut])
async def list_books(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return await crud.list_books(db, skip=skip, limit=limit)


@router.get("/{book_id}", response_model=models.BookOut)
async def get_book(book_id: str, db=Depends(get_db)):
    book = await crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=models.BookOut)
async def update_book(book_id: str, data: models.BookUpdate, db=Depends(get_db)):
    updated = await crud.update_book(db, book_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, db=Depends(get_db)):
    ok = await crud.delete_book(db, book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return None
