from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models import Comment, Ticket


class CommentService:
    """Comment business logic service."""

    @staticmethod
    async def get_ticket_comments(
        db: AsyncSession, ticket_id: UUID
    ) -> list[Comment]:
        """Get all top-level comments for ticket (threaded replies excluded)."""
        stmt = (
            select(Comment)
            .where((Comment.ticket_id == ticket_id) & (Comment.parent_id.is_(None)))
            .order_by(Comment.created_at.asc())
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_comment_replies(
        db: AsyncSession, parent_id: UUID
    ) -> list[Comment]:
        """Get all replies to a comment."""
        stmt = (
            select(Comment)
            .where(Comment.parent_id == parent_id)
            .order_by(Comment.created_at.asc())
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_threaded_comments(
        db: AsyncSession, ticket_id: UUID
    ) -> list[dict]:
        """Get comments with full thread structure."""
        comments = await CommentService.get_ticket_comments(db, ticket_id)
        result = []

        for comment in comments:
            replies = await CommentService.get_comment_replies(db, comment.id)
            comment_dict = {
                "id": comment.id,
                "body": comment.body,
                "author_id": comment.author_id,
                "created_at": comment.created_at,
                "is_edited": comment.is_edited,
                "replies": [
                    {
                        "id": r.id,
                        "body": r.body,
                        "author_id": r.author_id,
                        "created_at": r.created_at,
                        "is_edited": r.is_edited,
                    }
                    for r in replies
                ],
            }
            result.append(comment_dict)

        return result
