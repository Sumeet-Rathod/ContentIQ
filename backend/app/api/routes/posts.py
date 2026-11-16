from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.services.post_service import (
    create_post, list_posts, get_post_by_id, update_post, delete_post
)
from app.core.deps import get_current_user, require_editor_or_admin

router = APIRouter(prefix="/posts", tags=["Posts & Scheduling"])

@router.get("", response_model=List[PostResponse])
async def get_all_posts(
    status: Optional[str] = Query(None, description="Filter by status: draft, scheduled, published, or all"),
    platform: Optional[str] = Query(None, description="Filter by platform: instagram, linkedin, youtube, or all"),
    month: Optional[int] = Query(None, description="Filter by scheduled month (1-12)"),
    year: Optional[int] = Query(None, description="Filter by scheduled year"),
    current_user: dict = Depends(get_current_user)
):
    """Retrieve posts filtered strictly by the user's tenant ID, with optional platform/status/month filters."""
    return await list_posts(
        tenant_id=current_user["tenant_id"],
        status=status,
        platform=platform,
        month=month,
        year=year
    )

@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_new_post(
    post_in: PostCreate,
    current_user: dict = Depends(require_editor_or_admin)
):
    """Create a new post. Client role is prohibited; Editors and Admins permitted."""
    return await create_post(
        tenant_id=current_user["tenant_id"],
        user_id=current_user["id"],
        post_in=post_in
    )

@router.get("/{post_id}", response_model=PostResponse)
async def get_single_post(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get single post by ID, strictly isolating tenant ownership."""
    return await get_post_by_id(tenant_id=current_user["tenant_id"], post_id=post_id)

@router.put("/{post_id}", response_model=PostResponse)
async def update_existing_post(
    post_id: str,
    post_in: PostUpdate,
    current_user: dict = Depends(require_editor_or_admin)
):
    """Update post details. Client role is prohibited."""
    return await update_post(
        tenant_id=current_user["tenant_id"],
        post_id=post_id,
        post_in=post_in
    )

@router.delete("/{post_id}")
async def delete_existing_post(
    post_id: str,
    current_user: dict = Depends(require_editor_or_admin)
):
    """Delete a post. Client role is prohibited."""
    return await delete_post(tenant_id=current_user["tenant_id"], post_id=post_id)
