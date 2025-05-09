from . import BaseModel
from sqlalchemy import String, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column


class LockModel(BaseModel):
    __tablename__ = "lock"

    lock_id: Mapped[str] = mapped_column(String, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    expired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
