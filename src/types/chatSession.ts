export interface DemoProfile {
  id: string;
  name: string;
}

export type ConversationSender = 'user' | 'bot';

export type CaseStatus = 'gathering_info' | 'ready_to_resolve' | 'resolved' | 'escalated';

export interface CaseRecord {
  id: string;
  issue: string;
  status: CaseStatus;
  createdAt: string;
}

export interface ConversationMessage {
  id: string;
  sender: ConversationSender;
  text: string;
  time: string;
}
