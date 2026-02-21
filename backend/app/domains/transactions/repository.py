from __future__ import annotations

from datetime import datetime, timezone
import re

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


def list_for_profile(
    profile_name: str,
    limit: int = 5,
    transaction_id: str = "",
    state: str = "",
    transaction_type: str = "",
    account_last4: str = "",
) -> list[Transaction]:
    conditions = ["profile_name = ?"]
    params: list[object] = [profile_name]
    if transaction_id:
        conditions.append("id = ?")
        params.append(transaction_id)
    if state:
        conditions.append("state = ?")
        params.append(state)
    if transaction_type:
        conditions.append("type = ?")
        params.append(transaction_type)
    if account_last4:
        conditions.append("account_last4 = ?")
        params.append(account_last4)
    params.append(limit)
    where_clause = " AND ".join(conditions)
    with get_connection() as connection:
        rows = connection.execute(
            f"""
            SELECT id, profile_name, account_last4, type, amount, state, transaction_date
            FROM transactions
            WHERE {where_clause}
            ORDER BY transaction_date DESC
            LIMIT ?
            """,
            tuple(params),
        ).fetchall()
    return [Transaction(**dict(row)) for row in rows]


def summarize_profile(profile_name: str) -> dict[str, object]:
    items = list_for_profile(profile_name=profile_name, limit=200)
    successful = [item for item in items if item.state == "successful"]
    failed = [item for item in items if item.state == "failed"]
    debit_types = {"bank_transfer", "card_payment", "pos_charge", "bills"}
    credit_types = {"reversal"}
    net = 0
    for item in successful:
        digits = re.sub(r"\D", "", item.amount)
        amount = int(digits) if digits else 0
        if item.type in debit_types:
            net -= amount
        elif item.type in credit_types:
            net += amount
    latest = items[0] if items else None
    return {
        "total_transactions": len(items),
        "successful_transactions": len(successful),
        "failed_transactions": len(failed),
        "estimated_net_movement_naira": net,
        "latest_transaction_id": latest.id if latest else "",
        "latest_account_last4": latest.account_last4 if latest else "",
    }
