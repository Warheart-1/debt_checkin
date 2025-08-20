from datetime import date, datetime
from decimal import Decimal

from typing import Optional, List

from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Index, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Text, Enum, DateTime, Integer, Date, Numeric, JSON
from sqlalchemy.testing.schema import mapped_column

from debt_checkin.debt_check_web.backend.models.account import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    booking_date: Mapped[Optional[date]] = mapped_column(Date, index=True)
    value_date: Mapped[Optional[date]] = mapped_column(Date)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="EUR")

    description: Mapped[Optional[str]] = mapped_column(Text)
    counterparty: Mapped[Optional[str]] = mapped_column(String(255))

    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        index=True,
    )

    # "hash" pour la déduplication (ex: SHA-256) — on évite de nommer l'attribut Python "hash"
    tx_hash: Mapped[str] = mapped_column("hash", String(128), nullable=False)

    raw_payload: Mapped[Optional[dict]] = mapped_column(JSON)
    source_import_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("import_jobs.id", ondelete="SET NULL"),
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Relations
    account: Mapped["Account"] = relationship(back_populates="transactions")
    category: Mapped[Optional["Category"]] = relationship(back_populates="transactions")
    source_import: Mapped[Optional["ImportJob"]] = relationship(
        back_populates="transactions"
    )

    __table_args__ = (
        # Empêcher les doublons sur un même compte
        UniqueConstraint("account_id", "hash", name="uq_transactions_account_hash"),
        Index("ix_transactions_account_booking", "account_id", "booking_date"),
    )