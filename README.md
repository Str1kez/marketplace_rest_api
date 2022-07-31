# Marketplace API
## Похоже на Яндекс.Товары
### Используются методы 🔧
* **POST** `imports/` приходит список с товарами 
* **POST** `delete/{id}` удаляем товар
* **GET** `nodes/{id}` запрос на получение сведения о товаре

### Модель товара ShopUnit 🛒
* _id*_	**string($uuid)** <br>
  nullable: false <br>
  example: 3fa85f64-5717-4562-b3fc-2c963f66a333

* _name*_	**string** <br>
nullable: false <br>
Имя категории

* _date*_	**string($date-time)** <br>
nullable: false <br>
example: 2022-05-28T21:12:01.000Z <br>
Время последнего обновления элемента.

* _parentId_	**string($uuid)** <br>
nullable: true <br>
example: 3fa85f64-5717-4562-b3fc-2c963f66a333 <br>
UUID родительской категории

* *type**	**ShopUnitType** <br>
Тип элемента - категория или товар <br>
Enum ["OFFER", "CATEGORY"]

* *children* **List[ShopUnit]**