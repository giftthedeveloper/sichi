from __future__ import annotations

from datetime import datetime, timezone

from app.core.db import get_connection
from app.domains.transactions.models import Transaction


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_transactions_table() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
              id TEXT PRIMARY KEY,
              profile_name TEXT NOT NULL,
              account_last4 TEXT NOT NULL,
              type TEXT NOT NULL,
              amount TEXT NOT NULL,
              state TEXT NOT NULL,
              transaction_date TEXT NOT NULL
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date)")


def create_transaction(
    profile_name: str,
    account_last4: str,
    transaction_type: str,
    amount: str,
    state: str,
) -> Transaction:
    with get_connection() as connection:
        row = connection.execute("SELECT COUNT(*) AS total FROM transactions").fetchone()
        next_number = int(row["total"]) + 1 if row else 1
        txn_id = f"TXN-{90000 + next_number}"
        now = _now_iso()
        connection.execute(
            """
            INSERT INTO transactions (id, profile_name, account_last4, type, amount, state, transaction_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (txn_id, profile_name, account_last4, transaction_type, amount, state, now),
        )
    return Transaction(
        id=txn_id,
        profile_name=profile_name,
        account_last4=account_last4,
        type=transaction_type,
        amount=amount,
        state=state,
        transaction_date=now,
    )


def list_transactions(page: int, page_size: int) -> tuple[list[Transaction], int]:
    offset = (page - 1) * page_size
    with get_connection() as connection:
        total_row = connection.execute("SELECT COUNT(*) AS total FROM transactions").fetchone()
        rows = connection.execute(
            """
            SELECT id, profile_name, account_last4, type, amount, state, transaction_date
            FROM transactions
            ORDER BY transaction_date DESC
            LIMIT ? OFFSET ?
            """,
            (page_size, offset),
        ).fetchall()
    total = int(total_row["total"]) if total_row else 0
    items = [Transaction(**dict(row)) for row in rows]
    return items, total
