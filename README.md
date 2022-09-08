# pemplate
> A template for creating python projects with nbdev.

# Usage
## Setup
After cloning the repo:
1. cd *repo-directory*
2. mkdir nbdev-env/loper
3. docker-compose --file nbdev-env/docker-compose.yml --project-directory . run setup
4. Add the custom_quarto_yml param to settings.ini
5. Add the host param to _quarto.yml preview section with a value of 0.0.0.0

## Running
Run the below command to launch jupyter lab and start developing:
- docker-compose --file nbdev-env/docker-compose.yml --project-directory . up
