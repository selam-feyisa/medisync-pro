from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from uuid import UUID
from typing import List, Optional

from backend.app.models.ticket import Ticket


async def search_tickets(
    db: AsyncSession, 
    workspace_id: UUID, 
    query: str,
    limit: int = 20
) -> List[Ticket]:
    """Full-text search on tickets using PostgreSQL tsvector"""
    
    if not query or len(query.strip()) < 2:
        return []
    
    # Basic full-text search query
    stmt = select(Ticket).where(
        text("search_vector @@ plainto_tsquery(:query)")
    ).params(query=query).limit(limit)
    
    result = await db.execute(stmt)
    return result.scalars().all()