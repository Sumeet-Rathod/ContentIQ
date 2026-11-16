from datetime import datetime, timezone
from bson import ObjectId
from fastapi import HTTPException, status
from app.core.database import get_database
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.user import UserCreate, UserInvite, UserRoleUpdate

async def register_tenant_and_admin(user_in: UserCreate) -> dict:
    db = get_database()
    
    # 1. Check if user already exists
    existing_user = await db.users.find_one({"email": user_in.email.lower()})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )
    
    now_iso = datetime.now(timezone.utc).isoformat()
    
    # 2. Create the tenant
    tenant_name = user_in.tenant_name.strip() if user_in.tenant_name else f"{user_in.name}'s Agency"
    tenant_plan = getattr(user_in, "plan", "starter") or "starter"
    tenant_doc = {
        "name": tenant_name,
        "plan": tenant_plan,
        "created_at": now_iso
    }
    tenant_result = await db.tenants.insert_one(tenant_doc)
    tenant_id = str(tenant_result.inserted_id)
    
    # 3. Create the initial user with 'admin' role
    user_doc = {
        "email": user_in.email.lower(),
        "hashed_password": get_password_hash(user_in.password),
        "name": user_in.name,
        "tenant_id": tenant_id,
        "role": "admin",
        "created_at": now_iso
    }
    user_result = await db.users.insert_one(user_doc)
    user_id = str(user_result.inserted_id)
    
    # 4. Generate JWT
    token = create_access_token(
        subject=user_id,
        extra_claims={"tenant_id": tenant_id, "role": "admin"}
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "email": user_doc["email"],
            "name": user_doc["name"],
            "tenant_id": tenant_id,
            "role": "admin",
            "created_at": now_iso
        },
        "tenant": {
            "id": tenant_id,
            "name": tenant_doc["name"],
            "plan": tenant_doc["plan"],
            "created_at": now_iso
        }
    }

async def authenticate_user(email: str, password: str) -> dict:
    db = get_database()
    user = await db.users.find_one({"email": email.lower()})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = str(user["_id"])
    tenant_id = user["tenant_id"]
    tenant = await db.tenants.find_one({"_id": ObjectId(tenant_id)})
    
    token = create_access_token(
        subject=user_id,
        extra_claims={"tenant_id": tenant_id, "role": user["role"]}
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "email": user["email"],
            "name": user["name"],
            "tenant_id": tenant_id,
            "role": user["role"],
            "created_at": user.get("created_at", "")
        },
        "tenant": {
            "id": str(tenant["_id"]) if tenant else tenant_id,
            "name": tenant["name"] if tenant else "Default Agency",
            "plan": tenant.get("plan", "free") if tenant else "free",
            "created_at": tenant.get("created_at", "") if tenant else ""
        }
    }

async def invite_team_member(admin_tenant_id: str, invite_in: UserInvite) -> dict:
    db = get_database()
    existing_user = await db.users.find_one({"email": invite_in.email.lower()})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )
    
    now_iso = datetime.now(timezone.utc).isoformat()
    new_user_doc = {
        "email": invite_in.email.lower(),
        "hashed_password": get_password_hash(invite_in.password or "ContentIQ123!"),
        "name": invite_in.name,
        "tenant_id": admin_tenant_id,
        "role": invite_in.role,
        "created_at": now_iso
    }
    result = await db.users.insert_one(new_user_doc)
    new_user_doc["id"] = str(result.inserted_id)
    return new_user_doc

async def list_team_members(tenant_id: str) -> list:
    db = get_database()
    # Explicit tenant isolation: filter strictly by tenant_id
    cursor = db.users.find({"tenant_id": tenant_id})
    members = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["hashed_password"]
        members.append(doc)
    return members

async def update_member_role(tenant_id: str, user_id: str, update_in: UserRoleUpdate) -> dict:
    db = get_database()
    # Explicit tenant isolation: query matching both _id AND tenant_id
    result = await db.users.find_one_and_update(
        {"_id": ObjectId(user_id), "tenant_id": tenant_id},
        {"$set": {"role": update_in.role}},
        return_document=True
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team member not found in this tenant workspace"
        )
    result["id"] = str(result["_id"])
    del result["hashed_password"]
    return result
