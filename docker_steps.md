# Ejecutar la aplicación de películas con Docker Compose

Esta versión levanta cuatro servicios: MongoDB, la API Flask, el frontend Nginx (`movie-ui`) y un Nginx adicional (`nginx-proxy`) que recibe el tráfico publicado y lo enruta al frontend o a la API. Desde el navegador solo se publica el puerto `8181` del proxy.

## Requisitos

- Docker Engine instalado y activo en Ubuntu.
- Plugin Docker Compose v2 (`docker compose`).

## Iniciar

Desde la carpeta `step4_movie-app`:

```bash
cd docker-hands-on/step4_movie-app
# Si venías de la versión anterior, elimina contenedores/red viejos.
# Este comando conserva el volumen de MongoDB.
docker compose down --remove-orphans
docker compose up --build -d
```

MongoDB carga los documentos iniciales definidos en `mongo/init-movies.js` al inicializar por primera vez el volumen. La API espera a que MongoDB pase su healthcheck antes de arrancar.

Si ya intentaste iniciar el stack con una configuración de inicialización anterior y MongoDB queda en estado `unhealthy`, recrea el volumen de datos y vuelve a iniciar:

```bash
docker compose down -v
docker compose up --build -d
```

`down -v` borra los datos guardados en MongoDB.

## Verificar

```bash
# Estado de los cuatro servicios
docker compose ps

# Deben aparecer 6 documentos y dos comedias
docker compose exec movie-db mongosh --quiet movies_db --eval 'printjson({total: db.movies.countDocuments(), comedies: db.movies.countDocuments({category: "comedy"})})'

# Revisar si la API está disponible desde el proxy
docker compose logs --tail=50 movie-api nginx-proxy

# Seguir los logs
docker compose logs -f

# Probar la interfaz y el proxy hacia la API
curl -i http://localhost:8181/
curl -s "http://localhost:8181/api/movies?category=comedy"
curl -s "http://localhost:8181/api/movies"
```

Abre `http://localhost:8181/` en el navegador y filtra las películas. La URL del API también pasa por Nginx: `http://localhost:8181/api/movies?category=comedy`.

Para ver los logs de un servicio específico:

```bash
docker compose logs -f movie-db
docker compose logs -f movie-api
docker compose logs -f movie-ui
docker compose logs -f nginx-proxy
```

## Detener y limpiar

```bash
# Detener y eliminar contenedores y red de Compose; conserva el volumen de datos
docker compose down

# También elimina el volumen (borra los datos de MongoDB)
docker compose down -v
```

MongoDB no publica el puerto `27017` en el host: la API se conecta por la red interna de Compose. Para acceder directamente a MongoDB durante el taller, se puede agregar temporalmente `ports: ["27017:27017"]` al servicio `movie-db`.
