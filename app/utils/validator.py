from app.models import Role, LICENSE_REQUIRED_ROLES

def normalize_role(role: str) -> str:
    if not role:
        return ""
    return role.strip().lower()

def is_valid_role(role: str) -> bool:
    return normalize_role(role) in {r.value for r in Role}



def staff_roles_only(role: str) -> bool:
    role_norm = normalize_role(role)
    return role_norm in {
        Role.RECEPTIONIST.value,
        Role.DOCTOR.value,
        Role.RADIOGRAPHER.value,
        Role.RADIOLOGIST.value,
    }

def is_patient_role(role: str) -> bool:
    return normalize_role(role) == Role.PATIENT.value