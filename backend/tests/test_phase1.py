import pytest

@pytest.mark.asyncio
async def test_register_and_login(client):
    """Test user registration and subsequent JWT login."""
    # Register Tenant Alpha
    reg_payload = {
        "email": "alpha_admin@example.com",
        "name": "Alpha Admin",
        "password": "Password123!",
        "tenant_name": "Alpha Media Agency"
    }
    res = await client.post("/api/auth/register", json=reg_payload)
    assert res.status_code == 201, res.text
    data = res.json()
    assert "access_token" in data
    assert data["user"]["email"] == "alpha_admin@example.com"
    assert data["user"]["role"] == "admin"
    assert data["tenant"]["name"] == "Alpha Media Agency"

    # Login with valid credentials
    login_res = await client.post("/api/auth/login", json={
        "email": "alpha_admin@example.com",
        "password": "Password123!"
    })
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert "access_token" in login_data

    # Login with invalid credentials
    bad_login = await client.post("/api/auth/login", json={
        "email": "alpha_admin@example.com",
        "password": "WrongPassword!"
    })
    assert bad_login.status_code == 401

@pytest.mark.asyncio
async def test_tenant_isolation(client):
    """
    CRITICAL MULTI-TENANCY TEST:
    A user from Tenant Alpha MUST NEVER see, read, modify, or delete Tenant Beta's data.
    """
    # 1. Register Tenant Alpha
    res_a = await client.post("/api/auth/register", json={
        "email": "owner_a@agencya.com",
        "name": "Agency A Owner",
        "password": "SecretPassword1!",
        "tenant_name": "Agency A"
    })
    assert res_a.status_code == 201
    token_a = res_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # 2. Register Tenant Beta
    res_b = await client.post("/api/auth/register", json={
        "email": "owner_b@agencyb.com",
        "name": "Agency B Owner",
        "password": "SecretPassword2!",
        "tenant_name": "Agency B"
    })
    assert res_b.status_code == 201
    token_b = res_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 3. Tenant A creates a post
    post_a = await client.post("/api/posts", headers=headers_a, json={
        "platform": "instagram",
        "caption": "Confidential Campaign for Tenant A",
        "hashtags": ["#AgencyA", "#Secret"],
        "scheduled_time": "2026-10-25T14:30:00",
        "status": "scheduled"
    })
    assert post_a.status_code == 201
    post_a_id = post_a.json()["id"]

    # 4. Tenant B creates a post
    post_b = await client.post("/api/posts", headers=headers_b, json={
        "platform": "linkedin",
        "caption": "Quarterly Update for Tenant B",
        "hashtags": ["#AgencyB", "#Growth"],
        "scheduled_time": "2026-10-26T09:15:00",
        "status": "scheduled"
    })
    assert post_b.status_code == 201
    post_b_id = post_b.json()["id"]

    # 5. Tenant A lists posts: MUST ONLY see Tenant A's post
    list_a = await client.get("/api/posts", headers=headers_a)
    assert list_a.status_code == 200
    posts_seen_by_a = list_a.json()
    ids_seen_by_a = [p["id"] for p in posts_seen_by_a]
    assert post_a_id in ids_seen_by_a
    assert post_b_id not in ids_seen_by_a, "LEAK DETECTED: Tenant A saw Tenant B's post in list!"

    # 6. Tenant B lists posts: MUST ONLY see Tenant B's post
    list_b = await client.get("/api/posts", headers=headers_b)
    assert list_b.status_code == 200
    posts_seen_by_b = list_b.json()
    ids_seen_by_b = [p["id"] for p in posts_seen_by_b]
    assert post_b_id in ids_seen_by_b
    assert post_a_id not in ids_seen_by_b, "LEAK DETECTED: Tenant B saw Tenant A's post in list!"

    # 7. Tenant A directly attempts to GET Tenant B's post by ID: MUST 404 / Forbidden
    leak_get = await client.get(f"/api/posts/{post_b_id}", headers=headers_a)
    assert leak_get.status_code == 404, "SECURITY BREACH: Tenant A was able to retrieve Tenant B's post by ID!"

    # 8. Tenant A attempts to UPDATE Tenant B's post: MUST 404 / Forbidden
    leak_put = await client.put(f"/api/posts/{post_b_id}", headers=headers_a, json={
        "caption": "Malicious Tampering by Tenant A"
    })
    assert leak_put.status_code == 404, "SECURITY BREACH: Tenant A was able to update Tenant B's post!"

    # 9. Tenant A attempts to DELETE Tenant B's post: MUST 404 / Forbidden
    leak_del = await client.delete(f"/api/posts/{post_b_id}", headers=headers_a)
    assert leak_del.status_code == 404, "SECURITY BREACH: Tenant A was able to delete Tenant B's post!"

