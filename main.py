from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import Info

from routes import login, users, messages, friends, notifications, uploaded_files

app = FastAPI()

app = FastAPI(
    title="Chat Abdullajon",
    version="0.1.0",
    openapi_info=Info(
        title="Abdullajon",
        version="2.1.0",
    )
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def username_password():
    return {"username": "string", "password": "password"}


app.include_router(login.login_router)
app.include_router(users.users_router)
app.include_router(messages.message_router)
app.include_router(friends.friend_router)
app.include_router(notifications.notifications_router)
app.include_router(uploaded_files.uploaded_files_router)