# Proyecto Simple con Django y Docker Compose

Este es un proyecto simple que utiliza Docker Compose para ejecutar una aplicación distribuida de Django.  
Asegúrate de tener Docker y Docker Compose instalados, y que el motor de Docker esté en funcionamiento antes de comenzar.

## Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) instalado en tu máquina.
- El motor de Docker debe estar en ejecución.

> Docker Compose viene incluido con Docker Desktop en Windows y macOS.  
> En Linux, puede que necesites instalarlo por separado.

## Cómo iniciar el proyecto

Para lanzar el proyecto, simplemente ejecuta el siguiente comando en el directorio del proyecto (donde se encuentra el archivo `compose.yml`):

```bash
docker compose up