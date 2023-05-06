import secrets
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from ...models.db import User as UserDB, Token as TokenDB, TokenType, Organization as OrganizationDB, OrganizationMember, Project as ProjectDB
from ...models.read.user import User

config = Config('.env')  # read config from .env file
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)
class test:
    async def authorize_redirect(self, *args, **options):
        return str(config.get("GOOGLE_CLIENT_SECRET"))
oauth.test=test()
    
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

router=APIRouter()

@router.get("/{service}")
async def sso_setup(request: Request, service:str):
    redirect_uri = str(config.get("SSO_REDIRECT")).replace("{service}", service)#request.url_for('auth_via_google')
    return await getattr(oauth, service).authorize_redirect(request, redirect_uri)

@router.get("/{service}/callback")
async def sso_callback(request: Request, service:str):
    token = await getattr(oauth, service).authorize_access_token(request)
    sso_user=token["userinfo"]
    user, res=await UserDB.get_or_create(name=sso_user["name"], email=sso_user["email"])
    if res:
        org=await OrganizationDB.create(name=user.name, description=f"{user.name}'s Organization")
        await OrganizationMember.create(user=user, is_admin=True, organization=org)
        await ProjectDB.create(name=user.name, description=f"{user.name}'s Profile", organization=org)
        user.fullname=user.name
        await user.save()
    token=await TokenDB.create(token=secrets.token_hex(32), token_type=TokenType.bearer, user=user)
    if "users" not in request.session:
        request.session["users"]=[]
    request.session["users"].append({"name":user.name, "id":str(user.id), "token":token.token})
    return RedirectResponse("/")