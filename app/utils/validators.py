from app.models import Role, LICENSE_REQUIRED_ROLES

def normalize_role(role: str) -> str:
    if not role:
        return ""
    return role.strip().lower()

def is_valid_role(role: str) -> bool:
    return normalize_role(role) in {r.value for r in Role}
