from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["library"]  # Replace with your database name
collection = db["booklet"]  # Replace with your collection name


class Book(BaseModel):
    id: str
    title: str
    author: str

@app.post("/books/")
def create_book(book: Book):
    book_data = {"id": book.id, "title": book.title, "author": book.author}
    result = collection.insert_one(book_data)
    bookid = str(result.inserted_id)
    return {"book_id": bookid}

@app.get("/books/{bookid}")
def read_book(bookid: str):
    bookid = collection.find_one({"_id": ObjectId(bookid)})
    if bookid:
        return bookid
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{bookid}")
def update_book(bookid: str, book: Book):
    book_data = {"title": book.title, "author": book.author}
    result = collection.update_one({"_id": ObjectId(bookid)}, {"$set": book_data})
    if result.modified_count == 1:
        return {"message": "Book updated successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{bookid}")
def delete_book(book_id: str):
    result = collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 1:
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

import uvicorn
uvicorn.run(app, host="localhost", port=8000)
