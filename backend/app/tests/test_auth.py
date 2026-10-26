
import pytest


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser1",
            "email": "testuser1@example.com",
            "password": "StrongPass123!",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["username"] == "testuser1"
    assert data["email"] == "testuser1@example.com"
    assert data["is_active"] is True
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    user_data = {
        "username": "testuser2",
        "email": "duplicate@example.com",
        "password": "StrongPass123!",
    }

    first_response = await client.post(
        "/api/v1/auth/register",
        json=user_data,
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "differentuser",
            "email": "duplicate@example.com",
            "password": "AnotherPass123!",
        },
    )

    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "loginuser",
            "email": "loginuser@example.com",
            "password": "StrongPass123!",
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "loginuser@example.com",
            "password": "StrongPass123!",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "wrongpassuser",
            "email": "wrongpass@example.com",
            "password": "StrongPass123!",
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrongpass@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_without_token(client):
    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_valid_token(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "meuser",
            "email": "meuser@example.com",
            "password": "StrongPass123!",
        },
    )

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "meuser@example.com",
            "password": "StrongPass123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "meuser@example.com"
    assert response.json()["username"] == "meuser"
