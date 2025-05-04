import logging
import os


def _env2bool(key, default=None):
    val = os.getenv(key, default)
    r_val = {
        "true": True,
        "1": True,
        "false": False,
        "0": False,
    }.get(val.lower())
    if r_val is None:
        raise ValueError(f"Cannot parse boolean variable {key} (value: {val})")
    return r_val


def _env2int(key, default=None):
    val = os.getenv(key, default)
    try:
        return int(val)
    except Exception:
        raise ValueError(f"Cannot parse integer variable {key} (value: {val})")


DEBUG: bool = _env2bool("DEBUG", "true")

DB_HOST: str = os.getenv("DB_HOST")
DB_NAME: str = os.getenv("DB_NAME")
DB_USERNAME: str = os.getenv("DB_USERNAME")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_URL: str = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

AUTH_JWT_PUBLIC_B64: str = os.getenv("AUTH_JWT_PUBLIC_B64")
AUTH_JWT_ALGO: str = os.getenv("AUTH_JWT_ALGO", "HS256")
AUTH_HOST: str = os.getenv("AUTH_HOST").rstrip("/")
AUTH_CLIENT_ID: str = os.getenv("AUTH_CLIENT_ID", "HS256")
AUTH_CLIENT_SECRET: str = os.getenv("AUTH_CLIENT_SECRET", "HS256")

WALLETS_API_ENDPOINT: str = os.getenv("WALLETS_API_ENDPOINT", "HS256").rstrip("/")


logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
