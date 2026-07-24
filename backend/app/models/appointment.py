import uuid
import enum
from sqlalchemy import String, Enum, ForeignKey, Text, Integer, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, TimestampMixin


class AppointmentStatus(str, enum.Enum):
    scheduled = 'scheduled'
    confirmed = 'confirmed'
    checked_in = 'checked_in'
    in_progress = 'in_progress'
    completed = 'completed'
    cancelled = 'cancelled'
    no_show = 'no_show'


class AppointmentType(str, enum.Enum):
    in_person = 'in_person'
    telemedicine = 'telemedicine'


class Appointment(Base, TimestampMixin):
    __tablename__ = 'appointments'

    clinic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('workspaces.id'),
        nullable=False
    )

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('patients.id'),
        nullable=False
    )

    doctor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=False
    )

    scheduled_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)

    duration_minutes: Mapped[int] = mapped_column(Integer, default=30)

    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(AppointmentStatus),
        default=AppointmentStatus.scheduled,
        nullable=False
    )

    appointment_type: Mapped[AppointmentType] = mapped_column(
        Enum(AppointmentType),
        default=AppointmentType.in_person,
        nullable=False
    )

    chief_complaint: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)

    is_emergency: Mapped[bool] = mapped_column(Boolean, default=False)