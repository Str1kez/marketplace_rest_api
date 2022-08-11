import aioredis
import uvicorn
from uvicorn.config import LOGGING_CONFIG
from fastapi import FastAPI, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app import __version__
from app.config import settings
from app.db.models import db
from app.misc.exceptions import CustomValidationError
from app.routers import imports_router, delete_router, nodes_router


app = FastAPI(title='Marketplace API',
              version=__version__,
              debug=settings.debug)

app.include_router(router=imports_router)
app.include_router(router=delete_router)
app.include_router(router=nodes_router)


if not settings.debug:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Validation Failed"
        })

    @app.exception_handler(CustomValidationError)
    async def bad_request_exception_handler(request: Request, exc):
        return await validation_exception_handler(request, exc)


    @app.exception_handler(status.HTTP_404_NOT_FOUND)
    async def not_found_exception_handler(request: Request, exc):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Item not found"
        })


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(settings.redis_dsn, encoding="utf8",
                        decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='marketplace-api-cache')
    db.init_app(app)


def main():
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    uvicorn.run('app.main:app', host=settings.host, port=settings.port, reload=True, debug=settings.debug)


if __name__ == '__main__':
    main()
