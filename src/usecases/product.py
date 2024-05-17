from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic import ValidationError
import pymongo
from src.db.mongo import db_client
from src.exceptions import NotFoundException, BaseException, ValidationErrorException
from src.models.product import ProductModel
from src.schemas.filters import ProductsFilters
from src.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut


class ProductUseCase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.databate: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.databate.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        productModel = ProductModel(**body.model_dump())
        try:
            await self.collection.insert_one(productModel.model_dump())
            return ProductOut(**productModel.model_dump())
        except ValidationError as e:
            # Erro de validação
            raise ValidationErrorException(status_code=400, detail=e.errors())
        except Exception as e:
            # Outros erros
            raise BaseException(status_code=500, detail="Erro interno: " + str(e))

    async def get(self, id: UUID) -> ProductOut:
        product = await self.collection.find_one({"id": id})

        if not product:
            raise NotFoundException(
                message=f"Product not found with filter: UUID('{id}')"
            )

        return ProductOut(**product)

    async def query(self, filters: ProductsFilters = None) -> list[ProductOut]:
        filter = {}
        if filters:
            filter = filters.to_mongo_filters()
        return [ProductOut(**item) async for item in self.collection.find(filter)]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductOut:
        product = await self.collection.find_one({"id": id})

        if not product:
            raise NotFoundException(
                message=f"Product not found with filter: UUID('{id}')"
            )

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(
                message=f"Product not found with filter: UUID('{id}')"
            )

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUseCase()
