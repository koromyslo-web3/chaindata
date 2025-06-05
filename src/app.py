from fastapi import FastAPI

from .api.networks import router as networks_router
from .api.eth import router as eth_router

app = FastAPI()

app.include_router(networks_router, prefix="/networks", tags=["Networks"])
app.include_router(eth_router, prefix="/eth", tags=["Ethereum proxy"])
