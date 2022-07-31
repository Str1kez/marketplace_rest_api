from fastapi import APIRouter
from fastapi.responses import Response

from app.db.models import ShopUnitModel
from app.db.validation_models import ShopUnitImportRequest
from app.exceptions import CustomValidationError
from app.utils.swagger_responses import VALIDATION_ERROR_RESPONSE
from app.validators import parent_is_category

router = APIRouter(prefix='/imports',
                   tags=['Import items'],
                   responses=VALIDATION_ERROR_RESPONSE)


@router.post('')
async def post_imports(imports: ShopUnitImportRequest):
    """
    ### Lets send a list of nodes!
    """
    if not await parent_is_category(imports.items):
        raise CustomValidationError(message='parent is not CATEGORY')
    for node in imports.items:
        # Здесь node -> ShopUnitImport, а в бд ShopUnit
        new_node = await ShopUnitModel.get(node.id)
        if new_node:
            await new_node.update(date=imports.updateDate, **node.dict()).apply()
        else:
            await ShopUnitModel.create(date=imports.updateDate, **node.dict())
    # TODO: создать background task на изменение цены в бд у категорий
    return Response()
