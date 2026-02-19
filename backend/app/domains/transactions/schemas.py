from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

TransactionType = Literal["bank_transfer", "card_payment", "reversal", "pos_charge", "bills"]
TransactionState = Literal["failed", "successful"]


class TransactionCreateRequest(BaseModel):
    profile_name: str = Field(min_length=2, max_length=120)
    account_last4: str = Field(min_length=4, max_length=4)
    type: TransactionType
    amount: str = Field(min_length=2, max_length=80)
    state: TransactionState


class TransactionResponse(BaseModel):
    id: str
    profile_name: str
    account_last4: str
    type: TransactionType
    amount: str
    state: TransactionState
    transaction_date: str


class TransactionsListResponse(BaseModel):
    items: list[TransactionResponse]
    page: int
    page_size: int
    total: int
    total_pages: int
