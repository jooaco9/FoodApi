import json
import bcrypt
import os

from api.utilidades.models import Ingredient, Plate, User


# Clase que nos permite trabajar con los datos de prueba
class FoodData:

    # Propiedad que almacenara todos los datos
    food = []
    plates = []
    salients = []
    users = []
    work_dir = None

    def __init__(self):
        self.work_dir = os.getcwd()
        self.work_dir = self.work_dir + "\\api\\datos\\"
        # Cargar del fichero de datos de prueba
        file_food = open(self.work_dir +"alimentos.json")
        self.food = json.load(file_food)
        file_plates = open(self.work_dir +'platos.json')
        self.plates = json.load(file_plates)
        file_salients = open(self.work_dir +'destacados.json')
        self.salients = json.load(file_salients)
        file_users = open(self.work_dir +'usuarios.json')
        self.users = json.load(file_users)


# USUARIOS

    async def write_user(self, usr: User):

        # Tomo el ultimo id
        last_user_id = self.users['usuarios'][-1]['id']
        user_dict = usr.model_dump()
        user_dict['id'] = last_user_id + 1

        # Hash del password
        salt = bcrypt.gensalt()
        user_dict["password"] = bcrypt.hashpw(user_dict["password"].encode('utf-8'), salt).decode('utf-8')

        # Agregamos el usuario a la lista
        self.users["usuarios"].append(user_dict)
        with open(self.work_dir + "usuarios.json", "w", encoding="utf-8") as file_users:
            json.dump(self.users, file_users, indent=2)

        return user_dict


# INGREDIENTES

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

    # Devolucion asincrona de datos de alimentos
    async def get_ingredients(self, skip, total, name_filter):
        foods = self.food['alimentos'][skip:(total + skip)]

        # Si hay filtro, lo filtramos
        if name_filter:
            food_filter = [food for food in foods if name_filter in food["nombre"]]
            return {'alimentos': food_filter}

        # Si no hay filto, devolvemos con skip y total
        return {'alimentos': foods}

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
        with open(self.work_dir + "alimentos.json", "w", encoding="utf-8") as file_food:
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
            with open(self.work_dir + "alimentos.json", "w", encoding="utf-8") as file_food:
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
            with open(self.work_dir + "alimentos.json", "w", encoding="utf-8") as file_food:
                json.dump(self.food, file_food, indent=2)

            return {"status": f"Ingrediente {ingredient_delete['nombre']} borrado correctamente"}
        else:
            return {"status": "Ingrediente no encontrado"}

    async def write_ingredient_plate(self, ingredient: Ingredient, plate: Plate):
        ingredient = await self.write_ingredient(ingredient)

        # Serealizamos para añadir id
        plate_dict = plate.model_dump()
        plate_dict['ingredientes'][0]['id'] = ingredient['id']
        plate_ingredient_id = plate.model_validate(plate_dict)
        plate_dict = await self.write_plate(plate_ingredient_id)

        return dict([('ingrediente', ingredient), ('plate', plate_dict)])


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

    async def write_plate(self, plate: Plate, time_salient: int):
        # Tomo el ultimo id
        last_plate_id = self.plates["platos"][-1]["id"]
        plate_dict = plate.model_dump()
        plate_dict["id"] = last_plate_id + 1

        # Agrego nuevo plato a la lista
        self.plates["platos"].append(plate_dict)

        # Ahora lo escribo en el json
        with open(self.work_dir + "platos.json", "w", encoding="utf-8") as plate_file:
            json.dump(self.plates, plate_file, indent=2)

        salient_dict = await self.write_salient(plate_dict, time_salient)

        return dict([('plato', plate_dict), ('destacado', salient_dict)])

# DESTACADOS
    # Agregar un plato destacado
    async def write_salient(self, plate: Plate, time_salient: int):
        # Tomo el ultimo id de los destacados
        last_salient_id = self.salients["destacados"][-1]['id']

        # Plato nuevo destacados
        plate_salient = {
            "id": last_salient_id + 1,
            "id_plato": plate['id'],
            "tiempo": time_salient
        }

        self.salients["destacados"].append(plate_salient)

        with open(self.work_dir + 'destacados.json', 'w', encoding="utf-8") as salient_file:
            json.dump(self.salients, salient_file, indent=2)

        return plate_salient



