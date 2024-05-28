from lib.http.router import Route
from app.http.controllers.home import Homecontroller

"""Ruta Base Publica"""
Route().group(
    Route.get("/", [Homecontroller, 'index'])
)