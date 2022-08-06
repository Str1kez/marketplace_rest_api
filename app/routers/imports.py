from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import Response

from app.db.models import ShopUnitModel
from app.db.validation_models import ShopUnitImportRequest
from app.exceptions import CustomValidationError
from app.utils.responses import VALIDATION_ERROR_RESPONSE
from app.validators import parent_is_category

router = APIRouter(prefix='/imports',
                   tags=['Import items'],
                   responses=VALIDATION_ERROR_RESPONSE)


async def parent_checker(imports: ShopUnitImportRequest):
    if not await parent_is_category(imports.items):
        raise CustomValidationError(message='parent is not CATEGORY')
    return imports


@router.post('')
async def post_imports(background_tasks: BackgroundTasks, imports: ShopUnitImportRequest = Depends(parent_checker)):
    """### Отправь список узлов!"""
    
    for node in imports.items:
        # Здесь node -> ShopUnitImport, а в бд ShopUnit
        new_node = await ShopUnitModel.get(node.id)
        if new_node:
            await new_node.update(date=imports.updateDate, **node.dict()).apply()
        else:
            new_node = await ShopUnitModel.create(date=imports.updateDate, **node.dict())
        background_tasks.add_task(ShopUnitModel.update_category_price, new_node)

    return Response()
