from __future__ import annotations

from app.domains.transactions import repository
from app.domains.transactions.models import Transaction


def create_transaction(
    profile_name: str,
    account_last4: str,
    transaction_type: str,
    amount: str,
    state: str,
) -> Transaction:
    return repository.create_transaction(
        profile_name=profile_name.strip(),
        account_last4=account_last4.strip(),
        transaction_type=transaction_type,
        amount=amount.strip(),
        state=state,
    )


def list_transactions(page: int, page_size: int) -> tuple[list[Transaction], int, int]:
    items, total = repository.list_transactions(page=page, page_size=page_size)
    total_pages = max(1, (total + page_size - 1) // page_size)
    return items, total, total_pages
