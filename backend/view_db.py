"""
ContentIQ - Terminal Database Inspector
Allows the student and professor to visually inspect the MongoDB database contents in the terminal.
Usage:
    python view_db.py
"""
from pymongo import MongoClient

def inspect_db():
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client["contentiq"]
    
    print("=" * 65)
    print("  CONTENTIQ MONGODB INSPECTOR (DATABASE: contentiq)")
    print("=" * 65)
    
    # 1. Collections Summary
    collections = db.list_collection_names()
    print(f"\n[+] Total Collections Found: {len(collections)}")
    for col in sorted(collections):
        count = db[col].count_documents({})
        print(f"    - Collection '{col}': {count} documents")

    # 2. Tenants Detail
    print("\n[+] Registered Tenants:")
    for t in db.tenants.find():
        print(f"    - Tenant ID: {t['_id']} | Name: {t.get('name')} | Plan: {t.get('plan')}")

    # 3. Users Detail & Roles
    print("\n[+] User Accounts & RBAC Roles:")
    for u in db.users.find():
        print(f"    - Email: {u.get('email'):<26} | Role: {u.get('role').upper():<7} | Name: {u.get('name'):<20} | Tenant: {u.get('tenant_id')}")

    print("\n" + "=" * 65)

if __name__ == "__main__":
    inspect_db()
