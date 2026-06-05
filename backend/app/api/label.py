from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Label, Workspace
from app.schemas import LabelCreate, LabelResponse, LabelUpdate

router = APIRouter(prefix="/labels", tags=["labels"])


@router.post("", response_model=LabelResponse, status_code=status.HTTP_201_CREATED)
async def create_label(
    request: LabelCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Label:
    """Create new label in workspace."""
    workspace = await db.get(Workspace, request.workspace_id)
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    label = Label(
        workspace_id=request.workspace_id,
        name=request.name,
        color=request.color,
    )
    db.add(label)
    await db.commit()
    await db.refresh(label)
    return label


@router.get("/{label_id}", response_model=LabelResponse)
async def get_label(
    label_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Label:
    """Get label by ID."""
    label = await db.get(Label, label_id)
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found",
        )
    return label


@router.patch("/{label_id}", response_model=LabelResponse)
async def update_label(
    label_id: UUID,
    request: LabelUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Label:
    """Update label."""
    label = await db.get(Label, label_id)
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found",
        )

    if request.name:
        label.name = request.name
    if request.color:
        label.color = request.color

    await db.commit()
    return label


@router.delete("/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_label(
    label_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete label."""
    label = await db.get(Label, label_id)
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found",
        )
    await db.delete(label)
    await db.commit()
