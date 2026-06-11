from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.ticket import Ticket, TicketPriority, TicketStatus
# Add more imports as your models grow

async def seed_demo_tickets(db: AsyncSession):
    """Seed realistic healthcare-related demo tickets"""
    
    print("🌱 Seeding demo tickets...")

    # Sample tickets - you can expand this
    tickets_data = [
        {
            "title": "Update patient registration form",
            "description": "Add insurance verification fields and consent checkbox",
            "priority": TicketPriority.HIGH,
            "status": TicketStatus.TODO,
            "story_points": 5.0,
            # column_id will be passed when calling
        },
        {
            "title": "Fix appointment double booking bug",
            "description": "Resolve conflict when two patients book same slot",
            "priority": TicketPriority.CRITICAL,
            "status": TicketStatus.IN_PROGRESS,
            "story_points": 8.0,
        },
        {
            "title": "Implement doctor availability calendar",
            "description": "Show real-time availability for doctors",
            "priority": TicketPriority.MEDIUM,
            "status": TicketStatus.REVIEW,
            "story_points": 13.0,
        },
    ]

    for data in tickets_data:
        ticket = Ticket(
            title=data["title"],
            description=data["description"],
            priority=data["priority"],
            status=data["status"],
            story_points=data["story_points"],
            column_id=...  # You will pass real column_id when calling
        )
        db.add(ticket)

    await db.commit()
    print("✅ Demo tickets seeded successfully!")