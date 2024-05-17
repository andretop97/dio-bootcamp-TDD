from typing import List
from bson import Decimal128
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4

from src.exceptions import NotFoundException
from src.schemas.filters import ProductsFilters
from src.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from src.usecases.product import ProductUseCase

router = APIRouter(tags=["products"])


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID4 = Path(), usecase: ProductUseCase = Depends()) -> None:
    try:
        return await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUseCase = Depends()
) -> ProductOut:
    return await usecase.create(body=body)


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(id: UUID4 = Path(), usecase: ProductUseCase = Depends()) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(
    filters: str = None, usecase: ProductUseCase = Depends()
) -> List[ProductOut]:
    product_filters = None
    if filters:
        product_filters = ProductsFilters()

        values = filters.split("%")
        for value in values:
            key, val = value.split("@")
            if key == "gt":
                product_filters.price_gt = Decimal128(val)
            if key == "lt":
                product_filters.price_lt = Decimal128(val)
    return await usecase.query(filters=product_filters)


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(),
    body: ProductUpdate = Body(...),
    usecase: ProductUseCase = Depends(),
) -> ProductUpdateOut:
    try:
        return await usecase.update(id=id, body=body)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
