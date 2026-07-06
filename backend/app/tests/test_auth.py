from app.core.security import (
    hash_password, verify_password,
    create_access_token, decode_token
)

def test_password_hash_and_verify():
    hashed = hash_password('MyPassword123')
    assert verify_password('MyPassword123', hashed)
    assert not verify_password('WrongPassword', hashed)

def test_access_token_creation_and_decode():
    token = create_access_token('user-123', 'doctor', 'clinic-456')
    payload = decode_token(token)
    assert payload['sub'] == 'user-123'
    assert payload['role'] == 'doctor'
    assert payload['type'] == 'access'

def test_access_token_has_jti():
    token = create_access_token('user-123', 'nurse')
    payload = decode_token(token)
    assert 'jti' in payload and len(payload['jti']) > 0