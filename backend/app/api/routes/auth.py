from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, TokenResponse, LoginRequest, UserResponse
from app.schemas.tenant import TenantResponse
from app.services.auth_service import register_tenant_and_admin, authenticate_user
from app.core.deps import get_current_user
from app.core.database import get_database
from bson import ObjectId

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    """Register a new user and create their isolated organization/tenant with Admin role."""
    return await register_tenant_and_admin(user_in)

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """Authenticate with email and password to receive a JWT access token."""
    return await authenticate_user(credentials.email, credentials.password)

@router.post("/login/oauth", response_model=TokenResponse, include_in_schema=False)
async def login_oauth(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 password flow support for Swagger UI."""
    return await authenticate_user(form_data.username, form_data.password)

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Fetch current authenticated user profile and tenant information."""
    db = get_database()
    tenant = await db.tenants.find_one({"_id": ObjectId(current_user["tenant_id"])})
    return {
        "user": {
            "id": current_user["id"],
            "email": current_user["email"],
            "name": current_user["name"],
            "tenant_id": current_user["tenant_id"],
            "role": current_user["role"],
            "created_at": current_user.get("created_at", "")
        },
        "tenant": {
            "id": str(tenant["_id"]) if tenant else current_user["tenant_id"],
            "name": tenant["name"] if tenant else "Agency",
            "plan": tenant.get("plan", "free") if tenant else "free",
            "created_at": tenant.get("created_at", "") if tenant else ""
        }
    }
