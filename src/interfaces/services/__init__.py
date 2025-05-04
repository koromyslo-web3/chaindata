from ... import config
from .base import auth
from .wallets import WalletService

Wallets = WalletService(config.WALLETS_HOST)

__all__ = ["auth", "Wallets"]
