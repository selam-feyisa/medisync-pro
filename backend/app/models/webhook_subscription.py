import uuid
from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class WebhookSubscription(Base, TimestampMixin):
    """Webhook subscription model for event notifications."""
    __tablename__ = "webhook_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False
    )
    target_url: Mapped[str] = mapped_column(String(500), nullable=False)
    secret: Mapped[str] = mapped_column(String(255), nullable=False)  # HMAC secret
    subscribed_events: Mapped[str] = mapped_column(Text, nullable=False)  # JSON array of events
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relationships
    workspace = relationship("Workspace")
    deliveries = relationship("WebhookDelivery", back_populates="subscription", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<WebhookSubscription {self.id} - {self.target_url}>"
