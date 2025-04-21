from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from api import platos_rutas, ingredientes_rutas, usuarios_rutas
from api import tags_metadata

# Objeto app de tipo FastApi
# Configuracion del ApiRestFul
app = FastAPI(
    title="FoodApi",
    description="ApiRestFul para la gestion de alimentos y planes nutricionales",
    version="0.0.2",
    contact= {
        "name": "Joaquin Corbo",
        "url": "https://x.com/9_jokin",
        "email": "joaquin.corbo9@gmail.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    openapi_tags=tags_metadata
)

# Manejo de EXCEPCIONES

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"error": exc.detail})
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    # Conversion dict
    error_dict = eval(str(exc))

    if error_dict[0]['type'] == "greater_than_equal":
        code_error = 422
    else:
        code_error = 404
    return JSONResponse(
        status_code=code_error,
        content=jsonable_encoder(
            {
                "error": error_dict[0]["msg"],
                "dato_enviado": error_dict[0]['input']
            }
        )
    )

# DEFAULT
@app.get("/")
def read_root():
    return {"Hola": "Jokin"}

# INGREDIENTES
app.include_router(
    ingredientes_rutas,
    tags=['ingredientes'],
    prefix='/ingredientes'
)

# PLATOS
app.include_router(
    platos_rutas,
    tags=['platos'],
    prefix='/platos'
)

# USUARIOS
app.include_router(
    router=usuarios_rutas,
    tags=['usuarios'],
    prefix='/usuarios'
)
