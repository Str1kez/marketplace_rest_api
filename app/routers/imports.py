from fastapi import APIRouter, BackgroundTasks, Depends, Body
from fastapi.responses import Response

from datetime import datetime as dt

from app.db.models import ShopUnitModel
from app.db.validation_models import ShopUnitImportRequest
from app.exceptions import CustomValidationError
from app.utils.datetime_convert import convert_to_iso_8601
from app.utils.responses import VALIDATION_ERROR_RESPONSE
from app.validators import parent_is_category

router = APIRouter(prefix='/imports',
                   tags=['Import items'],
                   responses=VALIDATION_ERROR_RESPONSE)


async def parent_checker(imports: ShopUnitImportRequest = Body(
    examples={
        "category": {
            "summary": "Example with category",
            "description": "Single **category** in body",
            "value": {
                "items": [
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "name": "Auto",
                        "parentId": None,
                        "type": "CATEGORY",
                        "price": None
                    }
                ],
                "updateDate": convert_to_iso_8601(dt.now())
            }
        },
        "offer": {
            "summary": "Example with offer",
            "description": "Single **offer** in body",
            "value": {
                "items": [
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa1",
                        "name": "Трактор",
                        "parentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "type": "OFFER",
                        "price": 4534543
                    }
                ],
                "updateDate": convert_to_iso_8601(dt.now())
            }
        },
        "category_child": {
            "summary": "Example with child category",
            "description": "Child **category** in body",
            "value": {
                "items": [
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa2",
                        "name": "Легковые",
                        "parentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "type": "CATEGORY",
                        "price": None
                    }
                ],
                "updateDate": convert_to_iso_8601(dt.now())
            }
        },
    }
)):
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
