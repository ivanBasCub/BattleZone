from django.db import models

# Creamos las siguientes dos tablas que se usaran para las dos aplicaciones
    # Tabla de los niveles de dificultad
class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} - {self.name}"
    
    # Tabla con la lista de videojuegos
class VideoGame(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} - {self.name}"
