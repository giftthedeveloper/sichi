export type TransactionState = 'failed' | 'successful';

export interface MasterTransaction {
  id: string;
  profileName: string;
  accountLast4: string;
  type: 'bank_transfer' | 'card_payment' | 'reversal' | 'pos_charge' | 'bills';
  amount: string;
  state: TransactionState;
  transactionDate: string;
}
