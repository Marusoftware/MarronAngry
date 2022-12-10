from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

from fastapi.middleware.trustedhost import TrustedHostMiddleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["api.marusoftware.net", "localhost"])

from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

from starlette.middleware.sessions import SessionMiddleware
import random, string
def randomstr(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))
app.add_middleware(SessionMiddleware, secret_key=randomstr(15))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes={})

