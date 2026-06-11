import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_ticket(client: AsyncClient):
    response = await client.post(
        "/api/v1/tickets",
        json={
            "title": "Test Patient Appointment",
            "description": "Test ticket",
            "column_id": "00000000-0000-0000-0000-000000000000"  # Replace with real ID later
        }
    )
    assert response.status_code in [201, 200]