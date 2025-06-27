import uuid


def generate_unique_title(prefix: str = "song") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"