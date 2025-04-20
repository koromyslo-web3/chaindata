from fastapi import FastAPI

from .api.balances import router as balances_router
from .api.networks import router as networks_router
from .api.tokens import router as tokens_router

app = FastAPI()

app.include_router(balances_router, prefix="/balances", tags=["Balances"])
app.include_router(networks_router, prefix="/networks", tags=["Networks"])
app.include_router(tokens_router, prefix="/tokens", tags=["Tokens"])
