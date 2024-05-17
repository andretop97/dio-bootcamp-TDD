import pytest
import asyncio
from uuid import UUID
from httpx import AsyncClient

from src.db.mongo import db_client
from src.schemas.filters import ProductsFilters
from src.schemas.product import ProductIn, ProductUpdate
from src.usecases.product import product_usecase

from tests.factories import product_data, products_data


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mongo_client():
    return db_client.get()


@pytest.fixture(autouse=True)
async def clear_collections(mongo_client):
    yield
    collections_names = await mongo_client.get_database().list_collection_names()
    for collection_name in collections_names:
        if collection_name.startswith("system"):
            continue

        await mongo_client.get_database()[collection_name].delete_many({})


@pytest.fixture
async def client() -> AsyncClient:
    from main import app

    async with AsyncClient(app=app, base_url="http://test/") as ac:
        yield ac


@pytest.fixture
def products_url() -> str:
    return "/products/"


@pytest.fixture
def product_id() -> UUID:
    return UUID("50dceb9e-57d0-421c-a9ed-fdacecc0d2fe")


@pytest.fixture
def product_in(product_id):
    return ProductIn(**product_data(), id=product_id)


@pytest.fixture
def products_in(product_id):
    return [ProductIn(**product) for product in products_data()]


@pytest.fixture
def product_up(product_id):
    return ProductUpdate(**product_data(), id=product_id)


@pytest.fixture
async def product_inserted(product_in):
    return await product_usecase.create(body=product_in)


@pytest.fixture
async def products_inserted(products_in):
    return [await product_usecase.create(body=product_in) for product_in in products_in]


@pytest.fixture
async def filters():
    return ProductsFilters(price_gt="5.000", price_lt="8.000")
