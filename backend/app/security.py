import hmac

from fastapi import Header, HTTPException, status

from .config import get_settings


def require_admin_key(x_admin_key: str = Header(default="")) -> None:
    expected = get_settings().admin_api_key
    if not x_admin_key or not hmac.compare_digest(x_admin_key, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный ключ администратора",
        )

