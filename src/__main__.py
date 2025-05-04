import uvicorn

from .config import DEBUG

if __name__ == "__main__":
    uvicorn.run("src.app:app", reload=DEBUG, port=8000, host="0.0.0.0")
