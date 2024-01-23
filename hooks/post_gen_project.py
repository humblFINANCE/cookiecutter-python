import os
import platform
import shutil
import subprocess
import sys
import logging
from pathlib import Path
from rich.logging import RichHandler

# Configure logging with rich handler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger("rich")

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

# MICROMAMBA DEFINE FUNCTIONS ==================================================
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

def menv_exists_in(dir_name, start_path=Path.home(), depth=0, max_depth=2):
    """
    Recursively search for a directory up to a specified depth and return a tuple of (bool, Path) if it exists.
    Logs and ignores directories where access is denied. Returns (False, None) if no directory exists.

    Parameters
    ----------
    dir_name : str
        Name of the directory to search for.
    start_path : Path, optional
        The starting path for the search, defaults to the user's home directory.
    depth : int, optional
        Current depth of the search.
    max_depth : int, optional
        Maximum depth to search. Defaults to 2.

    Returns
    -------
    tuple
        A tuple of (bool, Path) where the bool is True if the directory is found, and the Path is the full path of the directory.
        If the directory is not found, the bool is False and the Path is None.
    """
    if depth > max_depth:
        return (False, None)

    try:
        if start_path.is_dir():
            if start_path.name == dir_name:
                return (True, start_path.resolve())
            for child in start_path.iterdir():
                if child.is_dir():
                    found_dir, path = menv_exists_in(
                        dir_name, child, depth + 1, max_depth
                    )
                    if found_dir:
                        new_dir = path.joinpath("menv")
                        if new_dir.exists():
                            return (True, new_dir)
                        return (True, path)
    except PermissionError as e:
        logger.warning(e)

    return (False, None)


# Function to check if micromamba is installed
def is_micromamba_installed():
    try:
        if platform.system() == "Windows":
            subprocess.check_output(["powershell", "-Command", "Get-Command micromamba"], shell=True)
        else:
            subprocess.check_output(["which", "micromamba"], shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

# MICROMAMBA INSTALLATION START ================================================
if not is_micromamba_installed():
    # Install micromamba
    if platform.system() == "Windows":
        # Windows Powershell
        run_command("Invoke-Expression ((Invoke-WebRequest -Uri https://micro.mamba.pm/install.ps1).Content)")
    else:
        # Linux, macOS, or Git Bash on Windows
        run_command('"${SHELL}" <(curl -L micro.mamba.pm/install.sh)')

if menv_exists_in("{{ cookiecutter.__package_name_kebab_case }}")[0]:
    print("A micromamba environment doesn't exist @ ", os.path.join(os.getcwd(), "menv"))

    # Create a new micromamba environment using the micromamba_env.yml file
    run_command("micromamba env create --file micromamba_env.yml --prefix ./menv")
    # Configure micromamba
    run_command("micromamba config --set env_prompt '({name})'")
    # Activate the micromamba environment
    run_command("micromamba activate --prefix ./menv")

{% endif %}
