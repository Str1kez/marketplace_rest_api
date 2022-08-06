from fastapi import APIRouter, BackgroundTasks, Path
from pydantic.types import UUID4
from starlette.responses import Response

from app.db.models import ShopUnitModel
from app.utils.responses import VALIDATION_ERROR_RESPONSE, NOT_FOUND_RESPONSE

router = APIRouter(prefix='/delete',
                   tags=['Delete item'],
                   responses=VALIDATION_ERROR_RESPONSE | NOT_FOUND_RESPONSE)


@router.delete('/{id}')
async def delete_node(background_tasks: BackgroundTasks, id: UUID4 = Path(..., description='**Existing** Item id',
                                                                          example='3fa85f64-5717-4562-b3fc-2c963f66afa4')):
    """### Удаление узла"""
    
    node = await ShopUnitModel.get_or_404(id)
    await node.delete()
    background_tasks.add_task(ShopUnitModel.update_category_price, node)
    return Response()
