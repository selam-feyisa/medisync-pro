import uuid
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class OAuthClient(Base, TimestampMixin):
    """OAuth client model for client credentials grant."""
    __tablename__ = "oauth_clients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    client_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    client_secret_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    scopes: Mapped[str | None] = mapped_column(String(500), nullable=True)  # JSON array of scopes

    def __repr__(self):
        return f"<OAuthClient {self.client_id} - {self.name}>"
