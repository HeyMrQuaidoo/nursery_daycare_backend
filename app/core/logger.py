import os
import logging
import functools
from fastapi import Request
from datetime import datetime
from pydantic import BaseModel


from app.core.config import settings


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AppLogger(metaclass=SingletonMeta):
    LOG_DIRECTORY = "logs"
    _logger_initialized = False

    def __init__(self):
        if not AppLogger._logger_initialized:
            self.setup_logger()
            AppLogger._logger_initialized = True

    def setup_logger(self):
        log_directory = AppLogger.LOG_DIRECTORY
        log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
        log_filepath = os.path.join(log_directory, log_filename)
        os.makedirs(log_directory, exist_ok=True)

        logging.basicConfig(
            filename=log_filepath,
            filemode="a",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=settings.LOG_LEVEL,
        )

    @classmethod
    def get_logger(cls):
        return logging.getLogger(__name__)

    @staticmethod
    async def get_body(request: Request):
        if not hasattr(request.state, "body"):
            try:
                request.state.body = await request.json()
            except Exception as e:
                logger = AppLogger.get_logger()
                logger.warning(f"Unable to read request body: {e}")
                request.state.body = None
        return request.state.body

    @staticmethod
    def log_with_method_name(method_name=None):
        def log_decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                if not args:
                    args_list = list(args) + list(kwargs.values())
                    args_list.extend(args)

                body = None
                request_method = None
                logger = AppLogger.get_logger()
                name_to_log = method_name if method_name else func.__name__

                for arg in args_list:
                    if isinstance(arg, Request):
                        request_method = arg.method
                        body = arg.state.json_body
                        break
                    if isinstance(arg, BaseModel):
                        body = arg.model_dump()
                        break

                logger.info(f"{request_method} {name_to_log}, Request Body: {body}")

                try:
                    response = await func(*args, **kwargs)
                    print(type(response))
                    if isinstance(response, list):
                        result = []
                        for r in response:
                            result.append(r.to_dict())
                    else:
                        result = response.to_dict()
                    logger.info(
                        f"{request_method} {name_to_log}, Return JSON: {result}"
                    )
                    return result
                except Exception as e:
                    logger.exception(f"Error in {request_method} {name_to_log}: {e}")
                    raise

            return wrapper

        return log_decorator

    @staticmethod
    def log_decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # check for function arguments
            if not args:
                args_list = list(args) + list(kwargs.values())
            args_list.extend(args)
            body = None
            request_method = None
            logger = AppLogger.get_logger()

            for arg in args_list:
                if isinstance(arg, Request):
                    request_method = arg.method
                    # body = arg.state.json_body
                    break
                if isinstance(arg, BaseModel):
                    body = arg.model_dump()
                    break

            logger.info(f"{request_method} {func.__name__}, Request Body: {body}")

            try:
                result = await func(*args, **kwargs)
                logger.info(f"{request_method} {func.__name__}, Return JSON: {result}")
                return result
            except Exception as e:
                logger.exception(f"Error in {request_method} {func.__name__}: {e}")
                raise

        return wrapper
