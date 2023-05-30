import threading
from asgiref.sync import sync_to_async
import asyncio
from django.shortcuts import render
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from jinja2 import Template
import webbrowser
from .models import Empresa
import tempfile


# Obtiene la ruta absoluta al directorio actual
current_directory = os.path.dirname(os.path.abspath(__file__))



# Create your views here.
# Input parameter: a request object that contains information about the incoming HTTP request.
# Output: renders a HTML template named home.html using the render() function provided by the Django framework.

def home(request):
    return render(request, 'app/home.html')


def dashboard(request):
    return render(request, 'app/dashboard.html')


def register(request):

    form = UserCreationForm(request.POST)
    if request.method == "POST":
         if form.is_valid():
            username = form.cleaned_data["username"]
            messages.success(request, f"Usuario {username}  creado exitosamente")
            form.save()
            return redirect("home")
    else:
        form = UserCreationForm()
    context = {"form": form}
    return render(request, "app/register.html", context)


def generar_grafico(X, probabilidades, temp_file):
    # Crea un gráfico XY utilizando Matplotlib
    plt.scatter(X.reshape(-1), probabilidades,
                label='Predicción de probabilidad')
    plt.xlabel('Ponderación de calificación')
    plt.ylabel('Probabilidad de alto riesgo')
    plt.legend()

    # Guarda el gráfico en el archivo temporal
    plt.savefig(temp_file)

def prediccion_probabilidad(request):
    # Obtén los datos de las empresas de la base de datos
    empresas = [
        {"nombre": "Empresa 1", "sector": "Automotriz", "calificador_riesgo": "Alto",
            "tipo_riesgo": "Financiero", "ponderacion_calificacion": 0.75, "alto_riesgo": True},
        {"nombre": "Empresa 2", "sector": "Tecnología", "calificador_riesgo": "Bajo",
            "tipo_riesgo": "Operativo", "ponderacion_calificacion": 0.35, "alto_riesgo": False},
        {"nombre": "Empresa 3", "sector": "Alimentos", "calificador_riesgo": "Medio",
            "tipo_riesgo": "Reputacional", "ponderacion_calificacion": 0.60, "alto_riesgo": False},
        {"nombre": "Empresa 4", "sector": "Energía", "calificador_riesgo": "Alto",
            "tipo_riesgo": "Operativo", "ponderacion_calificacion": 0.80, "alto_riesgo": True},
        {"nombre": "Empresa 5", "sector": "Finanzas", "calificador_riesgo": "Medio",
            "tipo_riesgo": "Financiero", "ponderacion_calificacion": 0.55, "alto_riesgo": False},
    ]

    # Crea y guarda los objetos Empresa en la base de datos
    for data in empresas:
        empresa = Empresa(
            nombre=data["nombre"],
            sector=data["sector"],
            calificador_riesgo=data["calificador_riesgo"],
            tipo_riesgo=data["tipo_riesgo"],
            ponderacion_calificacion=data["ponderacion_calificacion"],
            alto_riesgo=data["alto_riesgo"])
        empresa.save()

    # Obtén las características (X) y las etiquetas (y) de los datos
    empresas_db = Empresa.objects.all()
    X = np.array(
        [empresa.ponderacion_calificacion for empresa in empresas_db]).reshape(-1, 1)
    y = np.array([empresa.alto_riesgo for empresa in empresas_db])

    # Crea y entrena el modelo de regresión logística
    modelo = LogisticRegression()
    modelo.fit(X, y)

    # Realiza predicciones de probabilidad utilizando el modelo entrenado
    # Probabilidad de clase positiva (alto riesgo)
    probabilidades = modelo.predict_proba(X)[:, 1]

   # Crea un directorio temporal
    temp_dir = tempfile.mkdtemp()

    # Genera el nombre de archivo para el gráfico
    file_name = 'temporal.png'

    # Genera la ruta completa al archivo utilizando el MEDIA_ROOT
    temp_file = os.path.join(settings.MEDIA_ROOT, file_name)

    # Ejecuta la generación del gráfico en un hilo separado
    thread = threading.Thread(target=generar_grafico,
                              args=(X, probabilidades, temp_file))
    thread.start()
    thread.join()

    # Renderiza la plantilla HTML con la ruta del gráfico
    return render(request, 'app/model.html', {'imagen': settings.MEDIA_URL + file_name})










