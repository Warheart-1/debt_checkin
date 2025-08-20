from typing import Optional, List

from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.schema import ForeignKey, Index
from sqlalchemy.sql.sqltypes import String, Text
from sqlalchemy.testing.schema import mapped_column

from debt_checkin.debt_check_web.backend.models.account import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    # Motif utilisé pour auto-catégoriser (regex, LIKE, etc. selon votre logique applicative)
    rule_pattern: Mapped[Optional[str]] = mapped_column(Text)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL")
    )

    # Relations hiérarchiques
    parent: Mapped[Optional["Category"]] = relationship(
        back_populates="children",
        remote_side=lambda: [Category.id],
    )
    children: Mapped[List["Category"]] = relationship(
        back_populates="parent",
        cascade="all",
    )

    # Transactions liées
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="category")

    __table_args__ = (Index("ix_categories_parent", "parent_id"),)