from app.db.models import ShopUnit
from app.db.validation_models import ShopUnitImport, ShopUnitType


def __parent_is_category_in_query(nodes: list[ShopUnitImport], pending: ShopUnitImport) -> None | bool:
    """
    True: Если род узел корректен и в очереди
    False: Если род узел некорректен и в очереди
    None: Если род узел не в очереди
    """
    for node in nodes:
        if node.id == pending.parentId:
            return node.type is ShopUnitType.CATEGORY


async def parent_is_category(nodes: list[ShopUnitImport]) -> bool:
    for node in nodes:
        if node.parentId is None:
            continue
        in_query = __parent_is_category_in_query(nodes, node)
        if in_query == False:
            return False
        elif in_query:
            continue
        parent_node = await ShopUnit.get_or_404(node.parentId)
        if parent_node.type != ShopUnitType.CATEGORY:
            return False
    return True
