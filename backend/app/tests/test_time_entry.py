import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_time_entry_start_stop_flow(client: AsyncClient):
    """Test basic timer start and stop"""
    # Start timer
    response = await client.post(
        "/api/v1/time-entries/start",
        json={"description": "Test consultation"}
    )
    assert response.status_code in [200, 201]

    # Stop timer
    stop_response = await client.post(
        "/api/v1/time-entries/stop",
        params={"description": "Completed"}
    )
    assert stop_response.status_code == 200


@pytest.mark.asyncio
async def test_manual_time_entry(client: AsyncClient):
    """Test manual time entry creation"""
    response = await client.post(
        "/api/v1/time-entries/manual",
        json={
            "started_at": "2025-06-01T09:00:00",
            "stopped_at": "2025-06-01T10:30:00",
            "description": "Manual entry test"
        }
    )
    assert response.status_code in [200, 201]