import uuid
import enum
from sqlalchemy import String, Date, Enum, ForeignKey, Text, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin

class BloodType(str, enum.Enum):
    A_pos='A+'; A_neg='A-'; B_pos='B+'; B_neg='B-'
    AB_pos='AB+'; AB_neg='AB-'; O_pos='O+'; O_neg='O-'
    unknown='unknown'

class Patient(Base, TimestampMixin):
    __tablename__ = 'patients'
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id'), nullable=True
    )
    clinic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('clinics.id'), nullable=False
    )
    mrn: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    date_of_birth_encrypted: Mapped[str | None] = mapped_column(Text)
    gender: Mapped[str | None] = mapped_column(String(32))
    blood_type: Mapped[BloodType] = mapped_column(
        Enum(BloodType), default=BloodType.unknown
    )
    insurance_number_encrypted: Mapped[str | None] = mapped_column(Text)
    allergies: Mapped[dict | None] = mapped_column(JSON)
    no_show_count: Mapped[int] = mapped_column(Integer, default=0)