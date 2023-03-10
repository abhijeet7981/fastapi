from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import SeccisonLocal,engine
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import datetime,timedelta
from jose import jwt,JWTError





SECRET_Key='x4dc4gKLKbPDJgyzIHLXaPRLGfRKdtw9'
ALGORITHM = 'HS256'

class Create_user(BaseModel):
    username: str
    email:Optional[str]
    first_name:str
    last_name:str
    password: str

bcrypy_contex= CryptContext(schemes=['bcrypt'], deprecated='auto')

models.base.metadata.create_all(bind=engine)

oauth2_bearer= OAuth2PasswordBearer(tokenUrl='token')

app = FastAPI()

def get_password_hashed(password):
    return bcrypy_contex.hash(password)

def verify_password(plain_password,hashed_password):
    return bcrypy_contex.verify(plain_password,hashed_password)

def auth_user(username:str,password:str,db):
    user=db.query(models.Users).filter(models.Users.username==username).first()
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user

def create_access_token(username:str,user_id:int,expires_delta:Optional[timedelta]= None):
    encode = {
      'sub': username,'id':user_id
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({'exp':expire})
    return jwt.encode(encode,SECRET_Key,algorithm=ALGORITHM)

def get_current_user(token:str=Depends(oauth2_bearer)):
    try:
        payload=jwt.decode(token,SECRET_Key,algorithms=[ALGORITHM])
        username:str=payload['sub']
        user_id:int=payload['id']
        if username is None or user_id is None:
            raise HTTPException(status_code=404,detail='Nor found')
        return {'username':username,'user_id':user_id}
    except JWTError:
        raise get_user_exceptions()



def get_db():
    try:
        db=SeccisonLocal()
        yield db
    finally:
        db.close()

@app.post('/create/user')
def create_new_user(create_user:Create_user,db:Session=Depends(get_db)):

    create_user_model = models.Users()
    create_user_model.email=create_user.email
    create_user_model.first_name=create_user.first_name
    create_user_model.last_name=create_user.last_name
    create_user_model.username=create_user.username
    hashed_password=get_password_hashed(create_user.password)

    create_user_model.hashed_password=hashed_password
    create_user_model.is_active=True
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)

@app.post('/token')
def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
                            
        user=auth_user(form_data.username,form_data.password,db)
        if not user:
            raise token_exception()
        token_expires=timedelta(minutes=20)
        token = create_access_token(user.username,user.id,expires_delta=token_expires)
        return {'token': token}

#exceptions
def get_user_exceptions():
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,details='could not validate credentials',headers={'WWW-Authenticate':"Bearer"})
    return credentials_exception

def token_exception():
    token_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,details='Incoreect username or password',headers={'WWW-Authenticate':"Bearer"})
    return token_exception
                            
                            
    