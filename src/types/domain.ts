export type TicketStatus =
  | 'new'
  | 'triaged'
  | 'awaiting_user'
  | 'resolved_by_bot'
  | 'escalated'
  | 'blocked';

export type Sender = 'customer' | 'bot';

export type EscalationReason =
  | 'user_requested'
  | 'out_of_scope'
  | 'low_confidence'
  | 'policy_blocked'
  | 'safety_flag';

export interface Customer {
  id: string;
  name: string;
  handle: string;
  unread: number;
  status: TicketStatus;
}

export interface ChatMessage {
  id: string;
  customerId: string;
  sender: Sender;
  body: string;
  createdAt: string;
}

export interface Transaction {
  id: string;
  customerId: string;
  category: 'card_dispute' | 'transfer_status' | 'failed_transfer' | 'account_security';
  amount: string;
  status: TicketStatus;
  updatedAt: string;
  escalationReason?: EscalationReason;
  source: 'chat' | 'simulation';
}

export interface TimelineEvent {
  id: string;
  transactionId: string;
  title: string;
  note: string;
  time: string;
}

export interface NewSimulationInput {
  customerId: string;
  amount: string;
  category: Transaction['category'];
}
