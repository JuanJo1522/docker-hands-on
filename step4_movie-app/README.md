# Movie Explorer

Aplicación Docker Compose con una interfaz estática, API Flask, MongoDB, servicio de recomendaciones con Qwen y SonarQube Community Build con PostgreSQL. El frontend utiliza componentes Web de [BEEQ Design System](https://github.com/Endava/BEEQ).

## Levantar todos los servicios

En WSL Ubuntu, desde la raíz del repositorio:

```bash
cd step4_movie-app
test -f .env || cp .env.example .env
nano .env # define contraseñas locales largas y únicas
sudo sysctl -w vm.max_map_count=524288
docker compose up -d --build
```

SonarQube necesita `vm.max_map_count >= 524288` y `fs.file-max >= 131072` en el host para su Elasticsearch integrado. En WSL aplica temporalmente `sudo sysctl -w vm.max_map_count=524288` y `sudo sysctl -w fs.file-max=131072`; tras reiniciar WSL, repítelo. Para persistirlos, crea `/etc/sysctl.d/99-sonarqube.conf` con ambas líneas y aplica `sudo sysctl --system`. Compose configura los límites de archivos y procesos del contenedor SonarQube.

Si ya tienes un SonarQube independiente usando el puerto 9000, detenlo antes (`docker stop sonarqube`) o cambia `SONAR_PORT` en `.env`.

La primera compilación instala BEEQ y las dependencias de Python; además, el servicio de IA descarga el modelo al arrancar. El primer inicio puede tardar varios minutos y ocupar varios GB. SonarQube puede tardar un par de minutos adicionales en estar listo.

- Aplicación: `http://localhost:8182`
- SonarQube: `http://localhost:9000` (primer acceso normalmente `admin` / `admin`; cambia la contraseña)
- Películas: `http://localhost:8182/api/movies?category=drama`
- Recomendación IA: elige `drama`, `comedy` o `thriller` en la interfaz y usa **Elegir con IA**.

La siembra de MongoDB agrega o actualiza 24 películas sin duplicarlas. Para volver a ejecutar la siembra después de cambiar la lista, usa `docker compose run --rm movie-seed`; funciona también con el volumen de MongoDB ya creado. La IA recibe los títulos disponibles para la categoría elegida. El volumen del modelo evita volver a descargarlo.

Ver estado y logs:

```bash
docker compose ps
docker compose logs -f sonarqube
docker compose logs -f movie-ai
```

Detener sin borrar datos: `docker compose down`. No uses `-v` salvo que quieras eliminar las películas, los datos de SonarQube y la caché del modelo.

## Pruebas

- **Unitarias:** `backend/test_app.py` prueba filtros, validación y la comunicación con IA simulada; `mongo/test_db.py` prueba operaciones y proyección sobre Mongo simulado.
- **Integración:** `backend/test_integration.py` llama al endpoint Flask y consulta un MongoDB real aislado levantado por el Compose de pruebas.
- **End to end:** Playwright abre la interfaz servida por Nginx, filtra películas y pide una recomendación. El servicio IA se simula para que la prueba sea rápida y no descargue el modelo.

Desde `step4_movie-app` corre:

```bash
docker compose -p movie-tests -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from movie-tests
docker compose -p movie-tests -f docker-compose.test.yml down -v --remove-orphans
docker compose -p movie-e2e -f docker-compose.e2e.yml up --build --abort-on-container-exit --exit-code-from e2e
docker compose -p movie-e2e -f docker-compose.e2e.yml down -v --remove-orphans
```

La cobertura queda en `test-results/coverage.xml`; la configuración CI la envía a SonarQube. El workflow también arranca el servicio `sonarqube` desde el Compose principal antes de ejecutar el análisis.

## Secretos y persistencia

`.env` no se versiona. Conserva sus valores locales y reemplaza los marcadores de `.env.example`. En GitHub Actions configura `SONAR_TOKEN`, `SONAR_DB_USERNAME`, `SONAR_DB_PASSWORD`, `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `MONGO_ROOT_USERNAME` y `MONGO_ROOT_PASSWORD` como secretos, y `SONAR_HOST_URL=http://localhost:9000` como variable para el runner WSL. Si ya tenías el token asociado a un contenedor SonarQube independiente, genera un token nuevo en la instancia Compose y actualiza `SONAR_TOKEN` en GitHub.

`SONAR_DB_USERNAME` y `SONAR_DB_PASSWORD` se pueden definir en `.env` para el entorno local; si se cambian después de inicializar el volumen de PostgreSQL, las credenciales existentes no se actualizan automáticamente. La aplicación y SonarQube solo publican puertos en loopback por defecto.

## Gitflow y publicación

Crear una feature desde `develop`, abrir un PR de feature a develop, y una vez aprobada integrar la rama de release a `main`. Un push a `main` pasa tests/scan, publica las imágenes API, UI e IA a Docker Hub etiquetadas con el SHA y despliega Compose en la máquina del runner.

```bash
git switch develop
git pull
git switch -c feature/nombre-del-cambio
# editar, commit y push
git push -u origin feature/nombre-del-cambio
```

El runner autoalojado usado por este proyecto vive en WSL en `~/actions-runner/actions-runner`. Para ejecutarlo en una terminal WSL:

```bash
cd ~/actions-runner/actions-runner
./run.sh
```

Deja esa terminal abierta mientras GitHub Actions necesite el runner. Detén el proceso con `Ctrl+C`; si fue instalado como servicio, usa `./svc.sh start` y `./svc.sh stop` desde esa carpeta.
