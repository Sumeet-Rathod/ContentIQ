from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas.user import UserInvite, UserRoleUpdate, UserResponse
from app.services.auth_service import invite_team_member, list_team_members, update_member_role
from app.core.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/team", tags=["Team & Multi-tenancy"])

@router.get("/members", response_model=List[UserResponse])
async def get_team_members(current_user: dict = Depends(get_current_user)):
    """List all team members belonging strictly to the caller's tenant."""
    return await list_team_members(current_user["tenant_id"])

@router.post("/invite", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def invite_member(
    invite_in: UserInvite,
    current_admin: dict = Depends(get_current_admin)
):
    """Admin only: Invite/add a team member to the current tenant with specified role."""
    return await invite_team_member(current_admin["tenant_id"], invite_in)

@router.put("/members/{user_id}/role", response_model=UserResponse)
async def change_role(
    user_id: str,
    update_in: UserRoleUpdate,
    current_admin: dict = Depends(get_current_admin)
):
    """Admin only: Change a team member's role (admin, editor, client) within the tenant."""
    return await update_member_role(current_admin["tenant_id"], user_id, update_in)
