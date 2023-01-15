from fastapi import FastAPI,HTTPException,Request,status,Form,Header
from pydantic import BaseModel,Field
from uuid import UUID
from typing import Optional
from starlette.responses import JSONResponse

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

class BookNoRating(BaseModel):
    id:UUID
    title:str=Field(min_length=1)  #for must input
    author:str=Field(min_length=1,max_length=100)
    description:Optional[str]=Field(None,title= 'Description of book',min_length=1,max_length=100)

    


BOOKS=[]

@app.get('/')
def read_all_books(books_to_return:Optional[int]=None):
    if len(BOOKS)<1:
        create_book_no_api()

    if books_to_return and len(BOOKS) >= books_to_return >0:
        i=1
        new_books=[]
        while i<=books_to_return:
            new_books.append(BOOKS[i-1])
            i+=1
            return new_books
    return BOOKS


@app.post('/books/login')
def book_lofgin(username:str =Form(),password:str=Form()):
    return {'username':username, 'password':password}

@app.get('/header')
def read_header(random_header:Optional[str]=Header(None)):
    return {'random_header':random_header}




#get the boom with UUID
@app.get('/book/{book_id}/')
def read_book(book_id:UUID):
    for x in BOOKS:
        if x.id==book_id:
            return x
    raise raise_item_cannot_found()


#get the boom with UUID
@app.get('/book/rating/{book_id}/',response_model=BookNoRating)
def read_book_no_rating(book_id:UUID):
    for x in BOOKS:
        if x.id==book_id:
            return x
    raise raise_item_cannot_found()







#adding book in the DB
@app.post('/',status_code=status.HTTP_201_CREATED)
def create_book(book:Book):
    BOOKS.append(book)
    return book




   #update book with UUID
@app.put('/{book_id}/')
    
def update_book(book_id:UUID,book:Book):
    counter=0
    for x in BOOKS:
        counter+=1
        if x.id==book_id:
            BOOKS[counter-1]=book
            return BOOKS[counter-1]
    raise raise_item_cannot_found()



    

@app.delete('/{book_id}/')
def delete_book(book_id:UUID):
 counter=0
 for x in BOOKS:
     counter+=1
     if x.id==book_id:
        BOOKS.pop(counter-1)
        return f'ID : {book_id} deleted'


 raise raise_item_cannot_found()










def create_book_no_api():
    book1=Book(id='35236de1-0d59-4b09-b359-c6e952a7f373',title='title1',author='author1',description='des1',rating=60)
    book2=Book(id='45236de1-0d59-4b09-b359-c6e952a7f373',title='title2',author='author2',description='des2',rating=70)
    book3=Book(id='35236dd1-0d59-4b09-b359-c6e952a7f373',title='title3',author='author3',description='des3',rating=15)
    book4=Book(id='35236de2-0d59-4b09-b359-c6e952a7f373',title='title4',author='author4',description='des4',rating=88)
    BOOKS.append(book1)
    BOOKS.append(book2)
    BOOKS.append(book3)
    BOOKS.append(book4)



def raise_item_cannot_found():
    return HTTPException(status_code=404,detail='not found',headers={'X-header-Error':'nothing tobe seen at thr uuid'})



















