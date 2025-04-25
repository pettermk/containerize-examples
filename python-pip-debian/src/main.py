from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager
import os

os.environ['TESTCONTAINERS_RYUK_DISABLED'] = "true"
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


class TodoBase(SQLModel):
    title: str = Field(index=True)
    description: str
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class TodoCreate(TodoBase):
    pass

DATABASE_URL = os.getenv('DATABASE_URL')
postgres = None
if DATABASE_URL == None :
    from testcontainers.postgres import PostgresContainer
    postgres = PostgresContainer("postgres:16", driver="psycopg", port=5432)
    postgres.start()
    DATABASE_URL = postgres.get_connection_url() # "postgresql+psycopg://postgres:12345@localhost:5432/todos")

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager 
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield
    if postgres:
        postgres.stop()


app = FastAPI(lifespan=lifespan)


@app.post("/todos/", response_model=Todo)
def create_todo(todo: TodoCreate, session: Session = Depends(get_session)):
    db_todo = Todo(**todo.__dict__)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoCreate, session: Session = Depends(get_session)):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.__dict__.items():
        setattr(db_todo, key, value)
    db_todo.updated_at = datetime.now()
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"ok": True}


@app.get("/todos/", response_model=list[Todo])
def read_todos(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
    return todos

