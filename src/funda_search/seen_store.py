from __future__ import annotations

import sqlite3
from pathlib import Path

from .models import ListingSummary


class SeenStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.connection: sqlite3.Connection | None = None

    def __enter__(self) -> "SeenStore":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.execute(
            """
            create table if not exists seen_listing (
              listing_id text primary key,
              first_seen_at text not null default current_timestamp,
              last_seen_at text not null default current_timestamp
            )
            """
        )
        self.connection.commit()
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def mark_and_record(self, listings: list[ListingSummary]) -> list[ListingSummary]:
        connection = self._connection()
        annotated: list[ListingSummary] = []
        for listing in listings:
            was_seen = (
                connection.execute(
                    "select 1 from seen_listing where listing_id = ?",
                    (listing.id,),
                ).fetchone()
                is not None
            )
            connection.execute(
                """
                insert into seen_listing (listing_id) values (?)
                on conflict(listing_id) do update set last_seen_at = current_timestamp
                """,
                (listing.id,),
            )
            annotated.append(listing.with_seen_status(is_new=not was_seen))
        connection.commit()
        return annotated

    def _connection(self) -> sqlite3.Connection:
        if self.connection is None:
            raise RuntimeError("SeenStore must be used as a context manager")
        return self.connection
