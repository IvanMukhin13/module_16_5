from typing import Optional
from fastapi import FastAPI, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse
import uvicorn
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()

users_db = []
tempplates = Jinja2Templates(directory='templates')


class User(BaseModel):
    id: int = 0  # Значение по умолчанию для id
    username: str
    age: Optional[int] = None  # Поле age как Optional


@app.get('/')
def get_all_users(request: Request) -> HTMLResponse:
    return tempplates.TemplateResponse('users.html', {'request': request, 'users': users_db})


@app.get(path='/user/{user_id}')
def get_message(request: Request, user_id: int) -> HTMLResponse:
    try:
        for user in users_db:
            if user.id == user_id:
                return tempplates.TemplateResponse('users.html', {'request': request, 'user': user})
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')


@app.post('/', status_code=status.HTTP_201_CREATED)
def create_user(request: Request, username: str, age: Optional[int] = None) -> HTMLResponse:
    if users_db:
        user_id = max(users_db, key=lambda u: u.id).id + 1
    else:
        user_id = 1
    users_db.append(User(id=user_id, username=username, age=age))
    return tempplates.TemplateResponse('users.html', {'request': request, 'users': users_db})


@app.put('/user/{user_id}/{username}/{age}')
def update_user(user_id: int, username: str, age: int) -> str:
    try:
        edit_user = users_db[user_id - 1]
        edit_user.username = username
        edit_user.age = age
        return 'User update.'
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')


@app.delete('/user/{user_id}')
def delete_user(user_id: int):
    try:
        for user in users_db:
            if user.id == user_id:
                users_db.remove(user)
                return f'User with {user_id} was deleted.'
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


if __name__ == '__main__':
    uvicorn.run(app='module_16_5:app', host="127.0.0.1", port=8000, reload=True)
