from ... import config
from httpx import AsyncClient, Response, BasicAuth
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import jwt, JWTError

oauth_scheme = OAuth2PasswordBearer(tokenUrl="")

_AUTH = BasicAuth(config.AUTH_CLIENT_ID, config.AUTH_CLIENT_SECRET)
_AUTH_HOST = config.AUTH_HOST.rstrip("/")


class ServiceException(Exception):
    pass


class CredentialsException(ServiceException):
    pass


class AuthException(ServiceException):
    pass


async def _get_token() -> str:
    async with AsyncClient(auth=_AUTH) as c:
        response = await c.post(_AUTH_HOST + "/token/service")
        if response.status_code != 200:
            raise CredentialsException()
        return response.json().get("token")


def auth(token_str=Depends(oauth_scheme)) -> str:
    try:
        decoded = jwt.decode(
            token_str, config.AUTH_JWT_PUBLIC_B64, config.AUTH_JWT_ALGO
        )
    except JWTError:
        raise HTTPException(401)

    return decoded["sub"]


class BaseService:

    host: str = None
    _token: str = None

    def __init__(self, host: str):
        self.host = host.rstrip("/")
        self._token = None

    async def _update_token(self):
        self._token = await _get_token()

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self._token}"}

    async def _request(self, method: str, uri: str, query=None, json=None, timeout=300):

        async def request():
            async with AsyncClient() as client:
                url = self.host + uri
                return await client.request(
                    method,
                    url,
                    query=query,
                    json=json,
                    headers=self.headers,
                    timeout=timeout,
                )

        response = await request()
        if response.status_code != 401:
            return response.json()

        await self._update_token()

        response: Response = await request()
        if response.status_code == 401:
            raise AuthException()

        if not response.is_success:
            raise ServiceException(response.text)

        return response.json()
