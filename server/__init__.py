from fastapi import APIRouter, FastAPI, Request
from fastapi.security import OAuth2PasswordBearer

def custom_generate_unique_id(route: APIRouter):
    return f"{f'{route.tags[0]}-'if len(route.tags) else ''}{route.name}"

app = FastAPI(title="Marron API", description="API of Marron", generate_unique_id_function=custom_generate_unique_id)

from fastapi.middleware.trustedhost import TrustedHostMiddleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["marron.marusoftware.net", "localhost"])

from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

from starlette.middleware.sessions import SessionMiddleware
import random, string
def randomstr(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))
app.add_middleware(SessionMiddleware, secret_key=randomstr(15))

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware,
    allow_origins=["https://marron.marusoftware.net", "http://localhost:5000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes={})

from .routes import router
app.include_router(router)

from .db import init_db, final_db
@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await final_db()