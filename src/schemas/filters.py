from decimal import Decimal
from typing import Annotated, Optional
from bson import Decimal128
from pydantic import AfterValidator, BaseModel, Field


def convert_decimal_128(v):
    return Decimal128(str(v))


Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]


class ProductsFilters(BaseModel):
    price_gt: Optional[Decimal_] = Field(None, description="Limite superior de preço")
    price_lt: Optional[Decimal_] = Field(None, description="Limite inferior de preço")

    def to_mongo_filters(self) -> dict:
        filter = {}
        filter["price"] = {}
        if self.price_gt:
            filter["price"]["$gt"] = self.price_gt
        if self.price_gt:
            filter["price"]["$lt"] = self.price_lt

        return filter
