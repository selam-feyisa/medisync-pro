from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from pydantic import BaseModel
from typing import List
from collections import deque

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Ticket, TicketDependency
from app.models.ticket_dependency import DependencyType

router = APIRouter(prefix="/tickets/{ticket_id}/dependencies", tags=["ticket-dependencies"])


class DependencyCreate(BaseModel):
    related_ticket_id: UUID
    dependency_type: str = DependencyType.blocks


def detect_circular_dependency(ticket_id: UUID, related_ticket_id: UUID, dependencies: List[TicketDependency]) -> bool:
    """Detect circular dependencies using DFS."""
    # Build adjacency list
    graph = {}
    for dep in dependencies:
        if dep.blocker_id not in graph:
            graph[dep.blocker_id] = []
        graph[dep.blocker_id].append(dep.blocked_id)
    
    # Add new edge
    if ticket_id not in graph:
        graph[ticket_id] = []
    graph[ticket_id].append(related_ticket_id)
    
    # DFS to detect cycle
    visited = set()
    rec_stack = set()
    
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        
        if node in graph:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
        
        rec_stack.remove(node)
        return False
    
    for node in graph:
        if node not in visited:
            if dfs(node):
                return True
    
    return False


@router.post("", response_model=TicketDependency, status_code=status.HTTP_201_CREATED)
async def create_dependency(
    ticket_id: UUID,
    request: DependencyCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TicketDependency:
    """Create ticket dependency with circular dependency prevention."""
    # Verify both tickets exist
    blocker = await db.get(Ticket, ticket_id)
    blocked = await db.get(Ticket, request.related_ticket_id)
    
    if not blocker or not blocked:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or both tickets not found",
        )
    
    # Get all existing dependencies for circular check
    result = await db.execute(select(TicketDependency))
    all_deps = result.scalars().all()
    
    # Check for circular dependency
    if detect_circular_dependency(ticket_id, request.related_ticket_id, all_deps):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Circular dependency detected",
        )
    
    # Check if dependency already exists
    existing = await db.execute(
        select(TicketDependency).where(
            TicketDependency.blocker_id == ticket_id,
            TicketDependency.blocked_id == request.related_ticket_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dependency already exists",
        )
    
    dependency = TicketDependency(
        blocker_id=ticket_id,
        blocked_id=request.related_ticket_id,
        dependency_type=request.dependency_type
    )
    db.add(dependency)
    await db.commit()
    await db.refresh(dependency)
    return dependency


@router.get("", response_model=List[TicketDependency])
async def list_dependencies(
    ticket_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[TicketDependency]:
    """List all dependencies for a ticket."""
    result = await db.execute(
        select(TicketDependency).where(
            TicketDependency.blocker_id == ticket_id
        )
    )
    return result.scalars().all()


@router.delete("/{dep_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dependency(
    ticket_id: UUID,
    dep_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete ticket dependency."""
    dependency = await db.get(TicketDependency, dep_id)
    if not dependency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dependency not found",
        )
    
    await db.delete(dependency)
    await db.commit()
