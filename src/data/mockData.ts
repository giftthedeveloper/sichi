import type { ChatMessage, Customer, TimelineEvent, Transaction } from '../types/domain';

export const customersSeed: Customer[] = [
  { id: 'c-101', name: 'Ava Harper', handle: '@avah', unread: 2, status: 'awaiting_user' },
  { id: 'c-102', name: 'Mina Sloan', handle: '@mina', unread: 0, status: 'resolved_by_bot' },
  { id: 'c-103', name: 'Lena Park', handle: '@lenap', unread: 1, status: 'triaged' }
];

export const messagesSeed: ChatMessage[] = [
  {
    id: 'm-1',
    customerId: 'c-101',
    sender: 'customer',
    body: 'My transfer to NovaPay failed this morning.',
    createdAt: '09:16'
  },
  {
    id: 'm-2',
    customerId: 'c-101',
    sender: 'bot',
    body: 'I can help. Please confirm transfer amount and date to continue.',
    createdAt: '09:17'
  },
  {
    id: 'm-3',
    customerId: 'c-102',
    sender: 'customer',
    body: 'Where is the refund from my card dispute?',
    createdAt: '08:50'
  },
  {
    id: 'm-4',
    customerId: 'c-102',
    sender: 'bot',
    body: 'Your refund is completed. It should appear within 24 hours.',
    createdAt: '08:52'
  }
];

export const transactionsSeed: Transaction[] = [
  {
    id: 'tx-7842',
    customerId: 'c-101',
    category: 'failed_transfer',
    amount: '$280.00',
    status: 'awaiting_user',
    updatedAt: '09:17',
    source: 'chat'
  },
  {
    id: 'tx-7831',
    customerId: 'c-102',
    category: 'card_dispute',
    amount: '$62.50',
    status: 'resolved_by_bot',
    updatedAt: '08:52',
    source: 'chat'
  },
  {
    id: 'tx-7827',
    customerId: 'c-103',
    category: 'transfer_status',
    amount: '$1,400.00',
    status: 'triaged',
    updatedAt: '08:47',
    source: 'chat'
  }
];

export const timelineSeed: TimelineEvent[] = [
  {
    id: 'e-1',
    transactionId: 'tx-7842',
    title: 'Intent classified: failed transfer',
    note: 'Confidence 0.88, in allowed category list.',
    time: '09:16'
  },
  {
    id: 'e-2',
    transactionId: 'tx-7842',
    title: 'Awaiting customer details',
    note: 'Requested amount, transfer date, and recipient handle.',
    time: '09:17'
  }
];
