import json
import logging
import logging.config
import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


def setup_loggers(filename: str):
    with open(filename, "r") as f:
        config = json.load(f)

    logging.config.dictConfig(config)


class LoggingMiddleware(BaseHTTPMiddleware):
    logger = logging.getLogger("request_logger")
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response: Response = await call_next(request)
        process_time = time.perf_counter() - start_time

        log_data = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": process_time,
        }
        self.logger.info("Request", extra=log_data)
        return response
