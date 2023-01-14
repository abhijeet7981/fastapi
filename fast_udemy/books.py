from fastapi import FastAPI
from enum import Enum
from typing import Optional

app=FastAPI()

BOOKS = {
    'book1':{'tilte':'one','author' : 'Aone'},
'book2':{'tilte':'two','author':'Atwo'},
'book3':{'tilte':'three','author':'Athree'},
'book4':{'tilte':'four','author':'Afour'},
'book5':{'tilte':'five','author':'five'}

}


class DirectionName(str,Enum):
    north='north'
    south='south'
    east='east'
    west='west'


@app.get("/")
def read_all_books(skip_book:Optional[str]=None):
    if skip_book:
        new_book=BOOKS.copy()
        del new_book[skip_book]
        return new_book
    return BOOKS



@app.get('/{book_name}')
def read_book(book_name:str):
    return BOOKS[book_name]


@app.get("/direction/{direction_name}")
def get_direction(direction_name:DirectionName):
    if direction_name== DirectionName.north:
        return {'Direction':direction_name,'sub':'Up'}
    if direction_name== DirectionName.south:
        return {'Direction':direction_name,'sub':'Down'}
    if direction_name== DirectionName.west:
        return {'Direction':direction_name,'sub':'Left'}
    if direction_name== DirectionName.east:
        return {'Direction':direction_name,'sub':'Right'}




@app.get("/books/mybook")
def read_fav_book():
    return {'book title':'my fav book'}    

@app.get('/books/{book_id}')
def read_book(book_id: int):
    return {'book_title':book_id}