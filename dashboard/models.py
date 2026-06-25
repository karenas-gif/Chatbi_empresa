from django.db import models


class Contacto(models.Model):

    telefono=models.CharField(max_length=20)

    nombre=models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    fecha_registro=models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.telefono


class Conversacion(models.Model):

    contacto=models.ForeignKey(
        Contacto,
        on_delete=models.CASCADE
    )

    mensaje=models.TextField()

    tipo=models.CharField(
        max_length=50
    )

    estado=models.CharField(
        max_length=50
    )

    fecha=models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.mensaje


class Solicitud(models.Model):

    contacto=models.ForeignKey(
        Contacto,
        on_delete=models.CASCADE
    )

    servicio=models.CharField(
        max_length=100
    )

    estado=models.CharField(
        max_length=50
    )

    fecha=models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.servicio
    
class Resena(models.Model):

    contacto = models.ForeignKey(
        Contacto,
        on_delete=models.CASCADE
    )

    calificacion = models.IntegerField()

    comentario = models.TextField()

    fecha = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dashboard_resenas'


class Alerta(models.Model):

    mensaje = models.TextField()

    tipo = models.CharField(max_length=100)

    estado = models.CharField(max_length=50)

    fecha = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dashboard_alertas'