import  json

# Clase que nos permite trabajar con los datos de prueba
class FoodData:

    # Propiedad que almacenara todos los alimentos
    alimentos = []

    def __init__(self):
        # Cargar del fichero de datos de prueba
        file = open("datos/alimentos.json")
        self.alimentos = json.load(file)

    # Devolucion asincrona de datos de alimentos
    async def get_ingredientes(self):
        return self.alimentos["alimentos"]

    # Devolucion asincrona de un alimento
    async def get_ingrediente(self, ingrediente_id: int):
        # ingrediente_id: int, hace la conversion a entero, que tambien se hace en el endpoint,
        # ya que en la url se pasa como string
        alimento = None

        # Recorremos todos los datos JSON
        for item in self.alimentos["alimentos"]:
            if item["id"] == ingrediente_id:
                alimento = item
                break

        return alimento
