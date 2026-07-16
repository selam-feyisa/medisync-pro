import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from app.models import User, Notification
from app.models.notification import NotificationType


@pytest.mark.asyncio
async def test_list_notifications(db: AsyncSession, client: AsyncClient):
    """Test listing notifications for a user."""
    # Create test user
    user = User(email="test@example.com", hashed_password="hash", full_name="Test User")
    db.add(user)
    await db.flush()
    
    # Create notifications
    notif1 = Notification(
        user_id=user.id,
        notification_type=NotificationType.ticket_assigned,
        title="Ticket Assigned",
        message="You have been assigned to a ticket",
        is_read=False
    )
    notif2 = Notification(
        user_id=user.id,
        notification_type=NotificationType.ticket_mentioned,
        title="Mentioned",
        message="You were mentioned in a comment",
        is_read=True
    )
    db.add_all([notif1, notif2])
    await db.commit()
    
    response = await client.get("/api/v1/notifications")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_list_unread_only(db: AsyncSession, client: AsyncClient):
    """Test listing only unread notifications."""
    # Create test user
    user = User(email="test@example.com", hashed_password="hash", full_name="Test User")
    db.add(user)
    await db.flush()
    
    # Create notifications
    notif1 = Notification(
        user_id=user.id,
        notification_type=NotificationType.ticket_assigned,
        title="Ticket Assigned",
        message="You have been assigned to a ticket",
        is_read=False
    )
    notif2 = Notification(
        user_id=user.id,
        notification_type=NotificationType.ticket_mentioned,
        title="Mentioned",
        message="You were mentioned in a comment",
        is_read=True
    )
    db.add_all([notif1, notif2])
    await db.commit()
    
    response = await client.get("/api/v1/notifications?unread_only=true")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["is_read"] == False


@pytest.mark.asyncio
async def test_mark_as_read(db: AsyncSession, client: AsyncClient):
    """Test marking a notification as read."""
    # Create test user
    user = User(email="test@example.com", hashed_password="hash", full_name="Test User")
    db.add(user)
    await db.flush()
    
    notification = Notification(
        user_id=user.id,
        notification_type=NotificationType.ticket_assigned,
        title="Ticket Assigned",
        message="You have been assigned to a ticket",
        is_read=False
    )
    db.add(notification)
    await db.commit()
    
    response = await client.patch(f"/api/v1/notifications/{notification.id}/read")
    
    assert response.status_code == 200
    data = response.json()
    assert data["is_read"] == True


@pytest.mark.asyncio
async def test_mark_all_as_read(db: AsyncSession, client: AsyncClient):
    """Test marking all notifications as read."""
    # Create test user
    user = User(email="test@example.com", hashed_password="hash", full_name="Test User")
    db.add(user)
    await db.flush()
    
    # Create unread notifications
    notif1 = Notification(
        user_id=user.id,
        notification_type=NotificationType.ticket_assigned,
        title="Ticket Assigned",
        message="You have been assigned to a ticket",
        is_read=False
    )
    notif2 = Notification(
        user_id=user.id,
        notification_type=NotificationType.ticket_mentioned,
        title="Mentioned",
        message="You were mentioned in a comment",
        is_read=False
    )
    db.add_all([notif1, notif2])
    await db.commit()
    
    response = await client.patch("/api/v1/notifications/read-all")
    
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_unread_count(db: AsyncSession, client: AsyncClient):
    """Test getting unread notification count."""
    # Create test user
    user = User(email="test@example.com", hashed_password="hash", full_name="Test User")
    db.add(user)
    await db.flush()
    
    # Create notifications
    notif1 = Notification(
        user_id=user.id,
        notification_type=NotificationType.ticket_assigned,
        title="Ticket Assigned",
        message="You have been assigned to a ticket",
        is_read=False
    )
    notif2 = Notification(
        user_id=user.id,
        notification_type=NotificationType.ticket_mentioned,
        title="Mentioned",
        message="You were mentioned in a comment",
        is_read=True
    )
    notif3 = Notification(
        user_id=user.id,
        notification_type=NotificationType.ticket_updated,
        title="Updated",
        message="Ticket was updated",
        is_read=False
    )
    db.add_all([notif1, notif2, notif3])
    await db.commit()
    
    response = await client.get("/api/v1/notifications/unread/count")
    
    assert response.status_code == 200
    data = response.json()
    assert data["unread_count"] == 2


@pytest.mark.asyncio
async def test_delete_notification(db: AsyncSession, client: AsyncClient):
    """Test deleting a notification."""
    # Create test user
    user = User(email="test@example.com", hashed_password="hash", full_name="Test User")
    db.add(user)
    await db.flush()
    
    notification = Notification(
        user_id=user.id,
        notification_type=NotificationType.ticket_assigned,
        title="Ticket Assigned",
        message="You have been assigned to a ticket",
        is_read=False
    )
    db.add(notification)
    await db.commit()
    
    response = await client.delete(f"/api/v1/notifications/{notification.id}")
    
    assert response.status_code == 204
