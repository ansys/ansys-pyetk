"""PyAEDT CLI extension for the Electronic Transformer Toolkit (PyETK).

Exposes the toolkit as a sub-app of the ``pyaedt`` CLI:

    pyaedt etk                             Show this help message
    pyaedt etk validate FILE [FILE ...]    Validate one or more JSON config files (no AEDT required)
    pyaedt etk create --file FILE          Create the full transformer model in a running AEDT
                      --port PORT          instance. Use part flags to build only a subset:
                      [--create-core]
                      [--create-winding]
                      [--create-bobbin]

By default (no part flags) the full model — core + winding + bobbin + circuit + setup — is
created in one shot via ``create_model()``.  When one or more part flags are given only those
specific geometries are built, which is useful for iterating on a single component without
rebuilding the whole design.
"""

from __future__ import annotations

import json
from pathlib import Path

import typer

etk_app = typer.Typer(
    help="Electronic Transformer Toolkit commands.",
    no_args_is_help=True,
)


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------


@etk_app.command(name="validate")
def validate(
    files: list[Path] = typer.Argument(..., help="One or more transformer JSON configuration files to validate."),
    json_output: bool = typer.Option(False, "--json", is_flag=True, help="Emit machine-readable JSON output."),
) -> None:
    """Validate one or more transformer JSON configuration files without launching AEDT."""
    from ansys.aedt.toolkits.electronic_transformer.backend.api import ToolkitBackend

    results = []
    any_failed = False

    for file in files:
        if not file.is_file():
            results.append({"file": str(file), "status": "error", "errors": [f"File not found: {file}"]})
            any_failed = True
            continue

        toolkit = ToolkitBackend()
        try:
            toolkit.load_properties_from_json(file)
        except Exception as exc:
            results.append({"file": str(file), "status": "error", "errors": [str(exc)]})
            any_failed = True
            continue

        valid, errors = toolkit.validate_model()
        results.append({"file": str(file), "status": "ok" if valid else "error", "errors": errors})
        if not valid:
            any_failed = True

    if json_output:
        typer.echo(json.dumps(results if len(results) > 1 else results[0]))
    else:
        for r in results:
            if r["status"] == "ok":
                typer.echo(f"✓ {r['file']}: Validation passed.")
            else:
                typer.echo(f"✗ {r['file']}: Validation failed.", err=True)
                for msg in r["errors"]:
                    typer.echo(f"    - {msg}", err=True)

    if any_failed:
        raise typer.Exit(code=1)


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


@etk_app.command(name="create")
def create(
    file: Path = typer.Argument(..., help="Path to the transformer JSON configuration file."),
    port: int = typer.Option(..., "--port", "-p", help="gRPC port of the running AEDT instance."),
    create_core: bool = typer.Option(False, "--create-core", is_flag=True, help="Create only the core geometry."),
    create_winding: bool = typer.Option(
        False, "--create-winding", is_flag=True, help="Create only the winding geometry."
    ),
    create_bobbin: bool = typer.Option(
        False, "--create-bobbin", is_flag=True, help="Create only the bobbin geometry."
    ),
    json_output: bool = typer.Option(False, "--json", is_flag=True, help="Emit machine-readable JSON output."),
) -> None:
    """Create a transformer model in a running AEDT instance from a JSON configuration file.

    By default the full model (core + winding + bobbin + circuit + analysis setup) is created
    in one shot.  Pass one or more part flags to build only specific components:

    \b
      --create-core      Build only the core geometry
      --create-winding   Build only the winding geometry
      --create-bobbin    Build only the bobbin geometry

    Multiple part flags can be combined (e.g. --create-core --create-winding).

    AEDT must already be running and accessible on the given gRPC port.
    Start one with: pyaedt session start --version <VERSION>
    """
    from ansys.aedt.toolkits.electronic_transformer.backend.api import ToolkitBackend

    if not file.is_file():
        _exit_error(f"File not found: {file}", json_output)

    # Determine build mode: full model vs. explicit parts
    build_all = not any([create_core, create_winding, create_bobbin])
    parts_requested = []
    if not build_all:
        if create_core:
            parts_requested.append("core")
        if create_winding:
            parts_requested.append("winding")
        if create_bobbin:
            parts_requested.append("bobbin")

    toolkit = ToolkitBackend()
    toolkit.properties.use_grpc = True
    toolkit.properties.selected_process = port

    try:
        toolkit.load_properties_from_json(file)
    except Exception as exc:
        _exit_error(f"Failed to load JSON: {exc}", json_output)

    _echo(f"Connecting to AEDT on port {port}...", json_output)
    try:
        toolkit.connect_aedt()
    except Exception as exc:
        _exit_error(f"Failed to connect to AEDT on port {port}: {exc}", json_output)
    toolkit.wait_to_be_idle()

    created = []
    failed = []

    if build_all:
        _echo("Creating full transformer model...", json_output)
        result = toolkit.create_model()
        if result:
            created.append("full model")
        else:
            failed.append("full model")
    else:
        _echo(f"Creating parts: {', '.join(parts_requested)}...", json_output)
        if create_core:
            result = toolkit.create_core_geometry()
            (created if result else failed).append("core")
        if create_winding:
            result = toolkit.create_winding_geometry()
            (created if result else failed).append("winding")
        if create_bobbin:
            result = toolkit.create_bobbin_geometry()
            (created if result else failed).append("bobbin")

    project = toolkit.properties.active_project
    design = toolkit.properties.active_design

    if failed:
        _exit_error(
            f"Failed to create: {', '.join(failed)}. "
            f"Created: {', '.join(created) or 'nothing'}. "
            "Check the AEDT log for details.",
            json_output,
        )

    if json_output:
        typer.echo(json.dumps({"status": "ok", "created": created, "project": project, "design": design}))
    else:
        typer.echo(f"Created {', '.join(created)} in project '{project}', design '{design}'.")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _echo(message: str, json_output: bool) -> None:
    """Print a status message only in human-readable mode."""
    if not json_output:
        typer.echo(message)


def _exit_error(message: str, json_output: bool) -> None:
    """Print an error and exit with code 1."""
    if json_output:
        typer.echo(json.dumps({"status": "error", "error": message}))
    else:
        typer.echo(f"Error: {message}", err=True)
    raise typer.Exit(code=1)