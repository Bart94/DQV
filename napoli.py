import os
import secrets
from datetime import date

x = date.today()

y = date.today()

print((y-x).days)

print(type(secrets.token_hex(32)))
