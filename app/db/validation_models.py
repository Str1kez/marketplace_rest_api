import datetime
from enum import Enum

from pydantic import BaseModel, validator
from pydantic.types import UUID, PositiveInt

from app.utils.datetime_convert import convert_to_iso_8601


class ShopUnitType(str, Enum):
    CATEGORY = 'CATEGORY'
    OFFER = 'OFFER'


class ShopUnitImport(BaseModel):
    id: UUID
    name: str
    parentId: UUID | None
    type: ShopUnitType
    price: PositiveInt | None

    # @validator('price')
    # def validate_type_price(cls, v, values):
    #     """
    #     Валидация категорий на безценовой основе
    #     """
    #     t = values.get('type')
    #     if t is ShopUnitType.CATEGORY and v is not None:
    #         raise ValueError('price of category should be null')
    #     if t is ShopUnitType.OFFER and v is None:
    #         raise ValueError("price of offer shouldn't be null")
    #     return v

    @validator('parentId')
    def validate_parent_id(cls, v, values):
        """
        Валидация на рекурсивное наследование
        """
        id = values.get('id')
        if id == v:
            raise ValueError("parentId can't handle self id")
        return v


class ShopUnit(ShopUnitImport):
    date: datetime.datetime

    class Config:
        json_encoders = {
            datetime.datetime: convert_to_iso_8601,
        }


class ShopUnitImportRequest(BaseModel):
    items: list[ShopUnitImport]
    updateDate: datetime.datetime

    @validator('items')
    def validate_unique_id(cls, v):
        """
        Валидация на одинаковые id у товаров
        """
        v_set = set(unit.id for unit in v)
        if len(v_set) != len(v):
            raise ValueError("Objects have similar id")
        return v


class ShopUnitExportRequest(ShopUnit):
    children: list['ShopUnitExportRequest'] | None

    # Config.extra = allow?
    # Как убрать валидацию???
