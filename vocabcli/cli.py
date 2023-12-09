""" This module provides vocabcli CLI."""
# vocabcli/cli.py

from pathlib import Path
from typing import Optional, List

import typer

from vocabcli import (
        ERRORS,
        __app_name__,
        __version__,
        config,
        database,
        vocabcli
)

app = typer.Typer()

@app.command()
def init(
        db_path: str = typer.Option(
            str(database.DEFAULT_DB_FILE_PATH),
            "--db-path",
            "-db",
            prompt="vocab database location?",
        ),
) -> None:
    """Initialise the vocab database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
                f'Creating config file failed with "{ERRORS[app_init_error]}"',
                fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
                f'Creating database failed with "{ERRORS[db_init_error]}"',
                fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The vocab database is {db_path}", fg=typer.colors.GREEN)

def get_worder() -> vocabcli.Worder:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
                'Config file not found. Please run "vocabcli init"',
                fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return vocabcli.Worder(db_path)
    else:
        typer.secho(
                'Database not found. Please run "vocabcli init"',
                fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def add(
        name: str = typer.Argument(...),
        article: Optional[str] = typer.Option(-1, "--article", "-a", min=-1, max=2),
        gender: Optional[str] = typer.Option(-1, "--gender", "-g", min=-1, max=2),
        typ: Optional[str] = typer.Argument(...),
) -> None:
    """Add a new word with a name."""
    worder = get_worder()
    article_map = ["der", "die", "das", None]
    gender_map = ["feminine", "masculine", "neuter", None]

    if typ == None:
        raise "You must provide a type!"

    word, error = worder.add(name, article_map[int(article)], gender_map[int(gender)], typ)

    if error:
        typer.secho(
                f'Adding word failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
                f"""     word: {name} was added
with article: {article_map[int(article)]}
with gender: {gender_map[int(gender)]}
with type: {typ}""",
                fg=typer.colors.GREEN,
        )

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None: 
    return
