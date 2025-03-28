import  json

from models import Ingredient, Plate


# Clase que nos permite trabajar con los datos de prueba
class FoodData:

    # Propiedad que almacenara todos los alimentos
    food = []
    plates = []
    file_food = None

    def __init__(self):
        # Cargar del fichero de datos de prueba
        self.file_food = open("datos/alimentos.json")
        self.food = json.load(self.file_food)
        self.file_food.close()
        file_plates = open('datos/platos.json')
        self.plates = json.load(file_plates)

    # Operacion para buscar ingrediente
    def search_ingredit(self, ingredient_id: int):
        ingredient = None
        ingredient_pos = 0
        for food in self.food["alimentos"]:
            if food["id"] == ingredient_id:
                ingredient = food
                break
            ingredient_pos += 1

        return ingredient_pos, ingredient

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

    # Recibir el nuevo ingrediente y guardarlo
    async def write_ingredient(self, ingredient: Ingredient):
        # Conseguimos el ulitmo id de la lista
        last_food_id = self.food['alimentos'][-1]['id']

        # Incremento el id para el ingrediente nuevo
        ingredient_dict = ingredient.model_dump()
        ingredient_dict['id'] = last_food_id + 1
        self.food["alimentos"].append(ingredient_dict)

        # Escribo en el json el nuevo ingrediente
        with open("datos/alimentos.json", "w", encoding="utf-8") as file_food:
            json.dump(self.food, file_food, indent=2)
        return ingredient_dict

    # Operacion para actualizar un ingrediente
    async def update_ingredient(self, ingredient_id: int, ingredient: Ingredient):

        # ingredient_update = None
        # ingredient_pos = 0
        # for food in self.food["alimentos"]:
        #     if food["id"] == ingredient_id:
        #         ingredient_update = food
        #         break
        #     ingredient_pos += 1

        # Busco el ingrediente para actualizarlo
        ingredient_pos, ingredient_update = self.search_ingredit(ingredient_id)

        # Si existe el ingrediente lo actualizo
        if ingredient_update:
            # Pasamos el modelo a un diccionario
            ingredient_dict = ingredient.model_dump()

            # Recorro cada clave del diccionario
            for elem in ingredient_dict:
                # Si existe valor con la clave, lo actualizo
                if ingredient_dict[elem] is not None:
                    self.food["alimentos"][ingredient_pos][elem] = ingredient_dict[elem]

            # Rescribo el json con el ingrediente actualizdo
            with open("datos/alimentos.json", "w", encoding="utf-8") as file_food:
                json.dump(self.food, file_food, indent=2)
            return self.food["alimentos"][ingredient_pos]
        else:
            return  None

    # Operacion para borrar un ingrediente
    async def delete_ingredient(self, ingredient_id: int):

        # Busco ingrediente para elminarlo
        ingredient_pos, ingredient_delete = self.search_ingredit(ingredient_id)

        if ingredient_delete:
            # Borro ingrediente de la lista
            del self.food["alimentos"][ingredient_pos]
            with open("datos/alimentos.json", "w", encoding="utf-8") as file_food:
                json.dump(self.food, file_food, indent=2)

            return {"status": f"Ingrediente {ingredient_delete['nombre']} borrado correctamente"}
        else:
            return {"status": "Ingrediente no encontrado"}


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

    async def write_plate(self, plate: Plate):
        # Tomo el ultimo id
        last_plate_id = self.plates["platos"][-1]["id"]
        plate_dict = plate.model_dump()
        plate_dict["id"] = last_plate_id + 1

        # Agrego nuevo plato a la lista
        self.plates["platos"].append(plate_dict)

        # Ahora lo escribo en el json
        with open("datos/platos.json", "w", encoding="utf-8") as plate_file:
            json.dump(self.plates, plate_file, indent=2)

        return plate_dict