@pytest.mark.asyncio
async def test_post_crud_and_hour_extraction(client):
    """Test post CRUD operations and ensure scheduled_hour is derived without UTC conversion."""
    res = await client.post("/api/auth/register", json={
        "email": "crud_admin@example.com",
        "name": "CRUD Admin",
        "password": "Password123!",
        "tenant_name": "CRUD Corp"
    })
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create post with scheduled_time "2026-11-05T18:45"
    create_res = await client.post("/api/posts", headers=headers, json={
        "platform": "youtube",
        "caption": "New Product Launch Showcase #Tech #AI",
        "hashtags": ["Tech", "#AI"],
        "scheduled_time": "2026-11-05T18:45",
        "status": "scheduled"
    })
    assert create_res.status_code == 201
    post = create_res.json()
    assert post["platform"] == "youtube"
    assert post["scheduled_hour"] == 18, f"Expected hour 18, got {post['scheduled_hour']}"
    assert "#Tech" in post["hashtags"]
    assert "#AI" in post["hashtags"]
    post_id = post["id"]

    # Update post
    update_res = await client.put(f"/api/posts/{post_id}", headers=headers, json={
        "caption": "Updated Launch Showcase",
        "scheduled_time": "2026-11-05T21:15"
    })
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["caption"] == "Updated Launch Showcase"
    assert updated["scheduled_hour"] == 21, f"Expected hour 21, got {updated['scheduled_hour']}"

    # Delete post
    del_res = await client.delete(f"/api/posts/{post_id}", headers=headers)
    assert del_res.status_code == 200

    # Ensure deleted
    get_res = await client.get(f"/api/posts/{post_id}", headers=headers)
    assert get_res.status_code == 404

@pytest.mark.asyncio
async def test_role_permissions(client):
    """
    Test role permission boundaries:
    - Admin: can manage team and content
    - Editor: can create and update content, cannot manage team
    - Client: read-only; cannot create or update content
    """
    # Admin registers
    res = await client.post("/api/auth/register", json={
        "email": "agency_boss@test.com",
        "name": "Agency Boss",
        "password": "Password123!",
        "tenant_name": "Boss Agency"
    })
    admin_token = res.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # Admin invites an Editor
    inv_editor = await client.post("/api/team/invite", headers=admin_headers, json={
        "email": "content_creator@test.com",
        "name": "Content Creator",
        "role": "editor",
        "password": "CreatorPass123!"
    })
    assert inv_editor.status_code == 201

    # Admin invites a Client (read-only)
    inv_client = await client.post("/api/team/invite", headers=admin_headers, json={
        "email": "external_client@client.com",
        "name": "External Client",
        "role": "client",
        "password": "ClientPass123!"
    })
    assert inv_client.status_code == 201

    # Login as Editor
    login_editor = await client.post("/api/auth/login", json={
        "email": "content_creator@test.com",
        "password": "CreatorPass123!"
    })
    editor_token = login_editor.json()["access_token"]
    editor_headers = {"Authorization": f"Bearer {editor_token}"}

    # Login as Client
    login_client = await client.post("/api/auth/login", json={
        "email": "external_client@client.com",
        "password": "ClientPass123!"
    })
    client_token = login_client.json()["access_token"]
    client_headers = {"Authorization": f"Bearer {client_token}"}

    # 1. Editor creates post -> SUCCESS
    ed_post = await client.post("/api/posts", headers=editor_headers, json={
        "platform": "instagram",
        "caption": "Editor drafted post",
        "hashtags": ["#Editing"],
        "status": "draft"
    })
    assert ed_post.status_code == 201
    ed_post_id = ed_post.json()["id"]

    # 2. Editor tries to invite team member -> FORBIDDEN (403)
    ed_invite = await client.post("/api/team/invite", headers=editor_headers, json={
        "email": "unauthorized_user@test.com",
        "name": "Unauthorized User",
        "role": "editor"
    })
    assert ed_invite.status_code == 403

    # 3. Client views posts -> SUCCESS (Read-only)
    cl_view = await client.get("/api/posts", headers=client_headers)
    assert cl_view.status_code == 200

    # 4. Client tries to create post -> FORBIDDEN (403)
    cl_create = await client.post("/api/posts", headers=client_headers, json={
        "platform": "instagram",
        "caption": "Client should not be able to create this",
        "status": "draft"
    })
    assert cl_create.status_code == 403

    # 5. Client tries to edit post -> FORBIDDEN (403)
    cl_edit = await client.put(f"/api/posts/{ed_post_id}", headers=client_headers, json={
        "caption": "Client tampering attempt"
    })
    assert cl_edit.status_code == 403

    # 6. Client tries to delete post -> FORBIDDEN (403)
    cl_del = await client.delete(f"/api/posts/{ed_post_id}", headers=client_headers)
    assert cl_del.status_code == 403
