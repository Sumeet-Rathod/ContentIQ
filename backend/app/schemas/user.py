from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from app.schemas.tenant import TenantResponse

UserRole = Literal["admin", "editor", "client"]

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    tenant_name: Optional[str] = "My Agency Workspace"
    plan: Optional[str] = "starter"

class UserInvite(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    role: UserRole = "editor"
    password: Optional[str] = "ContentIQ123!"

class UserRoleUpdate(BaseModel):
    role: UserRole

class UserResponse(UserBase):
    id: str
    tenant_id: str
    role: UserRole
    created_at: str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    tenant: Optional[TenantResponse] = None
