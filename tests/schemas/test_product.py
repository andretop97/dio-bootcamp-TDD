from pydantic import ValidationError
import pytest
from src.schemas.product import ProductIn
from tests.factories import product_data


def test_schema_validated():
    data = product_data()
    product = ProductIn(**data)

    assert product.name == "Iphone 14 Pro Max"


def test_schema_return_raise():
    data = {
        "name": "Iphone 14 pro max",
        "quantity": 10,
        "price": "8.500",
    }

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)
        assert err.value.errors()[0]["msg"] == "Field required"
