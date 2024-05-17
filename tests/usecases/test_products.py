import pytest
from src.exceptions import NotFoundException
from src.schemas.product import ProductOut, ProductUpdateOut
from src.usecases.product import product_usecase


async def test_usecase_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


async def test_usecase_get_should_return_success(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


async def test_usecase_get_should_return_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(id="bcae69db-a1ee-4981-b28d-330bf0474ecd")

    assert (
        err.value.message
        == "Product not found with filter: UUID('bcae69db-a1ee-4981-b28d-330bf0474ecd')"
    )


@pytest.mark.usefixtures("products_inserted")
async def test_usecase_query_should_return_success():
    result = await product_usecase.query()

    assert isinstance(result, list)
    assert len(result) > 1


@pytest.mark.usefixtures("products_inserted")
async def test_usecase_query_filters_should_return_success(filters):
    result = await product_usecase.query(filters)
    assert isinstance(result, list)
    assert len(result) == 2


async def test_usecase_update_should_return_success(product_inserted, product_up):
    product_up.price = "7.500"
    result = await product_usecase.update(id=product_inserted.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)


async def test_usecase_update_should_return_not_found(product_up):
    product_up.price = "7.500"
    id: str = "bcae69db-a1ee-4981-b28d-330bf0474ecd"

    with pytest.raises(NotFoundException) as err:
        await product_usecase.update(id=id, body=product_up)

    assert (
        err.value.message
        == "Product not found with filter: UUID('bcae69db-a1ee-4981-b28d-330bf0474ecd')"
    )


async def test_usecase_delete_should_return_success(product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)
    assert result is True
