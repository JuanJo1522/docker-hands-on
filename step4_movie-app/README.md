# Containerized Movie Explorer

Movie Explorer runs MongoDB, a Flask API, an Nginx UI, and the Qwen2.5-0.5B-Instruct Hugging Face model in a separate AI container. Nginx exposes the application at `http://localhost:8181`; its `/api` routes go to the API. The API filters movies by category and can ask the AI service for a text recommendation.

## Start locally (WSL Ubuntu)

Install Docker Engine with Compose and start it, then:

```bash
cd step4_movie-app
cp .env.example .env
nano .env # set a long random MONGO_ROOT_PASSWORD
export DOCKERHUB_USERNAME=local
export IMAGE_TAG=dev
docker compose up -d --build
```

Open `http://localhost:8181`. Category listing: `http://localhost:8181/api/movies?category=comedy`. AI recommendation: `http://localhost:8181/api/recommendations?category=comedy`. The first start downloads the model (about 1 GB) and can take several minutes; allow several GB of free RAM for inference. Watch progress with `docker compose logs -f movie-ai`.

Check services with `docker compose ps`; stop with `docker compose down`. `docker compose down -v` also deletes the MongoDB database and downloaded model cache.

## Tests and SonarQube

Run the small API test with coverage:

```bash
docker compose -f docker-compose.test.yml run --build --rm movie-tests
```

`Dockerfile.tests` provides a manual test image configuration too. The CI workflow at `../.github/workflows/movie-app.yml` scans the result to SonarQube. Run SonarQube on the same machine (commonly with its own Compose stack) and set GitHub variable `SONAR_HOST_URL` to a runner-reachable URL, plus secret `SONAR_TOKEN`.

## CI/CD and Docker Hub

The GitHub Actions workflow uses a Windows x64 **self-hosted runner** with Docker Desktop. Register the runner for this repository using GitHub's Settings → Actions → Runners guide, and leave its runner service running. Add repository secrets:

- `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` (create a Docker Hub access token)
- `MONGO_ROOT_USERNAME` and `MONGO_ROOT_PASSWORD`
- `SONAR_TOKEN`

Add repository variable `SONAR_HOST_URL`. The workflow tests/scans pull requests. On a push to `main`, after checks pass, it tags API/UI/AI images with the full commit SHA, pushes them to Docker Hub, and deploys the Compose stack on the runner. The runner checkout needs a `step4_movie-app/.env` populated with the same Mongo credentials before its first deployment; `.env` is ignored by Git.

## Gitflow branch routine

Protect `main` and require reviewed pull requests. Use `develop` for integration; feature branches start there and merge back by PR. Create release branches from `develop`, stabilize them, merge to `main` and back to `develop`, then create a `vX.Y.Z` tag on the release commit. Create hotfix branches from `main`, merge the fix to `main` and back to `develop`, and tag the patch release.

```bash
git switch main
git pull
git switch -c develop
git push -u origin develop
git switch -c feature/ai-recommendations
# edit, commit, push feature branch; open PR -> develop
```

A `main` push triggers publish and deployment; feature and develop work runs checks only. Use commit prefixes such as `feat:`, `fix:`, and `test:` so changes are easy to review. Image tags use commit SHA for traceable rollbacks.

