from bson import ObjectId
from typing import Optional

def validate_object_id(id_str: str) -> Optional[ObjectId]:
    """
    Valida e converte string para ObjectId.
    Retorna ObjectId se válido, None se inválido.
    """
    try:
        return ObjectId(id_str)
    except:
        return None