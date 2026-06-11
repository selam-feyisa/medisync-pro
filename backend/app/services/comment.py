from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List
import re

from backend.app.models.comment import Comment
from backend.app.schemas.comment import CommentCreate
from backend.app.core.exceptions import NotFoundException


async def create_comment(db: AsyncSession, ticket_id: UUID, data: CommentCreate, author_id: UUID) -> Comment:
    comment = Comment(
        ticket_id=ticket_id,
        author_id=author_id,
        body=data.body,
        parent_id=data.parent_id
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    
    # Parse mentions (will be used later for notifications)
    mentions = parse_mentions(data.body)
    if mentions:
        print(f"👤 Mentioned users: {mentions}")  # TODO: Create notifications later
    
    return comment


def parse_mentions(body: str) -> List[str]:
    """Extract @username mentions from comment body"""
    if not body:
        return []
    # Simple regex to find @ followed by word characters
    matches = re.findall(r'@(\w+)', body)
    return list(set(matches))  # Remove duplicates


async def get_ticket_comments(db: AsyncSession, ticket_id: UUID) -> List[Comment]:
    result = await db.execute(
        select(Comment)
        .where(Comment.ticket_id == ticket_id)
        .order_by(Comment.created_at)
    )
    return result.scalars().all()