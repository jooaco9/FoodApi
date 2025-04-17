from fastapi import FastAPI, Response, status, Body, Query, Path
from typing_extensions import Annotated

from docs import tags_metadata
from food_data import FoodData
from models import Ingredient, Plate

# Objeto para trabajar con los datos de prueba
food = FoodData()

# Objeto app de tipo FastApi
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

# Configuracion del ApiRestFul

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
async def read_ingredient(ingredient_id: Annotated[int, Path(ge=1)], response: Response):
    # await pedir datos
    ingredient = await food.get_ingredient(ingredient_id)
    if ingredient:
        return  ingredient
    else:
        # Si no esta el ingrediente 404
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": str(ingredient_id) + " no encontrado"}

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
async def update_ingredient(ingredient_id: int, ingredient: Ingredient):
    return await food.update_ingredient(ingredient_id, ingredient)


# Endpoints de tipo DELETE, para ingredientes

# Borrar un ingrediente
@app.delete("/ingredientes/{ingredient_id}", tags=["ingredientes"])
async def delete_ingredient(ingredient_id: int):
    return await food.delete_ingredient(ingredient_id)

# Endopoints de tipo GET, para platos

# Devulve el plato segun el id
@app.get("/platos/{plate_id}",tags=["platos"], status_code=status.HTTP_200_OK)
async def read_plate(plate_id: int, response: Response):
    # Buscamos el plato
    plate = await food.get_plate(plate_id)
    #Si encontramos el ingrediente lo devolvemos
    if plate:
        return plate
    #Si el ingrediente es nulo
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": str(plate_id) + " no encontrado"}

# Devuelvo ingrediente de un plato, segun sus ids
@app.get("/platos/{plate_id}/ingredientes/{ingredient_id}",tags=["platos"], status_code=status.HTTP_200_OK)
async def read_plate_ingredient( response: Response, plate_id: int, ingredient_id: int):
    # Buscamos el plato
    ingredient = await food.get_ingredient_plate(plate_id,ingredient_id)
    #Si encontramos el ingrediente lo devolvemos
    if ingredient:
        return ingredient
    #Si el ingrediente es nulo
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "plato " + str(plate_id) + ", "+"ingrediente " + str(ingredient_id) + " no encontrado"}

# Endopoints de tipo POST, para platos

# Agregar un plato
@app.post("/platos", tags=["platos"])
async def write_plates(plate: Plate, time_salient: Annotated[int, Body()]):
    return await food.write_plate(plate, time_salient)
