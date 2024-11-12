from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.links import router as linksRouter
from routes.users import router as usersRouter
from routes.auth import router as authRouter
from database import create_db_and_tables


app = FastAPI(title="Devlinks v1.4")


origins = [
    'http://localhost:5173'
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
def on_startup():
    create_db_and_tables()

app.include_router(authRouter)
app.include_router(usersRouter)
app.include_router(linksRouter)

@app.get('/')
def get_homepage():
    return {'page': 'homepage'}

