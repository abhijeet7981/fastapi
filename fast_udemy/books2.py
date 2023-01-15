from fastapi import FastAPI
from pydantic import BaseModel,Field
from uuid import UUID
from typing import Optional

app=FastAPI()

class Book(BaseModel):
    
    id:UUID
    title:str=Field(min_length=1)  #for must input
    author:str=Field(min_length=1,max_length=100)
    description:Optional[str]=Field(title= 'Description of book',min_length=1,max_length=100)
    rating:int =Field(gt=-1,lt=101)   #gr=greater than lt=less than

    class Config:
        schema_extra={
            'example':{
                'id':'85236de1-0d59-4b09-b359-c6e952a7f373',
                'title':'maths',
                'author':'abhi',
                'decription':'very nice book is written',
                'rating':18
                
        }
        }


BOOKS=[]

@app.get('/')
def read_all_books(books_to_return:Optional[int]=None):
    if len(BOOKS)<1:
        create_book_no_api()

    if books_to_return and len(BOOKS)>= books_to_return>0:
        i=1
        new_books=[]
        while i<=books_to_return:
            new_books.append(BOOKS[i-1])
            i+=1
            return new_books
    return BOOKS



@app.post('/')
def create_book(book:Book):
    BOOKS.append(book)
    return book




def create_book_no_api():
    book1=Book(id='35236de1-0d59-4b09-b359-c6e952a7f373',title='title1',author='author1',description='des1',rating=60)
    book2=Book(id='45236de1-0d59-4b09-b359-c6e952a7f373',title='title2',author='author2',description='des2',rating=70)
    book3=Book(id='35236dd1-0d59-4b09-b359-c6e952a7f373',title='title3',author='author3',description='des3',rating=15)
    book4=Book(id='35236de2-0d59-4b09-b359-c6e952a7f373',title='title4',author='author4',description='des4',rating=88)
    BOOKS.append(book1)
    BOOKS.append(book2)
    BOOKS.append(book3)
    BOOKS.append(book4)
















