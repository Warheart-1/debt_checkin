from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Index
from sqlalchemy.sql.sqltypes import String, Text, Enum, DateTime, Integer
from sqlalchemy.testing.schema import mapped_column

from debt_checkin.debt_check_web.backend.utils.import_status import ImportStatus
from debt_checkin.debt_check_web.backend.models.account import Base


class ImportJob(Base):
    __tablename__ = "import_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(512), nullable=False)
    source_name: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[ImportStatus] = mapped_column(
        Enum(ImportStatus, name="import_status"),
        nullable=False,
        default=ImportStatus.pending,
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=func.now())
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    rows_read: Mapped[Optional[int]] = mapped_column(Integer)
    rows_loaded: Mapped[Optional[int]] = mapped_column(Integer)
    error: Mapped[Optional[str]] = mapped_column(Text)

    # Transactions importées par ce job
    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="source_import"
    )

    __table_args__ = (Index("ix_import_jobs_status", "status"),)