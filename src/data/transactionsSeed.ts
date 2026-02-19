import type { MasterTransaction } from '../types/transactionsMaster';

export const transactionsSeed: MasterTransaction[] = [
  {
    id: 'TXN-90211',
    profileName: 'Amaka Eze',
    accountLast4: '2049',
    type: 'bank_transfer',
    amount: 'N25,000',
    state: 'failed',
    transactionDate: '2026-02-18 09:21'
  },
  {
    id: 'TXN-90208',
    profileName: 'Tosin Akin',
    accountLast4: '1186',
    type: 'card_payment',
    amount: 'N12,500',
    state: 'successful',
    transactionDate: '2026-02-18 08:58'
  },
  {
    id: 'TXN-90201',
    profileName: 'Sade Bello',
    accountLast4: '7731',
    type: 'reversal',
    amount: 'N40,000',
    state: 'successful',
    transactionDate: '2026-02-17 18:37'
  },
  {
    id: 'TXN-90193',
    profileName: 'Chiamaka Obi',
    accountLast4: '6542',
    type: 'pos_charge',
    amount: 'N8,100',
    state: 'failed',
    transactionDate: '2026-02-17 14:12'
  },
  {
    id: 'TXN-90187',
    profileName: 'Ada Nwosu',
    accountLast4: '3104',
    type: 'bills',
    amount: 'N16,800',
    state: 'successful',
    transactionDate: '2026-02-17 11:05'
  },
  {
    id: 'TXN-90179',
    profileName: 'Ifeoma Ibe',
    accountLast4: '4420',
    type: 'bank_transfer',
    amount: 'N55,000',
    state: 'failed',
    transactionDate: '2026-02-16 20:40'
  }
];
