import datetime
from app.db.models import ShopUnit


async def get_all_children_list(node: ShopUnit) -> dict:
    node.date = node.date.astimezone().replace(tzinfo=datetime.timezone.utc)
    result = node.to_dict()
    nodes = await ShopUnit.query.where(ShopUnit.parentId == node.id).gino.all()
    if nodes:
        result['children'] = [await get_all_children_list(node) for node in nodes]
    return result
