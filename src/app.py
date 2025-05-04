from fastapi import FastAPI

from .api.networks import router as networks_router
from .api.tokens import router as tokens_router
from .api.transaction import router as transaction_router

app = FastAPI()

app.include_router(networks_router, prefix="/networks", tags=["Networks"])
app.include_router(tokens_router, prefix="/tokens", tags=["Tokens"])
app.include_router(transaction_router, prefix="/transactions", tags=["Transactions"])
