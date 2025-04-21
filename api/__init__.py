from api.datos.food_data import FoodData
from api.utilidades.models import Ingredient, Plate, User, UserOut
from api.utilidades.docs import tags_metadata
from api.rutas.platos import router as platos_rutas
from api.rutas.ingredientes import router as ingredientes_rutas
from api.rutas.usuarios import router as usuarios_rutas