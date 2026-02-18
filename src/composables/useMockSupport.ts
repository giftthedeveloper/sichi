import { computed, reactive } from 'vue';

import { customersSeed, messagesSeed, timelineSeed, transactionsSeed } from '../data/mockData';
import type { ChatMessage, Customer, NewSimulationInput, TicketStatus, TimelineEvent, Transaction } from '../types/domain';

interface SupportState {
  customers: Customer[];
  messages: ChatMessage[];
  transactions: Transaction[];
  events: TimelineEvent[];
  activeCustomerId: string;
}

const state = reactive<SupportState>({
  customers: structuredClone(customersSeed),
  messages: structuredClone(messagesSeed),
  transactions: structuredClone(transactionsSeed),
  events: structuredClone(timelineSeed),
  activeCustomerId: customersSeed[0].id
});

const nowStamp = (): string => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

const nextStatusByMessage = (body: string): TicketStatus => {
  if (body.toLowerCase().includes('human')) return 'escalated';
  if (body.toLowerCase().includes('sad') || body.toLowerCase().includes('lonely')) return 'blocked';
  return 'triaged';
};

export function useMockSupport() {
  const activeCustomer = computed(() =>
    state.customers.find((customer) => customer.id === state.activeCustomerId)
  );

  const activeMessages = computed(() =>
    state.messages.filter((message) => message.customerId === state.activeCustomerId)
  );

  const activeTransaction = computed(() =>
    state.transactions.find((transaction) => transaction.customerId === state.activeCustomerId)
  );

  const activeEvents = computed(() => {
    const transaction = activeTransaction.value;
    if (!transaction) return [];
    return state.events.filter((event) => event.transactionId === transaction.id);
  });

  const selectCustomer = (customerId: string): void => {
    state.activeCustomerId = customerId;
    const match = state.customers.find((customer) => customer.id === customerId);
    if (match) match.unread = 0;
  };

  const appendMessage = (message: ChatMessage): void => {
    state.messages.push(message);
  };

  const sendCustomerMessage = (body: string): void => {
    const customer = activeCustomer.value;
    if (!customer || !body.trim()) return;
    const status = nextStatusByMessage(body);
    appendMessage({
      id: `m-${crypto.randomUUID()}`,
      customerId: customer.id,
      sender: 'customer',
      body,
      createdAt: nowStamp()
    });
    customer.status = status;
    const transaction = state.transactions.find((item) => item.customerId === customer.id);
    if (transaction) {
      transaction.status = status;
      transaction.updatedAt = nowStamp();
    }
  };

  const escalateConversation = (): void => {
    const customer = activeCustomer.value;
    if (!customer) return;
    customer.status = 'escalated';
    const transaction = state.transactions.find((item) => item.customerId === customer.id);
    if (!transaction) return;
    transaction.status = 'escalated';
    transaction.escalationReason = 'user_requested';
    transaction.updatedAt = nowStamp();
    state.events.push({
      id: `e-${crypto.randomUUID()}`,
      transactionId: transaction.id,
      title: 'Escalated to human support',
      note: 'Requested directly in customer chat.',
      time: transaction.updatedAt
    });
  };

  const createSimulation = (input: NewSimulationInput): void => {
    const id = `tx-${Math.floor(Math.random() * 9000) + 1000}`;
    state.transactions.unshift({
      id,
      customerId: input.customerId,
      category: input.category,
      amount: input.amount,
      status: 'new',
      updatedAt: nowStamp(),
      source: 'simulation'
    });
    state.events.unshift({
      id: `e-${crypto.randomUUID()}`,
      transactionId: id,
      title: 'Simulation created',
      note: 'Mock case added from transaction simulator.',
      time: nowStamp()
    });
  };

  return {
    state,
    activeCustomer,
    activeMessages,
    activeTransaction,
    activeEvents,
    selectCustomer,
    sendCustomerMessage,
    escalateConversation,
    createSimulation
  };
}
