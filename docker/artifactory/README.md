# Local Terminus Artifactory

This directory defines a laptop-local JFrog Artifactory Community Edition for C/C++ deployment. It provides a Conan 2 package remote when the home-network `rpi5` server is unavailable.

Artifactory runs in Docker and stores all application state in a normal host directory. Removing or replacing the container therefore does not remove repositories or packages.

## Directory structure

```text
docker/artifactory/
├── .env.example
├── .gitignore
├── README.md
├── artifactory-service
└── compose.yaml
```

Runtime data is outside the Git repository by default:

```text
~/.terminus/artifactory/
├── backups/
└── var/
```

The `var/` directory is mounted at `/var/opt/jfrog/artifactory` inside the container and contains the database, package binaries, configuration, and logs.

## Requirements

- Docker Desktop with Docker Compose v2
- Conan 2 for client configuration
- At least 4 GiB of memory available to the container; 6–8 GiB available to Docker Desktop is more comfortable during startup
- Ports `8081` and `8082` available on localhost

The Compose ports bind to `127.0.0.1`, so the service is not exposed to the LAN by default.

## Initial setup

From this directory:

```bash
cp .env.example .env
./artifactory-service start
./artifactory-service logs
```

The first startup downloads the image and initializes Artifactory, which can take several minutes. Check readiness in another terminal:

```bash
./artifactory-service status
```

Open the UI at:

```text
http://localhost:8082
```

Complete the initial setup wizard and change the administrator password. Credentials belong in the local Artifactory/Conan credential stores and must not be added to `.env` or committed to Git.

## Create the Conan repository

In the Artifactory UI:

1. Open **Administration**.
2. Open **Repositories**.
3. Add a **Local Repository**.
4. Select the **Conan** package type.
5. Use `conan-local` as the repository key, or update `ARTIFACTORY_CONAN_REPOSITORY` in `.env`.

A local repository is sufficient for Terminus packages. A virtual Conan repository can be added later if multiple local or remote repositories need one client endpoint.

## Configure Conan

Activate the Terminus Conan environment, then add the remote:

```bash
go-conan
./artifactory-service configure-conan
```

To log in, pass the Artifactory username. Conan prompts for the password without placing it in shell history:

```bash
./artifactory-service configure-conan admin
```

The default endpoint is:

```text
http://localhost:8081/artifactory/api/conan/conan-local
```

The default Conan remote name is `terminus-local`. Confirm the configured remotes with:

```bash
conan remote list
```

When working away from home, disable the unreachable remote so Conan does not pause or fail while contacting it:

```bash
conan remote disable terminus-conan
```

Re-enable it after returning to the home network:

```bash
conan remote enable terminus-conan
```

## Build and upload packages

After configuring and logging into `terminus-local`, upload directly with Conan:

```bash
conan upload "terminus_core/1.0.6" --remote terminus-local --confirm
```

Existing Terminus build scripts currently use the remote configured by their Conan setup. Before relying on `tmns-docker-build -u`, verify that the build container has the local remote configured and can reach the host service. A container cannot use its own `localhost` to reach the macOS host; use this endpoint from Docker Desktop containers:

```text
http://host.docker.internal:8081/artifactory/api/conan/conan-local
```

A future improvement should allow `conan-setup.cfg` or `tmns-docker-build` to select between the `rpi5` and laptop Artifactory endpoints without editing tracked configuration.

## Lifecycle commands

Start or update the service:

```bash
./artifactory-service start
```

Show container and HTTP readiness:

```bash
./artifactory-service status
```

Follow logs:

```bash
./artifactory-service logs
```

Stop the container without deleting data:

```bash
./artifactory-service stop
```

The scripts intentionally do not include a data-destruction command. If the deployment must be reset, review and remove the configured `ARTIFACTORY_DATA_DIR` manually.

## Configuration

Copy `.env.example` to `.env` and adjust values locally:

| Variable | Default | Purpose |
|---|---|---|
| `ARTIFACTORY_IMAGE` | `releases-docker.jfrog.io/jfrog/artifactory-cpp-ce:7.63.12` | Pinned Artifactory image |
| `ARTIFACTORY_CONTAINER_NAME` | `terminus-artifactory` | Docker container name |
| `ARTIFACTORY_DATA_DIR` | `${HOME}/.terminus/artifactory/var` | Persistent host storage |
| `ARTIFACTORY_PORT` | `8081` | Artifactory service/API port |
| `ARTIFACTORY_ROUTER_PORT` | `8082` | Router and browser UI port |
| `ARTIFACTORY_CONAN_REPOSITORY` | `conan-local` | Conan repository key |
| `ARTIFACTORY_CONAN_REMOTE` | `terminus-local` | Local Conan remote name |

The image is pinned for reproducibility. Review JFrog release notes and update the pin deliberately instead of tracking `latest`.

## Backups

Stop Artifactory before taking a filesystem-level backup so the embedded database is consistent:

```bash
./artifactory-service stop
./artifactory-service backup
./artifactory-service start
```

Backups are written to `~/.terminus/artifactory/backups` by default. Override the destination for one invocation with:

```bash
ARTIFACTORY_BACKUP_DIR=/Volumes/Backup/terminus-artifactory ./artifactory-service backup
```

Periodically test restoration into a separate data directory. A backup that has never been restored should not be treated as verified.

## Suggested follow-up structure

As the deployment grows, keep host-management concerns under this directory:

```text
docker/artifactory/
├── config/                 # Non-secret Artifactory configuration templates
├── tests/                  # Service and Conan endpoint verification
├── artifactory-service     # Add guarded restore/bootstrap commands here
└── compose.yaml
```

Useful next steps are:

1. Add an authenticated REST bootstrap script for idempotent creation of `conan-local`.
2. Add selectable local/home Conan remote profiles to `conan-setup.cfg`.
3. Add a package migration script that downloads from `rpi5` and uploads to the local remote without copying credentials into files.
4. Add backup retention only after defining explicit retention requirements and confirmation safeguards.
5. Add a restore verification workflow using a separate container and temporary data directory.

## Troubleshooting

### Docker is unavailable

Start Docker Desktop and rerun `./artifactory-service start`.

### Artifactory is still starting

Inspect logs:

```bash
./artifactory-service logs
```

Java initialization and database migrations can make the first startup slow.

### Port already in use

Change `ARTIFACTORY_PORT` and/or `ARTIFACTORY_ROUTER_PORT` in `.env`, then restart the service.

### Permission errors in the data directory

Docker Desktop normally handles bind-mounted macOS directories. Confirm that Docker Desktop is permitted to access the configured path and that the current user owns it.

### Conan works on the host but not in build containers

Use `host.docker.internal`, not `localhost`, in the remote URL configured inside Docker Desktop containers.
