from web3.auto import w3


def exclude_none_from_kwargs(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


def to_checksum(address: str):
    return w3.to_checksum_address(address)
