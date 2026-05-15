import shutil
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

from invoke import Collection, Context, task

DOCS_PATH = Path("docs")
DOCS_SRC_PATH = DOCS_PATH / "src"


def get_allowed_doc_languages():
    """Detect languages as subfolders in docs/src/

    Ensure `en` is always first.
    """
    return ["en"] + [f.name for f in DOCS_SRC_PATH.iterdir() if f.is_dir() and f.name != "en"]


ALLOWED_DOC_LANGUAGES = get_allowed_doc_languages()
ALLOWED_VERSION_TYPES = ["release", "bug", "feature"]


@task
def version(_c: Context):
    """Show the current version."""
    with open("src/github_custom_actions/__about__.py") as f:
        version_line = f.readline()
        version_num = version_line.split('"')[1]
        print(version_num)
        return version_num


def ver_task_factory(version_type: str):
    @task
    def ver(c: Context):
        """Bump the version."""
        c.run(f"./scripts/verup.sh {version_type}")

    return ver


@task
def compile_requirements(c: Context):
    "Convert requirements.in to requirements.txt and requirements.dev.txt."
    start_time = subprocess.check_output(["date", "+%s"]).decode().strip()
    c.run("uv pip compile requirements.in --output-file=requirements.txt --upgrade")
    reqs_time = subprocess.check_output(["date", "+%s"]).decode().strip()
    c.run("uv pip compile requirements.dev.in --output-file=requirements.dev.txt --upgrade")
    end_time = subprocess.check_output(["date", "+%s"]).decode().strip()
    print(f"Req's compilation time: {int(reqs_time) - int(start_time)} seconds")
    print(f"Req's dev compilation time: {int(end_time) - int(reqs_time)} seconds")
    print(f"Total execution time: {int(end_time) - int(start_time)} seconds")

    c.run("scripts/include_pyproject_requirements.py requirements.in")


@task(pre=[compile_requirements])
def reqs(c: Context):
    """Upgrade requirements including pre-commit."""
    c.run("pip install -r requirements.dev.txt")


@contextmanager
def docs_rendered(language: str):
    """Render docs sources for language specified.

    Copy language agnostic assets from en to non-en folders.
    Substitute language and site dir in config copy.

    Returns config copy path.
    """
    config_template_path = DOCS_PATH / "mkdocs.yml"
    common_path = DOCS_PATH / "common"
    src_path = DOCS_SRC_PATH / language

    build_docs_path = Path("build") / "docs"
    build_config_path = build_docs_path / "mkdocs.yml"
    build_src_path = build_docs_path / "src" / language
    site_dir = Path("site") if language == "en" else Path("site") / language

    config = config_template_path.read_text()
    config = config.replace("LANGUAGE", language)
    config = config.replace("SITE_DIR", str(site_dir))

    build_docs_path.mkdir(parents=True, exist_ok=True)
    build_config_path.write_text(config)
    shutil.rmtree(build_src_path, ignore_errors=True)
    shutil.copytree(src_path, build_src_path)
    if common_path.is_dir():
        shutil.copytree(common_path, build_src_path, dirs_exist_ok=True)
    yield build_config_path


def docs_task_factory(language: str):
    @task
    def docs(c: Context):
        """Docs preview for the language specified."""
        with docs_rendered(language) as config_copy_path:
            port = 8001
            c.run(f"open -a 'Google Chrome' http://127.0.0.1:{port}")
            c.run(f"zensical serve --config-file {config_copy_path} --dev-addr localhost:{port}")

    return docs


@task
def build_docs(c: Context):
    """Build docs in docs/site/."""
    for language in ALLOWED_DOC_LANGUAGES:
        with docs_rendered(language) as config_copy_path:
            c.run(f"zensical build --config-file {config_copy_path}")


@task
def uv(c: Context):
    """Install or upgrade uv."""
    c.run("curl -LsSf https://astral.sh/uv/install.sh | sh")


@task
def pre(c):
    """Run pre-commit checks"""
    c.run("pre-commit run --verbose --all-files")


namespace = Collection.from_module(sys.modules[__name__])
for name in ALLOWED_VERSION_TYPES:
    namespace.add_task(ver_task_factory(name), name=f"ver-{name}")  # type: ignore[bad-argument-type]
for name in ALLOWED_DOC_LANGUAGES:
    namespace.add_task(docs_task_factory(name), name=f"docs-{name}")  # type: ignore[bad-argument-type]
