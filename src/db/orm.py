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
    meta = sa.Column(psql.JSONB())
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


class OrmTransaction(Base):
    __tablename__ = "transactions"
    id = sa.Column(psql.UUID(True), default=uuid4, primary_key=True)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    network_id = sa.Column(sa.String(), sa.ForeignKey("networks.id"))
    price = sa.Column(sa.Numeric(60, 0))
    status = sa.Column(sa.String())
    txn_hash = sa.Column(sa.String())
    success = sa.Column(sa.Boolean())
    request_data = sa.Column(psql.JSONB())
    response_data = sa.Column(psql.JSONB())
