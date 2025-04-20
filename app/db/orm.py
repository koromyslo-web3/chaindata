from uuid import uuid4

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OrmNetwork(Base):
    __tablename__ = "networks"
    id = sa.Column(sa.String(), primary_key=True)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    name = sa.Column(sa.String(), nullable=False)
    type = sa.Column(sa.String(), nullable=False)
    native_symbol = sa.Column(sa.String(), nullable=False)
    endpoints = sa.Column(psql.JSONB(), nullable=False)
    is_active = sa.Column(sa.Boolean(), nullable=False)


class OrmToken(Base):
    __tablename__ = "tokens"
    id = sa.Column(psql.UUID(True), default=uuid4, primary_key=True)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    symbol = sa.Column(sa.String(), index=True)
    network_id = sa.Column(sa.String(), sa.ForeignKey("networks.id"), index=True)
    decimals = sa.Column(sa.SmallInteger())
    contract = sa.Column(sa.String(), index=True)

    __tableargs__ = (
        sa.UniqueConstraint("network_id", "contract", name="uq_network_contract"),
    )


class OrmBalance(Base):
    __tablename__ = "balances"
    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    address = sa.Column(sa.String(), index=True)
    token_id = sa.Column(psql.UUID(True), sa.ForeignKey("tokens.id"), index=True)
    amount = sa.Column(sa.Numeric(60, 0))
    last_synced_at = sa.Column(sa.DateTime())

    __tableargs__ = (
        sa.UniqueConstraint("wallet", "token_id", name="uq_wallet_token_id"),
    )
