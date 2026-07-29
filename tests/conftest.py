from copy import deepcopy

import pytest
from httpx import ASGITransport, AsyncClient

import src.app as app_module


@pytest.fixture
async def client():
    transport = ASGITransport(app=app_module.app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_activities_state():
    # Keep tests isolated because the API stores mutable state in memory.
    original_activities = deepcopy(app_module.activities)

    yield

    app_module.activities.clear()
    app_module.activities.update(deepcopy(original_activities))
