from fastapi import APIRouter, Path
from pydantic.types import UUID4

from app.db.models import ShopUnit
from app.db.validation_models import ShopUnitExportRequest
from app.utils.children_expand import get_all_children_list
from app.utils.responses import VALIDATION_ERROR_RESPONSE, NOT_FOUND_RESPONSE

router = APIRouter(prefix='/nodes',
                   tags=['View item'],
                   responses=VALIDATION_ERROR_RESPONSE | NOT_FOUND_RESPONSE)


@router.get('/{id}', response_model=ShopUnitExportRequest)
async def view_node(id: UUID4 = Path(..., description='**Existing** Item id', example='3fa85f64-5717-4562-b3fc-2c963f66afa6')):
    """### Можно посмотреть на товары"""
    
    node = await ShopUnit.get_or_404(id)
    # Просмотр всех объектов ~O(n^2)
    node_dict = await get_all_children_list(node)
    
    return node_dict
