# FoodApi

ApiRestFul para la gestión de alimentos y planes nutricionales desarrollada con FastAPI y Python.

> **Nota**: Este es un proyecto en progreso y actualmente no está terminado. Se están desarrollando nuevas características y mejoras.

## Descripción

FoodApi es un proyecto de API REST desarrollado con fines de aprendizaje. Proporciona endpoints para gestionar ingredientes y platos, implementando operaciones CRUD (Crear, Leer, Actualizar, Eliminar) a través de métodos HTTP (GET, POST, PUT, DELETE).

La API permite a los usuarios:
- Crear, leer, actualizar y eliminar ingredientes
- Crear y leer platos
- Asociar ingredientes con platos
- Obtener información detallada sobre ingredientes en un plato específico

## Características

- Operaciones CRUD completas para ingredientes
- Creación y consulta de platos
- Opciones de filtrado mediante parámetros de consulta
- Manejo adecuado de errores con códigos de estado HTTP
- Documentación completa de la API con Swagger/OpenAPI

## Tecnologías utilizadas

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno y rápido para construir APIs
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Validación de datos y gestión de configuraciones
- [JSON](https://www.json.org/) - Formato de almacenamiento de datos

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/jooaco9/FoodApi.git
cd FoodApi
```

2. Crear un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar la aplicación:
```bash
uvicorn main:app --reload
```

La API estará disponible en http://localhost:8000

## Documentación de la API

Una vez que el servidor esté en funcionamiento, puedes acceder a la documentación interactiva automática de la API en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estructura del proyecto

- `main.py` - Archivo principal de la aplicación con las rutas de FastAPI
- `models.py` - Modelos Pydantic para la validación de datos
- `food_data.py` - Clase de gestión de datos para ingredientes y platos
- `docs.py` - Configuración de la documentación de la API
- `datos/` - Directorio que contiene archivos JSON con datos de prueba

## Estado del proyecto

Este proyecto está en desarrollo activo. Se están implementando nuevas funcionalidades y mejorando las existentes. No se considera una versión final y pueden producirse cambios significativos.

## Contacto

- Joaquín Corbo - [@9_jokin](https://x.com/9_jokin)
- Correo electrónico: joaquin.corbo9@gmail.com
