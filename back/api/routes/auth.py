from fastapi import APIRouter, HTTPException

auth = APIRouter(prefix="/auth")


# ===== USER =====
@auth.post("/register")
def register(username: str, password: str):
    # Add simple password validation
    raise HTTPException(status_code=500, detail="Not implemented")


@auth.post("/login")
def login(username: str, password: str):
    raise HTTPException(status_code=500, detail="Not implemented")


@auth.post("/logout")
def logout():
    raise HTTPException(status_code=500, detail="Not implemented")
