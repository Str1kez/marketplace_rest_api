import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import __version__
from app.config import settings
from app.db.models import db
from app.exceptions import CustomValidationError
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
    db.init_app(app)


def main():
    uvicorn.run('app.main:app', host=settings.host, port=settings.port, reload=True, debug=settings.debug)


if __name__ == '__main__':
    main()
