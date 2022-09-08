"""Guided and automatic setup for new projects."""
import configparser
import json
import os
import shutil
import subprocess
from typing import Any, Dict, Optional, TypedDict


DEFAULT_BRANCH = "main"
DEFAULT_PYTHON = "3.10"
DEFAULT_GIT_USER = "{git_username}"
DEFAULT_GIT_EMAIL = "{git_email}"
SETTINGS_FILE = "settings.ini"


def input_with_default(label: str, defaults: configparser.ConfigParser, fallback: str = "", key: Optional[str] = None) -> str:
    """Return the string if non empty otherwise use the default."""
    key = label.replace(" ", "_") if key is None else key
    default = defaults.get("DEFAULT", key, fallback=fallback)
    prompt = f"{label}: " if default == "" or default.startswith("{") else f"{label} ({default}): "
    value = input(prompt).strip()
    if value == "":
        return default
    return value


def initialize_project() -> None:
    """Install the project."""
    subprocess.run(["nbdev_new"])
    subprocess.run(["nbdev_install_hooks"])
    shutil.copy("./nbdev-env/00_core.ipynb", "./00_core.ipynb")
    shutil.copy("./nbdev-env/index.ipynb", "./index.ipynb")
    

def install_git_hooks() -> None:
    """Install the git hooks for the repo."""
    subprocess.run(["nbdev_install_git_hooks"])


class Settings(TypedDict):
    """Ini file settings."""
    lib_name: str
    user: str
    description: str
    keywords: str
    author: str
    author_email: str
    copyright: str
    branch: str
    min_python: str


def update_ini() -> None:
    """Update the ini file with required info."""

    config = configparser.ConfigParser()
    config.read(SETTINGS_FILE)

    lib_name = input_with_default("lib name", defaults=config)
    user = input_with_default(f"github username", defaults=config, key="user")
    description = input_with_default("description", defaults=config)
    keywords = input_with_default("keywords", defaults=config)
    author = input_with_default(f"author", defaults=config, fallback=user)
    author_email = input_with_default(f"author email", defaults=config)
    copyright = input_with_default(f"copyright", defaults=config, fallback=author)
    branch = input_with_default(f"branch", defaults=config, fallback=DEFAULT_BRANCH)
    min_python = input_with_default(f"min python", defaults=config, fallback=DEFAULT_PYTHON)

    settings = Settings(
        lib_name=lib_name,
        user=user,
        description=description,
        keywords=keywords,
        author=author,
        author_email=author_email,
        copyright=copyright,
        branch=branch,
        min_python=min_python
    )
    inifile = SETTINGS_FILE
    with open(inifile, "r") as infile:
        lines = infile.readlines()

    for i, line in enumerate(lines):
        key = line.split("=")[0].strip("# ")
        if key in settings:
            lines[i] = f"{key} = {settings[key]}\n"

    with open(inifile, "w") as outfile:
        outfile.writelines(lines)
    

def is_type(cell: Dict[str, Any], cell_type: str) -> bool:
    """Return true if cell is of the given type."""
    return cell.get("cell_type") == cell_type


def is_markdown(cell: Dict[str, Any]) -> bool:
    """Return True if the cell is a markdown cell."""
    return is_type(cell, "markdown")


def is_code(cell: Dict[str, Any]) -> bool:
    """Return True if the cell is a code cell."""
    return is_type(cell, "code")


def source_startswith(cell: Dict[str, Any], key: str) -> bool:
    """Return True if cell source start with the key."""
    source = cell.get("source", [])
    return len(source) > 0 and source[0].startswith(key)


def update_index() -> None:
    """Update the index notebook."""
    notebook = "index.ipynb"
    with open(notebook, "r") as infile:
        index = json.loads(infile.read())
    
    config = configparser.ConfigParser()
    config.read(SETTINGS_FILE)
    lib_name = config.get("DEFAULT", "lib_name")

    for cell in index["cells"]:
        if (is_code(cell) and source_startswith(cell, "#| hide")):
            cell["source"] = [
                f"#| hide\n",
                f"from {lib_name}.core import*"]
        elif (is_markdown(cell) and source_startswith(cell, "# template")):
            cell["source"] = [
                f"# {lib_name}" "\n",
                "\n",
                f"> {config.get('DEFAULT', 'description')}" "\n"]
        elif (is_markdown(cell) and source_startswith(cell, "`pip install template`")):
            cell["source"] = [f"`pip install {lib_name}`"]
    
    with open(notebook, "w") as outfile:
        json.dump(index, outfile)


def update_core() -> None:
    """Update the core notebook."""
    notebook = "00_core.ipynb"
    with open(notebook, "r") as infile:
        core = json.loads(infile.read())
    
    config = configparser.ConfigParser()
    config.read(SETTINGS_FILE)
    lib_name = config.get("DEFAULT", "lib_name")

    for cell in core["cells"]:
        if (is_markdown(cell) and source_startswith(cell, "# module name here")):
            cell["source"] = [
                f"# {lib_name}" "\n",
                "\n",
                f"> {config.get('DEFAULT', 'description')}" "\n"]
    
    with open(notebook, "w") as outfile:
        json.dump(core, outfile)


def build_lib() -> None:
    """Build the package."""
    subprocess.run(["nbdev_build_lib"])


def build_docs() -> None:
    """Build the docs."""
    subprocess.run(["nbdev_build_docs"])


def configure_git() -> None:
    """Set git config info."""
    subprocess.run(["git", "config", "--local", "user.name", DEFAULT_GIT_USER])
    subprocess.run(["git", "config", "--local", "user.email", DEFAULT_GIT_EMAIL])


def set_git_user() -> None:
    """Set git user info."""
    config = configparser.ConfigParser()
    config.read("settings.ini")
    user = config.get("DEFAULT", "user", fallback="{}")
    if not user.startswith("{"):
        subprocess.run(["git", "config", "--local", "user.name", user])
    author_email = config.get("DEFAULT", "author_email", fallback="{}")
    if not author_email.startswith("{"):
        subprocess.run(["git", "config", "--local", "user.email", author_email])


def create_new() -> None:
    """Run all setup steps."""
    if not os.path.exists(SETTINGS_FILE):
        # configure_git()
        initialize_project()
        set_git_user()
        # install_git_hooks() does not need to be called because the hooks
        # are installed as part of initialize project.
        # update_ini()
        update_index()
        update_core()
        # build_lib()
        # build_docs()


if __name__ == "__main__":
    create_new()
