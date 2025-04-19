import uvicorn
from fastapi import FastAPI, Response, status, Body, Query, Path, HTTPException
from typing_extensions import Annotated
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from docs import tags_metadata
from food_data import FoodData
from typing import Any
from models import Ingredient, Plate, User, UserOut

# Objeto para trabajar con los datos de prueba
food = FoodData()

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

# Definicion de los ENDPOINTS

# Endopoints de tipo GET, para ingredientes
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Devuleve todos los ingredientes
@app.get("/ingredientes", tags=["ingredientes"], status_code=status.HTTP_200_OK)
async def read_ingredients(skip: int=0, total: int=10, all_ingredients: bool | None = None,
                           name_filter: Annotated[str | None, Query(min_length=3, max_length=10)] = None):
    # los query parameters se ponen directamente en la funcion que se llama para el endpoint definido
    # skipt y int se ponen en la url, /ingredientes/?skip=x&total=y, se pueden no poner o poner solo uno de los dos tambien

    # para definir query parameters opcionales se pone | None = None y si quiero poner uno obligatorio saco el valor
    # por defecto y se pone al principio
    # await pedir datos
    if not all_ingredients:
        return await food.get_ingredients(skip, total, name_filter)
    else:
        return await food.get_all_ingredients()

# Devuelve un ingredinte segun id
# Como default ponemos status 200
@app.get("/ingredientes/{ingredient_id}",tags=["ingredientes"], status_code=status.HTTP_200_OK)
async def read_ingredient(ingredient_id: Annotated[int, Path(ge=1)]):
    # await pedir datos
    ingredient = await food.get_ingredient(ingredient_id)

    if not ingredient:
        raise HTTPException(status_code=404, detail=f"Ingrediente {str(ingredient_id)} no encontrado")

    return ingredient

# Endpoints de tipo POST, para ingredientes

# Agregar un ignrediente
@app.post("/ingredientes", tags=["ingredientes"])
async def write_ingredients(ingredient: Ingredient):
    return await food.write_ingredient(ingredient)

@app.post("/ingredientes_platos", tags=["ingredientes"])
async def write_ingredients_plates(ingredient: Ingredient, plate: Plate):
    return await food.write_ingredient_plate(ingredient, plate)

# Endopints de tipo PUT, para ingredientes

# Modificar un ingrediente
@app.put("/ingredientes/{ingredient_id}", tags=["ingredientes"])
async def update_ingredient(ingredient_id: Annotated[int, Path(ge=1)], ingredient: Ingredient):
    return await food.update_ingredient(ingredient_id, ingredient)


# Endpoints de tipo DELETE, para ingredientes

# Borrar un ingrediente
@app.delete("/ingredientes/{ingredient_id}", tags=["ingredientes"])
async def delete_ingredient(ingredient_id: Annotated[int, Path(ge=1)]):
    return await food.delete_ingredient(ingredient_id)

# Endopoints de tipo GET, para platos

# Devulve el plato segun el id
@app.get("/platos/{plate_id}",tags=["platos"], status_code=status.HTTP_200_OK)
async def read_plate(plate_id: Annotated[int, Path(ge=1)]):
    # Buscamos el plato
    plate = await food.get_plate(plate_id)

    # Si no se encuentra el plato, devolvemos 404
    if not plate:
        raise HTTPException(status_code=404, detail="Plato " + str(plate_id) + " no encontrado")

    return plate

# Devuelvo ingrediente de un plato, segun sus ids
@app.get("/platos/{plate_id}/ingredientes/{ingredient_id}",tags=["platos"], status_code=status.HTTP_200_OK)
async def read_plate_ingredient( response: Response, plate_id: Annotated[int, Path(ge=1)], ingredient_id: Annotated[int, Path(ge=1)]):
    # Buscamos el plato
    ingredient = await food.get_ingredient_plate(plate_id,ingredient_id)

    # Si no esta el ingrediente 404
    if not ingredient:
        raise HTTPException(status_code=404, detail="Plato " + str(plate_id) + ", ingrediente " + str(ingredient_id) + " no encontrado")

    return ingredient

# Endopoints de tipo POST, para platos

# Agregar un plato
@app.post("/platos", tags=["platos"])
async def write_plates(plate: Plate, time_salient: Annotated[int, Body()]):
    return await food.write_plate(plate, time_salient)


# USUARIOS

# Con -> Any, hacemos que devuelva el modelo que pongo en response_model, por mas que lo que devuelve
# write_user es un User, nosotros devolvemos el UserOut que no tiene la password
@app.post("/usuarios", response_model=UserOut, tags=['usuarios'])
async def write_user(usr: User) -> Any:
    return await food.write_user(usr)






# if __name__ == "__main__":
#     # Esto es para usar el debug y correrlo desde pycharm y no hacer el uvicorn por fuera
#     uvicorn.run(app, host="0.0.0.0", port=8000)