from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
from .audit import correlate_metrics_and_generate_issues

app = FastAPI(title="JaffeBot 3.0 API")

# Allow CORS for local Next.js dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Dummy user/token for demonstration
fake_user = {"username": "admin", "token": "secrettoken"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    if token != fake_user["token"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return fake_user

@app.post("/token")
def login():
    # Dummy token endpoint for demonstration
    return {"access_token": fake_user["token"], "token_type": "bearer"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/agents")
def list_agents():
    return {"agents": []}  # Placeholder

@app.get("/audits")
def list_audits():
    return {"audits": []}  # Placeholder

@app.get("/content")
def list_content():
    return {"content": []}  # Placeholder

@app.get("/backlinks")
def list_backlinks():
    return {"backlinks": []}  # Placeholder

@app.get("/settings")
def get_settings(current_user: dict = Depends(get_current_user)):
    return {"settings": {"user": current_user["username"]}}  # Protected endpoint

class AuditRequest(BaseModel):
    domain: str
    path: Optional[str] = "/"

@app.post("/api/audit")
def run_audit(request: AuditRequest = Body(...)):
    issues = correlate_metrics_and_generate_issues(request.domain)
    return {"issues": issues}

# Integration note:
# The Next.js dashboard (http://localhost:3000) can call these endpoints directly. 