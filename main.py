from fastapi import FastAPI

# tag para poder agregar conjuntos en la documentacion
tags_metadata = [
    {
        "name": "ingredientes",
        "description": "Opercaiones relacionadas con el CRUD de ingredientes"
    }
]

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
def read_ingredients():
    return {"Objeto": "Ingredientes"}

