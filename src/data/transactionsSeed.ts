import type { MasterTransaction } from '../types/transactionsMaster';

export const transactionsSeed: MasterTransaction[] = [
  {
    id: 'TXN-90211',
    profileName: 'Amaka Eze',
    type: 'bank_transfer',
    amount: 'N25,000',
    state: 'processing',
    createdAt: '2026-02-18 09:21'
  },
  {
    id: 'TXN-90208',
    profileName: 'Tosin Akin',
    type: 'card_payment',
    amount: 'N12,500',
    state: 'review',
    createdAt: '2026-02-18 08:58'
  },
  {
    id: 'TXN-90201',
    profileName: 'Sade Bello',
    type: 'reversal',
    amount: 'N40,000',
    state: 'resolved',
    createdAt: '2026-02-17 18:37'
  },
  {
    id: 'TXN-90193',
    profileName: 'Chiamaka Obi',
    type: 'pos_charge',
    amount: 'N8,100',
    state: 'escalated',
    createdAt: '2026-02-17 14:12'
  }
];
