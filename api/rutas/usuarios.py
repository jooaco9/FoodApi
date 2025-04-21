from fastapi import APIRouter, BackgroundTasks
from typing import Any

from api import FoodData, UserOut, User

food = FoodData()

router = APIRouter()

def send_fake_email(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

# Con -> Any, hacemos que devuelva el modelo que pongo en response_model, por mas que lo que devuelve
# write_user es un User, nosotros devolvemos el UserOut que no tiene la password
@router.post("", response_model=UserOut, tags=['usuarios'])
async def write_user(usr: User, background_tasks: BackgroundTasks) -> Any:
    # La background task no influye en la respuesta, se hace cuando puede, se ejecuta en el background
    background_tasks.add_task(send_fake_email, usr.email, message="Nuestro primer correo fake")
    return await food.write_user(usr)