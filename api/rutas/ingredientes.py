from fastapi import APIRouter

from fastapi import status, Path, HTTPException, Query
from typing_extensions import Annotated

from api import Plate, FoodData, Ingredient

food = FoodData()

router = APIRouter()

# Devuleve todos los ingredientes
@router.get("", status_code=status.HTTP_200_OK)
async def read_ingredients(skip: Annotated[int,
                                 Query(description="Cantidad de ingredientes a saltar")] = 0,
                           total: Annotated[int,
                                  Query(description="Total de ingredientes a devolver")] = 10,
                           all_ingredients: Annotated[bool | None,
                                            Query(description="Se muestran todos los ingredientes")] = None,
                           name_filter: Annotated[str | None,
                                        Query(
                                            description="Filtro de busqueda",
                                            min_length=3,
                                            max_length=10
                                        )] = None):
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
@router.get("/{ingredient_id}", status_code=status.HTTP_200_OK,
         summary="Buscar Ingrediente",
         description="Buscar ingrediente a traves del ingredient_id"
         )
async def read_ingredient(ingredient_id: Annotated[int, Path(description="Id entero de busqueda" ,ge=1)]):
    # await pedir datos
    ingredient = await food.get_ingredient(ingredient_id)

    if not ingredient:
        raise HTTPException(status_code=404, detail=f"Ingrediente {str(ingredient_id)} no encontrado")

    return ingredient

# Endpoints de tipo POST, para ingredientes

# Agregar un ignrediente
@router.post("")
async def write_ingredients(ingredient: Ingredient):
    return await food.write_ingredient(ingredient)

@router.post("/ingredientes_platos")
async def write_ingredients_plates(ingredient: Ingredient, plate: Plate):
    return await food.write_ingredient_plate(ingredient, plate)

# Endopints de tipo PUT, para ingredientes

# Modificar un ingrediente
@router.put("/{ingredient_id}")
async def update_ingredient(ingredient_id: Annotated[int, Path(ge=1)], ingredient: Ingredient):
    return await food.update_ingredient(ingredient_id, ingredient)


# Endpoints de tipo DELETE, para ingredientes

# Borrar un ingrediente
@router.delete("/{ingredient_id}")
async def delete_ingredient(ingredient_id: Annotated[int, Path(ge=1)]):
    return await food.delete_ingredient(ingredient_id)