import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_start_stop_timer(client: AsyncClient, test_user):
    """Test basic timer start and stop flow"""
    # Start timer
    start_response = await client.post(
        "/api/v1/time-entries/start",
        json={"description": "Test patient consultation"}
    )
    assert start_response.status_code in [200, 201]

    # Stop timer
    stop_response = await client.post(
        "/api/v1/time-entries/stop",
        params={"description": "Completed consultation"}
    )
    assert stop_response.status_code == 200