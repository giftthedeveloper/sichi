export interface DemoProfile {
  id: string;
  name: string;
}

export type ConversationSender = 'user' | 'bot';

export type CaseStatus = 'active' | 'ready_to_resolve' | 'resolved' | 'escalated';

export interface CaseRecord {
  id: string;
  status: CaseStatus;
  detailStage: 0 | 1 | 2 | 3;
  createdAt: string;
  updatedAt: string;
}

export interface ConversationMessage {
  id: string;
  sender: ConversationSender;
  text: string;
  time: string;
}
