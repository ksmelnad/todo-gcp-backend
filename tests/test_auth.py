import pytest
import time
import os

def make_token(secret: str, expired: bool = False, wrong_audience: bool = False) -> str:
    from jose import jwt
    payload = {
        "sub": "user-123",
        "role": "authenticated",
        "aud": "wrong" if wrong_audience else "authenticated",
        "exp": int(time.time()) + (-10 if expired else 3600),
        "iat": int(time.time()),
    }
    return jwt.encode(payload, secret, algorithm="HS256")

@pytest.mark.anyio
async def test_protected_requires_auth(client):
    response = await client.get("/protected")
    assert response.status_code == 401  # No auth header → HTTPBearer returns 401

@pytest.mark.anyio
async def test_protected_accepts_valid_token(client, monkeypatch):
    secret = "test-secret"
    monkeypatch.setenv("SUPABASE_JWT_SECRET", secret)
    token = make_token(secret)
    response = await client.get(
        "/protected", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["user_id"] == "user-123"

@pytest.mark.anyio
async def test_protected_rejects_expired_token(client, monkeypatch):
    secret = "test-secret"
    monkeypatch.setenv("SUPABASE_JWT_SECRET", secret)
    token = make_token(secret, expired=True)
    response = await client.get(
        "/protected", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401

@pytest.mark.anyio
async def test_protected_rejects_wrong_audience(client, monkeypatch):
    secret = "test-secret"
    monkeypatch.setenv("SUPABASE_JWT_SECRET", secret)
    token = make_token(secret, wrong_audience=True)
    response = await client.get(
        "/protected", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
