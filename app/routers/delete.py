from fastapi import APIRouter, BackgroundTasks
from pydantic.types import UUID4
from starlette.responses import Response

from app.db.models import ShopUnitModel
from app.utils.swagger_responses import VALIDATION_ERROR_RESPONSE, NOT_FOUND_RESPONSE

router = APIRouter(prefix='/delete',
                   tags=['Delete item'],
                   responses=VALIDATION_ERROR_RESPONSE | NOT_FOUND_RESPONSE)


@router.delete('/{id}')
async def delete_node(id: UUID4, background_tasks: BackgroundTasks):
    """
    ### Удаление узла
    """
    node = await ShopUnitModel.get_or_404(id)
    await node.delete()
    background_tasks.add_task(ShopUnitModel.update_category_price, node)
    return Response()
