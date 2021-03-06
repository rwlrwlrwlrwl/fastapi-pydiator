from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from pydiator_core.mediatr import pydiator
from app.data.todo.usecases.get_todo_by_id_data import GetTodoByIdDataRequest


class GetTodoByIdRequest(BaseModel, BaseRequest):
    id: int = Field(0, gt=0, description="The item id be greater than zero")


class GetTodoByIdResponse(BaseModel, BaseResponse):
    id: int = Field(...)
    title: str = Field(...)


class GetTodoByIdUseCase(BaseHandler):

    async def handle(self, req: GetTodoByIdRequest) -> GetTodoByIdResponse:
        todo_data = await pydiator.send(GetTodoByIdDataRequest(id=req.id))
        if todo_data is not None:
            return GetTodoByIdResponse(id=todo_data.id, title=todo_data.title)

        return None
