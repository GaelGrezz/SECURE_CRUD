from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException, Header
from jose import JWTError, jwt

load_dotenv()
SECRET_KEY = "KEY_HEX"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(subject: str = "frontend-app", expires_delta: timedelta | None = None):
    to_encode = {"sub": subject}
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(auth: str = Header(...)):
    try:
        payload = jwt.decode(auth, SECRET_KEY, algorithms=[ALGORITHM])
        client = payload.get("sub")
        if client is None:
            raise HTTPException(status_code=401, detail="Token no permitido.")
        return client
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado o inválido")