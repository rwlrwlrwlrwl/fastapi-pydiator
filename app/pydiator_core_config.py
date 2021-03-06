from app.data.todo.usecases.delete_todo_by_id_data import DeleteTodoByIdDataUseCase, DeleteTodoByIdDataRequest
from app.utils.config import redis_key_prefix, cache_pipeline_is_active, distributed_cache_is_active
from app.utils.client_factory import get_distributed_cache_provider
from app.utils.distributed_cache_provider import DistributedCacheProvider

from pydiator_core.mediatr import pydiator
from pydiator_core.mediatr_container import MediatrContainer
from pydiator_core.pipelines.cache_pipeline import CachePipeline
from pydiator_core.pipelines.log_pipeline import LogPipeline

from app.resources.todo.usecases.get_todo_all import GetTodoAllRequest, GetTodoAllUseCase
from app.resources.todo.usecases.get_todo_by_id import GetTodoByIdRequest, GetTodoByIdUseCase
from app.resources.todo.usecases.add_todo import AddTodoRequest, AddTodoUseCase
from app.resources.todo.usecases.update_todo import UpdateTodoRequest, UpdateTodoUseCase
from app.resources.todo.usecases.delete_todo_by_id import DeleteTodoByIdRequest, DeleteTodoByIdUseCase
from app.resources.todo.notifications.todo_cache_remove_handler import TodoChangeNotification, \
    TodoCacheRemoveNotificationHandler

from app.data.todo.usecases.get_todo_all_data import GetTodoAllDataRequest, GetTodoAllDataUseCase
from app.data.todo.usecases.get_todo_by_id_data import GetTodoByIdDataRequest, GetTodoByIdDataUseCase
from app.data.todo.usecases.add_todo_data import AddTodoDataUseCase, AddTodoDataRequest
from app.data.todo.usecases.update_todo_data import UpdateTodoDataRequest, UpdateTodoDataUseCase

DistributedCacheProvider.key_prefix = redis_key_prefix


def set_up_pydiator():
    container = MediatrContainer()
    container.register_pipeline(LogPipeline())
    if cache_pipeline_is_active is True:
        cache_pipeline = CachePipeline(get_distributed_cache_provider())
        container.register_pipeline(cache_pipeline)

    # Service usecases mapping
    container.register_request(GetTodoAllRequest, GetTodoAllUseCase())
    container.register_request(GetTodoByIdRequest, GetTodoByIdUseCase())
    container.register_request(AddTodoRequest, AddTodoUseCase())
    container.register_request(UpdateTodoRequest, UpdateTodoUseCase())
    container.register_request(DeleteTodoByIdRequest, DeleteTodoByIdUseCase())

    # Data usecases mapping
    container.register_request(GetTodoAllDataRequest, GetTodoAllDataUseCase())
    container.register_request(GetTodoByIdDataRequest, GetTodoByIdDataUseCase())
    container.register_request(AddTodoDataRequest, AddTodoDataUseCase())
    container.register_request(DeleteTodoByIdDataRequest, DeleteTodoByIdDataUseCase())
    container.register_request(UpdateTodoDataRequest, UpdateTodoDataUseCase())

    # Notification mapping
    container.register_notification(TodoChangeNotification, [TodoCacheRemoveNotificationHandler()])

    # Start
    pydiator.ready(container=container)
