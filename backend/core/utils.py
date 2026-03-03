
from bson import ObjectId


def validate_object_id(id_str: str) -> ObjectId | None:
    """
    Valida e converte string para ObjectId.
    Retorna ObjectId se válido, None se inválido.
    """
    try:
        return ObjectId(id_str)
    except (ValueError, TypeError):
        return None