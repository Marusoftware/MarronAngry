import aiosendgrid
from .config import Settings

config=Settings()

with aiosendgrid.AsyncSendGridClient(api_key="") as sendgrid:
    pass