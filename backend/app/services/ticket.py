from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models import Ticket, TicketAssignee, TicketLabel, User, Label


class TicketService:
    """Ticket business logic service."""

    @staticmethod
    async def assign_user_to_ticket(
        db: AsyncSession, ticket_id: UUID, user_id: UUID
    ) -> TicketAssignee:
        """Assign user to ticket."""
        assignment = TicketAssignee(
            ticket_id=ticket_id,
            user_id=user_id,
        )
        db.add(assignment)
        await db.flush()
        return assignment

    @staticmethod
    async def remove_user_from_ticket(
        db: AsyncSession, ticket_id: UUID, user_id: UUID
    ) -> None:
        """Remove user assignment from ticket."""
        stmt = select(TicketAssignee).where(
            (TicketAssignee.ticket_id == ticket_id)
            & (TicketAssignee.user_id == user_id)
        )
        result = await db.execute(stmt)
        assignment = result.scalars().first()
        if assignment:
            await db.delete(assignment)

    @staticmethod
    async def add_label_to_ticket(
        db: AsyncSession, ticket_id: UUID, label_id: UUID
    ) -> TicketLabel:
        """Add label to ticket."""
        label_assignment = TicketLabel(
            ticket_id=ticket_id,
            label_id=label_id,
        )
        db.add(label_assignment)
        await db.flush()
        return label_assignment

    @staticmethod
    async def get_ticket_assignees(
        db: AsyncSession, ticket_id: UUID
    ) -> list[User]:
        """Get all users assigned to ticket."""
        stmt = (
            select(User)
            .join(TicketAssignee)
            .where(TicketAssignee.ticket_id == ticket_id)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_ticket_labels(db: AsyncSession, ticket_id: UUID) -> list[Label]:
        """Get all labels on ticket."""
        stmt = (
            select(Label)
            .join(TicketLabel)
            .where(TicketLabel.ticket_id == ticket_id)
        )
        result = await db.execute(stmt)
        return result.scalars().all()
