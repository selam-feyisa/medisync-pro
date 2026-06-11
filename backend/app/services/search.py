from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from uuid import UUID
from typing import List, Optional

from backend.app.models.ticket import Ticket
from backend.app.core.exceptions import NotFoundException


async def search_tickets(
    db: AsyncSession, 
    workspace_id: UUID, 
    query: str,
    limit: int = 20
) -> List[Ticket]:
    """Full-text search on tickets within a specific workspace"""
    
    if not query or len(query.strip()) < 2:
        return []
    
    # Search only tickets belonging to the workspace (via project -> board -> column)
    stmt = select(Ticket).where(
        text("""
            search_vector @@ plainto_tsquery(:query) 
            AND column_id IN (
                SELECT c.id FROM columns c 
                JOIN boards b ON c.board_id = b.id 
                JOIN projects p ON b.project_id = p.id 
                WHERE p.workspace_id = :workspace_id
            )
        """)
    ).params(query=query, workspace_id=workspace_id).limit(limit)
    
    result = await db.execute(stmt)
    return result.scalars().all()