from pydantic import BaseModel

# Modelo Ingrediente
class Ingredient(BaseModel):
    nombre: str
    calorias: int | None = None # Opcional
    carbohidratos: float | None = None # Opcional
    proteinas: float | None = None # Opcional
    fibra: float | None = None  # Opcional
    grasas: float | None = None # Opcional

# Modelo para los ingredientes guardados en cada plato
class IngredientPlate(BaseModel):
    id: int
    cant: int
    ud: str

# Modelo Plato
class Plate(BaseModel):
    nombre: str
    tipo: str
    ingredientes: list[IngredientPlate]