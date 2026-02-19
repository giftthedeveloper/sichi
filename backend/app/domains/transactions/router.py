from __future__ import annotations

from fastapi import APIRouter, Query

from app.domains.transactions.models import Transaction
from app.domains.transactions.schemas import TransactionCreateRequest, TransactionResponse, TransactionsListResponse
from app.domains.transactions import service

router = APIRouter(prefix="/transactions", tags=["transactions"])


def _to_schema(transaction: Transaction) -> TransactionResponse:
    return TransactionResponse(
        id=transaction.id,
        profile_name=transaction.profile_name,
        account_last4=transaction.account_last4,
        type=transaction.type,
        amount=transaction.amount,
        state=transaction.state,
        transaction_date=transaction.transaction_date,
    )


@router.get("", response_model=TransactionsListResponse)
def list_transactions(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=5, ge=1, le=50),
) -> TransactionsListResponse:
    items, total, total_pages = service.list_transactions(page=page, page_size=page_size)
    return TransactionsListResponse(
        items=[_to_schema(item) for item in items],
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )


@router.post("", response_model=TransactionResponse)
def create_transaction(payload: TransactionCreateRequest) -> TransactionResponse:
    transaction = service.create_transaction(
        profile_name=payload.profile_name,
        account_last4=payload.account_last4,
        transaction_type=payload.type,
        amount=payload.amount,
        state=payload.state,
    )
    return _to_schema(transaction)
