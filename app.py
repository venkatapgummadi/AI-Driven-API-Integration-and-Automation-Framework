import time
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel

from automated_workflow import process_incoming_data

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Cloud-Native AI-driven API Integration Framework")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Dummy OAuth2 Setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy IP Blocklist for Demonstration
BLOCKED_IPS = {"192.168.1.100", "10.0.0.5"}

# Middleware for IP Blocking
@app.middleware("http")
async def block_ips(request: Request, call_next):
    client_ip = request.client.host
    if client_ip in BLOCKED_IPS:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "IP address is blocked."})
    response = await call_next(request)
    return response

# Pydantic schema for incoming payload
class TransactionPayload(BaseModel):
    transaction_amount: float
    user_transaction_frequency: float
    hour_of_day: float

# Auth Endpoint
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Mock authentication - accept any user/pass combo
    if not form_data.username or not form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": form_data.username + "_token", "token_type": "bearer"}

# Main Data Ingestion Endpoint
@app.post("/api/v1/process-data")
@limiter.limit("5/minute")
async def process_data(request: Request, payload: TransactionPayload, token: str = Depends(oauth2_scheme)):
    """
    Ingests data, passes it to the automated workflow which uses the AI model
    to make real-time decisions, and triggers business logic.
    """
    try:
        data_dict = payload.dict()
        result = process_incoming_data(data_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}
