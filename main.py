from fastapi import FastAPI, Response, status
from docs import tags_metadata
from food_data import FoodData

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

# Endopoint GET /
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/ingredientes", tags=["ingredientes"], status_code=status.HTTP_200_OK)
async def read_ingredients():
    # await pedir datos
    return await food.get_ingredientes()

# Como default ponemos status 200
@app.get("/ingredientes/{ingrediente_id}",tags=["ingredientes"], status_code=status.HTTP_200_OK)
async def read_ingredient(ingrediente_id: int, response: Response):
    # await pedir datos
    ingrediente = await food.get_ingrediente(ingrediente_id)
    if ingrediente:
        return  ingrediente
    else:
        # Si no esta el ingrediente 404
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": str(ingrediente_id) + " no encontrado"}



