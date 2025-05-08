# CI/CD Pipeline

The project uses **Azure DevOps Pipelines** to automate testing, building, and optionally deploying the Discord MovieBot.

## Pipeline Overview

The pipeline is defined in the `azure-pipelines.yml` file and consists of the following stages:

### Test
- Installs Python 3.12 and dependencies from `src/requirements.txt`
- Runs unit tests using `pytest`
- Checks code formatting using `black`
- Uses secrets from Azure variable group `moviebot-credentials`

### Docker
- Builds and pushes a Docker image to Docker Hub
- Skipped unless parameter `buildImage: true` is set
- Uses service connection `DockerHubConnection`

### Deploy *(optional)*
- Can simulate install/uninstall/reinstall steps using pipeline parameters
- Not implemented with real Kubernetes (yet)

## Environment Variables

The following secrets are stored in Azure DevOps as pipeline variables (via variable group):
- `DISCORD_TOKEN`
- `TMDB_API_KEY`
- `COHERE_API_KEY`

These are injected into a `.env` file during the build step.

## Running Pipeline Manually
You can trigger the pipeline from Azure DevOps UI and choose parameters like:
- Whether to build Docker (`buildImage: true/false`)
- Helm operation (`helmOperation: install/uninstall/both`)