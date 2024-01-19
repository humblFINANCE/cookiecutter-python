import os
import platform
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
with_pydantic_typing = int("{{ cookiecutter.with_pydantic_typing }}")

continuous_integration = "{{ cookiecutter.continuous_integration }}"
is_deployable_app = (
    "{{ not not cookiecutter.with_fastapi_api|int or not not cookiecutter.with_streamlit_app|int }}"
    == "True"
)
is_publishable_package = (
    "{{ not cookiecutter.with_fastapi_api|int and not cookiecutter.with_streamlit_app|int }}"
    == "True"
)
# Remove tagged.py if not using pydantic typing
if not with_pydantic_typing:
    os.remove(f"src/{package_name}/core/models/abstract/tagged.py")

# Remove base_model.py if not using pandera models
if not with_pandera_models:
    os.remove(f"src/{package_name}/core/models/base_model.py")

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


{% if cookiecutter.with_micromamba|int %}
# Setup Micromamba environment
def run_command(command):
    if platform.system() == "Windows":
        # Run the command in a new PowerShell process
        process = subprocess.Popen(["powershell", "-Command", command], shell=True)
    else:
        process = subprocess.Popen(command, shell=True)
    process.wait()
    if process.returncode != 0:
        print(f"Command failed: {command}", file=sys.stderr)
        sys.exit(1)

# Install micromamba
if platform.system() == "Windows":
    # Windows Powershell
    run_command(
        "Invoke-Expression ((Invoke-WebRequest -Uri https://micro.mamba.pm/install.ps1).Content)"
        )
else:
    # Linux, macOS, or Git Bash on Windows
    run_command('"${SHELL}" <(curl -L micro.mamba.pm/install.sh)')

# Create a new micromamba environment using the micromamba_env.yml file
run_command("micromamba env create --file micromamba_env.yml --prefix ./menv")

# Configure micromamba
run_command("micromamba config --set env_prompt '({name})'")

# Activate the micromamba environment
run_command(
    "echo 'source /opt/conda/etc/profile.d/conda.sh && conda activate ./menv' >> ~/.bashrc"
)
{% endif %}
