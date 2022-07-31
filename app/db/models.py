from gino_starlette import Gino
from sqlalchemy import Column, Text, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.config import settings

db = Gino(dsn=settings.pg_dsn)


class ShopUnitModel(db.Model):
    __tablename__ = 'ShopUnit'

    id = Column(UUID, primary_key=True)
    name = Column(Text, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    parentId = Column(UUID, ForeignKey('ShopUnit.id', ondelete='CASCADE'), index=True)
    type = Column(Text, nullable=False)
    price = Column(Integer, nullable=True)

    @staticmethod
    async def update_category_price(node: 'ShopUnitModel'):
        if not node.parentId:
            return
        parent_node = await ShopUnitModel.get(node.parentId)
        await ShopUnitModel.__set_price(parent_node)
        await ShopUnitModel.update_category_price(parent_node)

    @staticmethod
    async def __set_price(node: 'ShopUnitModel') -> None:
        sum_func = db.func.sum(ShopUnitModel.price)
        count_func = db.func.count(ShopUnitModel.id)
        # TODO: найти способ совместить эти функции в одну

        average_price = await db.select((sum_func, count_func)).where(ShopUnitModel.parentId == node.id).gino.all()
        print(average_price, node.id)
        # if average_price is None:
        #     await node.update(price=None).apply()
        # else:
        #     await node.update(price=int(average_price)).apply()
