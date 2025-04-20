from pydantic import BaseModel, Field
from enum import Enum

# Enum para el tipo de plato
class PlateType(str, Enum):
    incoming = "entrante"
    main = "principal"
    dessert = "postre"
    drink = "bebida"

# Modelo Ingrediente
class Ingredient(BaseModel):
    nombre: str
    calorias: int | None = Field(default=None, gt=0, description="Calorias del ingrediente. Entero mayor que 0") # Opcional
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
    nombre: str = Field(description="Nombre del plato", max_length=128) # Con Field agregamos documentacion
    tipo: PlateType
    ingredientes: list[IngredientPlate]

# Modelo para los usuarios
class User(BaseModel):
    nombre: str
    apellidos: str
    email: str
    password: str

class UserOut(BaseModel):
    nombre: str
    apellidos: str
    email: str