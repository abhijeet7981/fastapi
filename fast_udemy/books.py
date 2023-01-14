from fastapi import FastAPI

app=FastAPI()

BOOKS = {
    'book1':{'tilte':'one','author' : 'Aone'},
'book2':{'tilte':'two','author':'Atwo'},
'book3':{'tilte':'three','author':'Athree'},
'book4':{'tilte':'four','author':'Afour'},
'book5':{'tilte':'five','author':'five'}

}

@app.get("/")
def first_api():
    return BOOKS