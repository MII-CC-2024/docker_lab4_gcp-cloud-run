# Docker: python y Flask (Hola Mundo) en GCP Cloud Run


## Crea la aplicación

Crea un entorno virtual, actívalo, instala Flask y desarrolla tu aplicación.
(aquí no se muestran estos pasos, partimos de la aplicación ya desarrollada y las librerías necesarias indicadas en el fichero requirements.txt)


Aplicación: web.py:

```python

# file web.py

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET'])
def saluda():
    return render_template('index.html', msg="Hola Mundo!")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)


```

Vista: templates/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Web App</title>
    <link rel= "stylesheet" type= "text/css" href= "{{ url_for('static',filename='css/main.css') }}" />
</head>
<body>
    <h1> {{ msg }}</h1>
    <img src="{{ url_for('static',filename='img/logo.png') }}" />
</body>
</html>
```

Estilo: css/main.css

```css
h1 {
    color: red;
}
```

Imagen: img/logo.png


Prueba la aplicación en local


```shell
$ python3 web.py
```



## Contruir la imagen

Crea el fichero Dockerfile

```dockerfile

FROM python:3.10-alpine

WORKDIR /app

EXPOSE 8080

COPY ./app .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./web.py" ]

```

Construye la imagem

```shell
$ docker build --tag jluisalvarez/hm-flask:2024 .
```

Prueba la imagen en local

```shell
$ docker run -d --name hmflask -p 8080:8080 jluisalvarez/hm-flask:2024
```

Sube la imagen a Docker Hub

```shell
$ docker login

...

$ docker push jluisalvarez/hm-flask:2024

```

# Despliega en GCP Cloud Run

En la consola web de GCP, selecciona Cloud Run en la sección Serveless.


Selecciona crear servicio "Create Service" y marca "Deploy one revision from an existing container image"

En "Container image URL" introduce la imagen, por ejemplo, jluisalvarez/hm-flask:2024.

En "Name Service" introduce el nombre, por ejemplo, hm-flask y selecciona la región, por ejemplo, europe-southwest1 (Madrid).


En Authentication, marca la opción "Allow unauthenticated invocations" (Check this if you are creating a public API or website)

En "CPU allocation and pricing" marca "CPU is only allocated during request processing"

En "Service autoscaling", introduce en Minimum number of instances: 0 y en "Ingress control" selecciona All (Allow direct access to your service from the interne).

Revisa los valores de las secciones Container, Networking, Security; 
asegúrate que en Container el puerto coincide con el que expone la aplicación, selecciona la CPU y Memoria deseada y el entorno por defecto.

El resto de las opciones puedes dejarlas por defecto y pulsar en Crear.

Cuando se complete la acción, podrás acceder al contenedor con la URL del tipo https://hm-flask-xxxxxxxxxx-no.a.run.app/

