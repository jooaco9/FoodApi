from fastapi import FastAPI
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

@app.get("/ingredientes", tags=["ingredientes"])
async def read_ingredients():
    # await pedir datos
    return await food.get_ingredientes()

@app.get("/ingredientes/{ingrediente_id}",tags=["ingredientes"])
async def read_ingredient(ingrediente_id: int):
    # await pedir datos
    return await food.get_ingrediente(ingrediente_id)


