from gino_starlette import Gino
from sqlalchemy import Column, Text, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.config import settings

db = Gino(dsn=settings.pg_dsn)


class ShopUnit(db.Model):
    __tablename__ = 'ShopUnit'

    id = Column(UUID, primary_key=True)
    name = Column(Text, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    parentId = Column(UUID, ForeignKey('ShopUnit.id', ondelete='CASCADE'), index=True)
    type = Column(Text, nullable=False)
    price = Column(Integer, nullable=True)

    @staticmethod
    async def update_category_price(node: 'ShopUnit') -> None:
        if not node.parentId:
            return
        parent_node = await ShopUnit.get(node.parentId)
        await ShopUnit.__set_price(parent_node)
        await ShopUnit.update_category_price(parent_node)

    @staticmethod
    async def __set_price(node: 'ShopUnit') -> None:
        sum_func = db.func.sum(ShopUnit.price)
        count_func = db.func.count(ShopUnit.id)

        child_price, child_amount = await db.select((sum_func, count_func)).where(ShopUnit.parentId == node.id).gino.first()

        if child_price is None:
            await node.update(price=None).apply()
        else:
            await node.update(price=child_price // child_amount).apply()
