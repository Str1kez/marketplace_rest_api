import json

from pydantic import ValidationError, BaseSettings, PostgresDsn, Field, RedisDsn

import app.config as config
from app.db.validation_models import ShopUnit, ShopUnitType, ShopUnitExportRequest

try:
    su = ShopUnit(id='3fa85f64-5787-4562-b3fc-2c963f66a444',
                  name='ilya',
                  date='2022-05-23T21:12:01.000Z',
                  type='OFFER',
                  parentId='3fa85f64-5787-4562-b3fc-2c963f66a222',
                  price=None)
    # s = json.load(open('./test.json', encoding='utf-8'))
    # ssu = ShopUnitExportRequest(**s)
    # print(ssu.json())
    # su.date = su.date.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    # print(su.date)
    # print(su.type == ShopUnitType.CATEGORY)
    print('CATEGORY' == ShopUnitType.CATEGORY)
    # print(su.dict())
    print(config.settings)
except ValidationError as e:
    print(e.json())
