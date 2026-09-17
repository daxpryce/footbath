from pathlib import Path
from typing import Literal

import polars as pl


def write_to_table(
    df: pl.DataFrame,
    db_path: Path,
    table_name: str,
    if_table_exists: Literal["append", "replace", "fail"],
) -> None:
    # validate path exists (or is writable at least)
    db_as_uri = f"sqlite:///{db_path}"
    df.write_database(
        table_name=table_name,
        connection=db_as_uri,
        if_table_exists=if_table_exists,
    )
