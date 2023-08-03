import pytest
from sqlalchemy import insert, select

from auth.models import role
from conftest import async_session_maker, client


async def test_create_role():
    async with async_session_maker() as session:
        stat = insert(role).values(id=1, name="admin", permissions=None)
        await session.execute(stat)
        await session.commit()
        query = select(role)
        result = await session.execute(query)
        assert result.all() == [(1, 'admin', None)], "Роль не добавилась"


def test_register():
    response = client.post("/auth/register", json={
        "email": "user@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 0
    })
    assert response.status_code == 201
