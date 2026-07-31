import uuid
import enum
from sqlalchemy import String, Integer, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, TimestampMixin


class PlanType(str, enum.Enum):
    free = "free"
    basic = "basic"
    pro = "pro"
    enterprise = "enterprise"


class Plan(Base, TimestampMixin):
    """Subscription plan model."""
    __tablename__ = "plans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    plan_type: Mapped[PlanType] = mapped_column(String(50), nullable=False)
    
    # Pricing
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    interval: Mapped[str] = mapped_column(String(20), nullable=False, default="monthly")  # monthly, yearly
    
    # Limits
    seat_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    ai_tokens_limit: Mapped[int] = mapped_column(Integer, nullable=True)  # Optional AI token limit
    
    # Stripe integration
    stripe_price_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    # Features
    features: Mapped[str | None] = mapped_column(String(1000), nullable=True)  # JSON string of features
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)  # Visible to users

    def __repr__(self):
        return f"<Plan {self.name} - {self.price} {self.currency}/{self.interval}>"
