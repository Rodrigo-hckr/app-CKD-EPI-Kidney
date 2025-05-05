import re
import numpy as np
from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])

def calcular():
    if request.method == "POST":
        creatinina = float(request.form["creatinina"])
        edad = int(request.form["edad"])
        sexo = request.form["sexo"]
        raza = request.form["raza"]
        
        tfg = calcular_tfg(creatinina, edad, sexo, raza)
        estadio = determinar_estadio_erc(tfg)
        color_tfg = determinar_color_tfg(tfg)
        
        return render_template("resultado.html", tfg=tfg, estadio=estadio, color_tfg=color_tfg)
    
    return render_template("index.html")



def calcular_tfg(creatinina, edad, sexo, raza):
    kappa = 0.7 if sexo == "Mujer" else 0.9
    alpha = -0.241 if sexo == "Mujer" else -0.302
    
    tfg = 142 * min(creatinina /kappa, 1) ** alpha * max(creatinina / kappa ,1 ) ** -1.200
    tfg *= 0.9938 ** edad
    if sexo == "Mujer":
        tfg *= 1.012
    if raza == "Afrodescendiente":
        tfg *= 1.159
    return round(tfg, 2)   

def determinar_estadio_erc(tfg):
    if tfg >= 90:
        return "Estadio 1 - Función renal normal"
    elif tfg >= 60:
        return "Estadio 2 - Ligeramente disminuido \n Recomendación - Asegurate de beber Suficiente agua natural "
    elif tfg >= 45:
        return "Estadio 3a - Disminución leve de la función renal \n Recomendación - Evita alimentos ultra procesados"
    elif tfg >= 30:
        return "Estadio 3b - Disminución moderada de la función renal \n Recomendación - Disminuye el consumo de alimentos de origen animal"
    elif tfg >= 15:
        return "Estadio 4 - Reducción severa de la funcion renal \n  Recomendación - Visita a tu Nefrólogo y Nutriólogo renal"
    else:
        return "Estadio 5 - Fallo renal \n Recomendación - Visita a tu Nefrólogo y Nutriólogo renal"
    
def determinar_color_tfg(tfg):
     if tfg > 60: 
         return "#60b7fe"
     elif tfg > 30: 
         return "#ef6502"
     else:
         return "#c54f02"   

if __name__ == "__main__":
    port = int(os.environ.get("PORT",  10000))
    app.run(host="0.0.0.0", port=port)         