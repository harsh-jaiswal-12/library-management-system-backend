import pytest
import asyncio
from app.crud import create_book, list_books, get_book, update_book, delete_book
from app.models import BookCreate, BookUpdate
from bson import ObjectId


class InsertOneResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id


class DeleteResult:
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count


class FakeCursor:
    def __init__(self, docs):
        self.docs = list(docs)
        self._skip = 0
        self._limit = None

    def skip(self, n):
        self._skip = n
        return self

    def limit(self, n):
        self._limit = n
        return self

    def __aiter__(self):
        async def gen():
            seq = self.docs[self._skip : (None if self._limit is None else self._skip + self._limit)]
            for d in seq:
                yield d
        return gen()


class FakeCollection:
    def __init__(self):
        self._docs = {}

    async def insert_one(self, obj):
        _id = ObjectId()
        stored = dict(obj)
        stored["_id"] = _id
        self._docs[_id] = stored
        return InsertOneResult(_id)

    async def find_one(self, q):
        _id = q.get("_id")
        return self._docs.get(_id)

    def find(self):
        return FakeCursor(list(self._docs.values()))

    async def update_one(self, q, update):
        _id = q.get("_id")
        doc = self._docs.get(_id)
        if not doc:
            return
        doc.update(update.get("$set", {}))

    async def delete_one(self, q):
        _id = q.get("_id")
        if _id in self._docs:
            del self._docs[_id]
            return DeleteResult(1)
        return DeleteResult(0)


class FakeDB:
    def __init__(self):
        self.books = FakeCollection()


@pytest.mark.asyncio
async def test_create_get_update_delete_book():
    db = FakeDB()
    book_in = BookCreate(title="The Test", author="Author A")
    created = await create_book(db, book_in)
    assert created["title"] == "The Test"
    # get
    fetched = await get_book(db, created["_id"])
    assert fetched is not None and fetched["title"] == "The Test"
    # update
    updated = await update_book(db, created["_id"], BookUpdate(title="New Title"))
    assert updated["title"] == "New Title"
    # delete
    ok = await delete_book(db, created["_id"])
    assert ok is True
    assert await get_book(db, created["_id"]) is None


@pytest.mark.asyncio
async def test_list_books():
    db = FakeDB()
    for i in range(5):
        await create_book(db, BookCreate(title=f"T{i}", author="A"))
    items = await list_books(db)
    assert isinstance(items, list)
    assert len(items) == 5
