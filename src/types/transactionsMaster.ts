export type TransactionState = 'processing' | 'review' | 'resolved' | 'escalated';

export interface MasterTransaction {
  id: string;
  profileName: string;
  type: 'bank_transfer' | 'card_payment' | 'reversal' | 'pos_charge' | 'bills';
  amount: string;
  state: TransactionState;
  createdAt: string;
}
