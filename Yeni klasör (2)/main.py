from fastapi import FastAPI, HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session

app= FastAPI()

models.Base.metadata.create_all(bind=engine)


class PostBase(BaseModel):
    title:str
    content:str
    employee_id:int

class EmployeeBase(BaseModel):
  
  
   username:str
   mail: str



def get_db():
    db=SessionLocal()
    try:
        yield db
        
    finally:
        db.close()    


db_dependency = Annotated[Session, Depends(get_db)]   

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def creat_post(post: PostBase , db:db_dependency):
    db_post=models.Post(**post.dict())
    db.add(db_post)
    db.commit()

@app.post("/employees/", status_code=status.HTTP_201_CREATED)
async def creat_employee(employee:EmployeeBase, db:db_dependency):
    db_employee=models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()


@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id:int , db:db_dependency):
    post= db.query(models.Post).filter(models.Post.id==post_id).first()
    if post is None :
        raise HTTPException(status_code=404, detail='post was not found')
    return post

@app.get("/employees/{employee_id}", status_code=status.HTTP_200_OK)
async def read_employee(employee_id:int , db:db_dependency):
    employee= db.query(models.Employee).filter(models.Employee.id==employee_id).first()
    if employee is None :
        raise HTTPException(status_code=404, detail='User not found')
    return employee


@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db:db_dependency):
    db_post=db.query(models.Post).filter(models.Post.id==post_id).first()
    if db_post is None :
     raise HTTPException(status_code=404, detail='Post was not found')
    db.delete(db_post)
    db.commit()

@app.delete("/employees/{employee_id}", status_code=status.HTTP_200_OK)
async def delete_employee(employee_id: int, db:db_dependency):
    db_employee=db.query(models.Employee).filter(models.Employee.id==employee_id).first()
    if db_employee is None :
     raise HTTPException(status_code=404, detail='Employee was not found')
    db.delete(db_employee)
    db.commit()



