from app.db.models import ShopUnitModel


async def get_all_children_list(node: ShopUnitModel) -> dict:
    result = node.to_dict()
    nodes = await ShopUnitModel.query.where(ShopUnitModel.parentId == node.id).gino.all()
    if nodes:
        result['children'] = [await get_all_children_list(node) for node in nodes]
    return result
