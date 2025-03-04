import  json

# Clase que nos permite trabajar con los datos de prueba
class FoodData:

    # Propiedad que almacenara todos los alimentos
    food = []
    plates = []

    def __init__(self):
        # Cargar del fichero de datos de prueba
        file_food = open("datos/alimentos.json")
        self.food = json.load(file_food)
        file_plates = open('datos/platos.json')
        self.plates = json.load(file_plates)

# INGREDIENTES
    # Devolucion asincrona de datos de alimentos
    async def get_ingredients(self, skip, total):
        return {'alimentos': self.food['alimentos'][skip:(total+skip)]}

    async def get_all_ingredients(self):
        return self.food["alimentos"]

    # Devolucion asincrona de un alimento
    async def get_ingredient(self, ingrediente_id: int):
        # ingrediente_id: int, hace la conversion a entero, que tambien se hace en el endpoint,
        # ya que en la url se pasa como string
        alimento = None

        # Recorremos todos los datos JSON
        for item in self.food["alimentos"]:
            if item["id"] == ingrediente_id:
                alimento = item
                break

        return alimento

# PLATOS
    # Devolucion asincrona de datos de alimentos
    async def get_plates(self, skip, total):
        return {'platos': self.plates['platos'][skip:(total + skip)]}

    async def get_all_plates(self):
        return self.plates

    # Devolucion asincrona de un alimento
    async def get_plate(self, plate_id: int):
        plate = None
        # Recorremos todos los datos JSON
        for item in self.plates['platos']:
            # Comparamos el id que es int
            if item['id'] == plate_id:
                plate = item
                break
        return plate

    async def get_ingredient_plate(self, plate_id: int, ingredient_id: int):
        plate = await self.get_plate(plate_id)
        ingredient = None
        if plate:
            for item in plate['ingredientes']:
                # Comparamos el id que es int
                if item['id'] == ingredient_id:
                    ingredient = await self.get_ingredient(ingredient_id)
                    break
        return ingredient
