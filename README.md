# Servicio de Detección de Entidades
El repositorio implementa un servicio para la detección de entidades utilizando [spaCy](https://spacy.io)

## Instrucciones para el despliegue

### Stack de tecnologías
- Linux
- Docker
- Flask
- Gunicorn
  
### Instrucciones para el despliegue (desarrollo)
El servicio ha sido implementado utilizando contenedores Docker en Visual Studio Code, ver carpeta `.devcontainer`
  
### Instrucciones para el despliegue (API)
Se implementa mediante `docker-compose`. El contenedor despliega un servicio que gestiona el servidor `gunicorn` para lanzarlo si ocurre alguna caida, etc. Ver archivos y carpetas dentro de  `./docker`


#### API

Se implementa un único servicio descrito a continuación.

#### Servicio `sensors/ner`


### Interfaz REQUEST

El servicio espera un JSON con el siguiente formato, se verifica que el request tenga los campos obligatorios ("documents") y que cada documento tenga "id" y "text", en caso contrario falla.

```json
{
  "documents": [
    {
      "id": "unique document id 1",
      "text": "text to analyze",
      "lang": "language of the text [es|en]"
    },
    {
      "id": "unique document id n",
      "text": "ext to analyze",
      "lang": "language of the text [es|en]"
    }
  ],
  "pretty": "(may be empty, only key is important"
}
```

En el header, debe ir un token (key) de identificación, ej. 

```json
{
  "Content-type": "application/json",
  "key": "XXXXXXXXXXXXXXXXXXXX"
}
```
  

### Interfaz RESPONSE

Es un JSON, con la siguiente estructura:

```json
{
  "documents_analized": [
    {
      "id": "unique document id 1",
      "entities": [
        {
          "name": "entity 1 name",
          "type": "entity type",
          "score": "score of the detection",
          "gloss": "description of the entity type"
        },
        {
          "name": "entity n name",
          "type": "entity type",
          "score": "score of the detection",
          "gloss": "description of the entity type"
        }
      ]
    },
    {
      "id": "unique document id n",
      "entities": []
    }
  ]
}
```
  

### Ejemplo Request
```json
{
  "documents": [
    {
      "id": 1,
      "text": "Apple planea comprar una startup en U.K. por 12 millones de euros pero la Comisión Europea se opone. En respuesta, Apple retrasará la introducción del USB-C.",
      "lang": "es"
    },
    {
      "id": 2,
      "text": "Texto sin entidades",
      "lang": "es"
    }
  ],
  "pretty": ""
}
```		
  

### Ejemplo Response
```json
{
  "documents_analized": [
    {
      "id": 1,
      "entities": [
        {
          "name": "Apple",
          "type": "ORG",
          "score": 0,
          "gloss": "Companies, agencies, institutions, etc."
        },
        {
          "name": "UK",
          "type": "ORG",
          "score": 0,
          "gloss": "Companies, agencies, institutions, etc."
        },
        {
          "name": "Comisión Europea",
          "type": "ORG",
          "score": 0,
          "gloss": "Companies, agencies, institutions, etc."
        },
        {
          "name": "Apple",
          "type": "ORG",
          "score": 0,
          "gloss": "Companies, agencies, institutions, etc."
        },
        {
          "name": "USBC",
          "type": "ORG",
          "score": 0,
          "gloss": "Companies, agencies, institutions, etc."
        }
      ]
    },
    {
      "id": 2,
      "entities": []
    }
  ]
}
```