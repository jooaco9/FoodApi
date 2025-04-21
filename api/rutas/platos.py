from fastapi import APIRouter

from fastapi import Response, status, Body, Path, HTTPException
from typing_extensions import Annotated

from api import Plate, FoodData

food = FoodData()

router = APIRouter()

# Devulve el plato segun el id
@router.get("/{plate_id}", status_code=status.HTTP_200_OK)
async def read_plate(plate_id: Annotated[int, Path(ge=1)]):
    # Buscamos el plato
    plate = await food.get_plate(plate_id)

    # Si no se encuentra el plato, devolvemos 404
    if not plate:
        raise HTTPException(status_code=404, detail="Plato " + str(plate_id) + " no encontrado")

    return plate

# Devuelvo ingrediente de un plato, segun sus ids
@router.get("/{plate_id}/ingredientes/{ingredient_id}", status_code=status.HTTP_200_OK)
async def read_plate_ingredient( response: Response, plate_id: Annotated[int, Path(ge=1)], ingredient_id: Annotated[int, Path(ge=1)]):
    # Buscamos el plato
    ingredient = await food.get_ingredient_plate(plate_id,ingredient_id)

    # Si no esta el ingrediente 404
    if not ingredient:
        raise HTTPException(status_code=404, detail="Plato " + str(plate_id) + ", ingrediente " + str(ingredient_id) + " no encontrado")

    return ingredient

# Endopoints de tipo POST, para platos

# Agregar un plato
@router.post("")
async def write_plates(plate: Plate, time_salient: Annotated[int, Body()]):
    return await food.write_plate(plate, time_salient)