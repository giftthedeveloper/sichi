from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

TransactionType = Literal["bank_transfer", "card_payment", "reversal", "pos_charge", "bills"]
TransactionState = Literal["failed", "successful"]


@dataclass
class Transaction:
    id: str
    profile_name: str
    account_last4: str
    type: TransactionType
    amount: str
    state: TransactionState
    transaction_date: str
