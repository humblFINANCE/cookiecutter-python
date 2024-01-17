import os
import shutil
import subprocess
import sys

# Read Cookiecutter configuration.
package_name = "{{ cookiecutter.__package_name_snake_case }}"
development_environment = "{{ cookiecutter.development_environment }}"
with_fastapi_api = int("{{ cookiecutter.with_fastapi_api }}")
with_sentry_logging = int("{{ cookiecutter.with_sentry_logging }}")
with_streamlit_app = int("{{ cookiecutter.with_streamlit_app }}")
with_typer_cli = int("{{ cookiecutter.with_typer_cli }}")
with_pandera_models = int("{{ cookiecutter.with_pandera_models }}")
continuous_integration = "{{ cookiecutter.continuous_integration }}"
is_deployable_app = (
    "{{ not not cookiecutter.with_fastapi_api|int or not not cookiecutter.with_streamlit_app|int }}"
    == "True"
)
is_publishable_package = (
    "{{ not cookiecutter.with_fastapi_api|int and not cookiecutter.with_streamlit_app|int }}"
    == "True"
)

# Remove py.typed and Dependabot if not in strict mode.
if development_environment != "strict":
    os.remove(f"src/{package_name}/py.typed")
    os.remove(".github/dependabot.yml")

# Remove FastAPI if not selected.
if not with_fastapi_api:
    os.remove(f"src/{package_name}/api.py")
    os.remove("tests/test_api.py")

# Remove Sentry if not selected.
if not with_sentry_logging:
    os.remove(f"src/{package_name}/sentry.py")
    os.remove("tests/test_sentry.py")

# Remove Streamlit if not selected.
if not with_streamlit_app:
    os.remove(f"src/{package_name}/app.py")

# Remove Typer if not selected.
if not with_typer_cli:
    os.remove(f"src/{package_name}/cli.py")
    os.remove("tests/test_cli.py")

# Remove the continuous integration provider that is not selected.
if continuous_integration != "GitHub":
    shutil.rmtree(".github/")
elif continuous_integration != "GitLab":
    os.remove(".gitlab-ci.yml")

# Remove unused GitHub Actions workflows.
if continuous_integration == "GitHub":
    if not is_deployable_app:
        os.remove(".github/workflows/deploy.yml")
    if not is_publishable_package:
        os.remove(".github/workflows/publish.yml")


# Setup Micromamba environment
def run_command(command):
    process = subprocess.Popen(command, shell=True)
    process.wait()
    if process.returncode != 0:
        print(f"Command failed: {command}", file=sys.stderr)
        sys.exit(1)


# Install micromamba
run_command(
    "wget -qO- https://micromamba.snakepit.net/api/micromamba/linux-64/latest | tar -xvj bin/micromamba"
)

# Make micromamba executable
run_command("chmod +x bin/micromamba")

# Create a new micromamba environment using the micromamba_env.yml file
run_command("./bin/micromamba env create --file micromamba_env.yml")

# Configure micromamba
run_command("./bin/micromamba config --set env_prompt '({name})'")

# Activate the micromamba environment
run_command(
    "echo 'source /opt/conda/etc/profile.d/conda.sh && conda activate ./menv' >> ~/.bashrc"
)
