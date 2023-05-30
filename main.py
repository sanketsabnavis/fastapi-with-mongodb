from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()


client = MongoClient("mongodb://localhost:27017/")
db = client["library"]
collection = db['booklet']


class Book(BaseModel):
    title: str
    author: str


@app.post("/books/")
async def create_book(book: Book, book_id: int):
    # Code to create the book in the database
    # Save the book data using your database library
    collection.insert_one(book.dict())
    return {"message": "Book created successfully"}

@app.get("/books/{book_id}")
async def get_book(book_id: str):
    # Code to retrieve the book from the database
    # Fetch the book data using your database library
    item = collection.find_one({"_id": book_id})
    if item:
        return item
    raise HTTPException(status_code=404, detail='book not found')

@app.put("/books/{book_id}")
async def update_book(book_id: str, book: Book):
    # Code to update the book in the database
    # Update the book data using your database library
    item_data = {'title': book.title, 'author': book.author}
    res = collection.update_one({"_id": book_id}, {"$set": item_data})
    if res.modified_count == 1:
        return {"message": "Book updated successfully"}
    raise HTTPException(status_code=404, detail='book not found')

@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    # Code to delete the book from the database
    # Delete the book data using your database library
    res = collection.delete_one({"_id": book_id})
    if res.deleted_count == 1:
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail='book not found')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
