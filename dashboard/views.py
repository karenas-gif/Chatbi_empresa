from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg

from .models import *

import json


# 🔐 LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'error': 'Usuario o contraseña incorrectos'
            })

    return render(request, 'login.html')


# 🚪 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# 📊 DASHBOARD (PROTEGIDO)
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# 👤 CLIENTES (PROTEGIDO)
@login_required
def clientes(request):

    mensajes = Conversacion.objects.all().order_by('-id')

    contexto = {
        'mensajes': mensajes,
        'total_hoy': Conversacion.objects.count(),
        'procesando': Conversacion.objects.filter(
            estado='procesando'
        ).count(),

        'procesados': Conversacion.objects.filter(
            estado='recibido'
        ).count()
    }

    return render(
        request,
        'clientes.html',
        contexto
    )


# 💬 CHATS (PROTEGIDO)
@login_required
def chats(request):
    return render(request, 'chats.html')


# ⚙️ CONFIGURACIÓN (PROTEGIDO)
@login_required
def configuracion(request):
    return render(request, 'configuracion.html')


# 📈 ESTADÍSTICAS (PROTEGIDO)
@login_required
def estadisticas(request):
    return render(request, 'estadisticas.html')

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Contacto, Conversacion
import json

@csrf_exempt
def webhook(request):

    VERIFY_TOKEN = "chatbot123"

    # Validación Meta
    if request.method=="GET":

        mode=request.GET.get("hub.mode")
        token=request.GET.get("hub.verify_token")
        challenge=request.GET.get("hub.challenge")

        if mode=="subscribe" and token==VERIFY_TOKEN:
            return HttpResponse(challenge)

        return HttpResponse("Error",status=403)


    # Recibir mensajes reales
    if request.method=="POST":

        try:

            data=json.loads(request.body)

            entry=data["entry"][0]
            changes=entry["changes"][0]
            value=changes["value"]

            if "messages" in value:

                telefono=value["messages"][0]["from"]

                tipo=value["messages"][0]["type"]

                mensaje=""

                if tipo=="text":
                    mensaje=value["messages"][0]["text"]["body"]

                contacto,_=Contacto.objects.get_or_create(
                    telefono=telefono
                )

                Conversacion.objects.create(
                    contacto=contacto,
                    mensaje=mensaje,
                    tipo=tipo,
                    estado="recibido"
                )

            return JsonResponse({
                "status":"ok"
            })

        except Exception as e:

            return JsonResponse({
                "error":str(e)
            })

    return JsonResponse({
        "mensaje":"Webhook activo"
    })

@login_required
def logs(request):

    registros = Conversacion.objects.all().order_by('-fecha')

    return render(
        request,
        'logs.html',
        {
            'registros': registros
        }
    )

from django.http import HttpResponse

def diccionario_datos(request):

    contenido = """
DICCIONARIO DE DATOS

TABLA CONTACTO
- id: Identificador
- telefono: Número WhatsApp
- nombre: Nombre cliente
- fecha_registro: Fecha de creación

TABLA CONVERSACION
- id
- mensaje
- tipo
- estado
- fecha

TABLA SOLICITUD
- id
- servicio
- estado
- fecha

TABLA RESENA
- id
- calificacion
- comentario
- fecha
"""

    response = HttpResponse(
        contenido,
        content_type='text/plain'
    )

    response['Content-Disposition'] = (
        'attachment; filename="diccionario_datos.txt"'
    )

    return response
from django.http import HttpResponse


def descargar_vista(request, nombre):

    contenido = {

        "vista_prospectos_top":
        """
        VISTA: vista_prospectos_top

        Objetivo:
        Mostrar los prospectos más recientes y activos.

        Campos:
        - telefono
        - fecha_registro

        Uso:
        Seguimiento comercial.
        """,

        "vista_servicios_demanda":
        """
        VISTA: vista_servicios_demanda

        Objetivo:
        Mostrar servicios más solicitados.

        Campos:
        - servicio
        - total_solicitudes

        Uso:
        Planeación estratégica.
        """,

        "vista_rendimiento_agentes":
        """
        VISTA: vista_rendimiento_agentes

        Objetivo:
        Medir productividad.

        Indicadores:
        - mensajes atendidos
        - tiempo respuesta
        - satisfacción
        """
    }

    response = HttpResponse(
        contenido.get(nombre, "Documento no encontrado"),
        content_type="text/plain"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{nombre}.txt"'
    )

    return response