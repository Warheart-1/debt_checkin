from datetime import date
from typing import Optional, List

from sqlalchemy import String, Transaction
from sqlalchemy.orm import declarative_base, Mapped, relationship
from sqlalchemy.sql.schema import CheckConstraint, Index
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.testing.schema import mapped_column

from debt_checkin.debt_check_web.backend.models.base import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    institution: Mapped[Optional[str]] = mapped_column(String(255))
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="EUR")  # ISO 4217
    iban: Mapped[Optional[str]] = mapped_column(String(34), unique=True)
    last4: Mapped[Optional[str]] = mapped_column(String(4))
    opened_at: Mapped[Optional[date]] = mapped_column(Date)
    closed_at: Mapped[Optional[date]] = mapped_column(Date)

    # Relations
    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        # Au moins l'un des deux : IBAN ou 4 derniers chiffres
        CheckConstraint(
            "iban IS NOT NULL OR last4 IS NOT NULL",
            name="accounts_iban_or_last4_ck",
        ),
        Index("ix_accounts_currency", "currency"),
    )