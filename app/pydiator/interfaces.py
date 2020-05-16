from abc import ABC, abstractmethod
import enum
from app.utils.serializer_helper import JsonSerializable


class BaseRequest:
    def __init__(self):
        pass


class BaseNotification:
    def __init__(self):
        pass


class BaseResponse(JsonSerializable):
    def __init__(self):
        pass


class BaseHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def handle(self, req: BaseRequest):
        pass


class BaseNotificationHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def handle(self, notification: BaseNotification):
        pass


class CacheType(enum.Enum):
    NONE = 0
    DISTRIBUTED = 1
    MEMORY = 2


class BaseCacheable(ABC):

    def __init__(self):
        self._no_cache = False

    @abstractmethod
    def get_cache_key(self) -> str:
        pass

    @abstractmethod
    def get_cache_duration(self) -> int:
        pass

    @abstractmethod
    def get_cache_type(self) -> CacheType:
        pass

    @classmethod
    def set_no_cache(cls):
        cls._is_no_cache = True

    @classmethod
    def is_no_cache(cls):
        if hasattr(cls, '_is_no_cache'):
            return cls._is_no_cache
        return False


class BasePipeline(ABC):
    _next = None

    def __init__(self):
        pass

    def next(self) -> object:
        return self._next

    def set_next(self, handler=None):
        self._next = handler

    @abstractmethod
    async def handle(self, req: BaseRequest) -> object:
        pass