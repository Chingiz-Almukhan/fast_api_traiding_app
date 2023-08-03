import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import operation, Operation
from operations.schemas import OperationCreate, OperationEdit, OperationPartialEdit

router = APIRouter(
    prefix="/operations",
    tags=["Operation"],
)


@router.get("/")
async def get_specific_operations(operation_type: str,
                                  session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type).limit(2)
    result = await session.execute(query)
    result_as_dict = result.mappings().all()
    if result_as_dict:
        return {
            "status": "success",
            "data": result_as_dict,
            "details": None,
        }
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/")
async def add_specific_operations(new_operation: OperationCreate,
                                  session: AsyncSession = Depends(get_async_session)):
    statement = insert(operation).values(**new_operation.dict())
    await session.execute(statement)
    await session.commit()
    return {"status": "success"}


@router.put("/")
async def edit_specific_operations(operation_id: int, operation_update: OperationEdit,
                                   session: AsyncSession = Depends(get_async_session)):
    current_operation = await session.get(Operation, operation_id)
    if current_operation:
        current_operation.quantity = operation_update.quantity
        current_operation.figi = operation_update.figi
        current_operation.instrument_type = operation_update.instrument_type
        current_operation.type = operation_update.type
        await session.commit()
        return {"message": "Operation updated successfully"}
    raise HTTPException(status_code=404, detail="Operation not found")


@router.patch("/")
async def partial_update_specific_operation(operation_id: int,
                                            operation_update: OperationPartialEdit,
                                            session: AsyncSession = Depends(get_async_session)
                                            ):
    current_operation = await session.get(Operation, operation_id)
    if current_operation:
        if operation_update.quantity is not None:
            current_operation.quantity = operation_update.quantity
        if operation_update.figi is not None:
            current_operation.figi = operation_update.figi
        if operation_update.instrument_type is not None:
            current_operation.instrument_type = operation_update.instrument_type
        if operation_update.type is not None:
            current_operation.type = operation_update.type
        await session.commit()
        return {"message": "Operation updated successfully"}
    raise HTTPException(status_code=404, detail="Operation not found")


@router.delete("/")
async def delete_item(operation_id: int,
                      session: AsyncSession = Depends(get_async_session)):
    current_operation = await session.get(Operation, operation_id)
    if current_operation:
        await session.delete(current_operation)
        await session.commit()
        return {"message": "Operation deleted successfully"}
    raise HTTPException(status_code=404, detail="Operation not found")


@router.get("/long-operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Много данных"


@router.get("/main")
async def main(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(1))
    return result.all()
