from fastapi import APIRouter
from pydantic.types import UUID4

from app.db.models import ShopUnitModel
from app.db.validation_models import ShopUnitExportRequest
from app.utils.children_expand import get_all_children_list
from app.utils.swagger_responses import VALIDATION_ERROR_RESPONSE, NOT_FOUND_RESPONSE

router = APIRouter(prefix='/nodes',
                   tags=['View item'],
                   responses=VALIDATION_ERROR_RESPONSE | NOT_FOUND_RESPONSE)


@router.get('/{id}', response_model=ShopUnitExportRequest)
async def view_node(id: UUID4):
    """
    ### Можно посмотреть на товары
    """
    node = await ShopUnitModel.get_or_404(id)
    # Просмотр всех объектов ~O(n^2)
    node_dict = await get_all_children_list(node)
    return node_dict
