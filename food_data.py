import  json

# Clase que nos permite trabajar con los datos de prueba
class FoodData:

    # Propiedad que almacenara todos los alimentos
    food = []

    def __init__(self):
        # Cargar del fichero de datos de prueba
        file = open("datos/alimentos.json")
        self.food = json.load(file)

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
