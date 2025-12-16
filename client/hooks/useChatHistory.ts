import { useState, useEffect, useCallback } from 'react';
import type { Message } from '@/types/chat';

export interface ChatConversation {
  id: string;
  title: string;
  timestamp: string;
  messages: Message[];
}

const STORAGE_KEY = 'meal-chat-history';
const MAX_CONVERSATIONS = 50;

export function useChatHistory() {
  const [conversations, setConversations] = useState<ChatConversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);

  // Load conversations from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        setConversations(parsed);
      }
    } catch (error) {
      console.error('Error loading chat history:', error);
    }
  }, []);

  // Save conversations to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
    } catch (error) {
      console.error('Error saving chat history:', error);
    }
  }, [conversations]);

  // Generate title from first user message
  const generateTitle = (messages: Message[]): string => {
    const firstUserMessage = messages.find(m => m.role === 'user' && m.content);
    if (firstUserMessage?.content) {
      // Truncate to 50 characters
      return firstUserMessage.content.length > 50
        ? firstUserMessage.content.substring(0, 50) + '...'
        : firstUserMessage.content;
    }
    return 'Cuộc trò chuyện mới';
  };

  // Format timestamp
  const formatTimestamp = (date: Date): string => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Vừa xong';
    if (minutes < 60) return `${minutes} phút trước`;
    if (hours < 24) return `${hours} giờ trước`;
    if (days === 1) return 'Hôm qua';
    if (days < 7) return `${days} ngày trước`;
    return date.toLocaleDateString('vi-VN');
  };

  // Create new conversation
  const createConversation = useCallback((messages: Message[]): string => {
    const id = Date.now().toString();
    const newConversation: ChatConversation = {
      id,
      title: generateTitle(messages),
      timestamp: formatTimestamp(new Date()),
      messages,
    };

    setConversations(prev => {
      const updated = [newConversation, ...prev];
      // Keep only MAX_CONVERSATIONS
      return updated.slice(0, MAX_CONVERSATIONS);
    });
    setCurrentConversationId(id);
    return id;
  }, []);

  // Update existing conversation
  const updateConversation = useCallback((id: string, messages: Message[]) => {
    setConversations(prev =>
      prev.map(conv =>
        conv.id === id
          ? {
              ...conv,
              title: generateTitle(messages),
              timestamp: formatTimestamp(new Date()),
              messages,
            }
          : conv
      )
    );
  }, []);

  // Save current conversation
  const saveConversation = useCallback((messages: Message[]) => {
    if (messages.length === 0) return;

    setConversations(prev => {
      // Check if current conversation exists
      const existingIndex = prev.findIndex(conv => conv.id === currentConversationId);

      if (existingIndex >= 0 && currentConversationId) {
        // Update existing conversation
        return prev.map(conv =>
          conv.id === currentConversationId
            ? {
                ...conv,
                title: generateTitle(messages),
                timestamp: formatTimestamp(new Date()),
                messages,
              }
            : conv
        );
      } else {
        // Create new conversation
        const id = Date.now().toString();
        const newConversation: ChatConversation = {
          id,
          title: generateTitle(messages),
          timestamp: formatTimestamp(new Date()),
          messages,
        };

        // Set current conversation ID only if it's a new conversation
        if (!currentConversationId) {
          setCurrentConversationId(id);
        }

        const updated = [newConversation, ...prev];
        return updated.slice(0, MAX_CONVERSATIONS);
      }
    });
  }, [currentConversationId]);

  // Load conversation by ID
  const loadConversation = useCallback((id: string): Message[] | null => {
    const conversation = conversations.find(conv => conv.id === id);
    if (conversation) {
      setCurrentConversationId(id);
      return conversation.messages;
    }
    return null;
  }, [conversations]);

  // Delete conversation
  const deleteConversation = useCallback((id: string) => {
    setConversations(prev => prev.filter(conv => conv.id !== id));
    if (currentConversationId === id) {
      setCurrentConversationId(null);
    }
  }, [currentConversationId]);

  // Start new conversation
  const startNewConversation = useCallback(() => {
    setCurrentConversationId(null);
  }, []);

  // Get conversation list for sidebar
  const getConversationList = useCallback(() => {
    return conversations.map(conv => ({
      id: conv.id,
      title: conv.title,
      timestamp: conv.timestamp,
    }));
  }, [conversations]);

  // Memoize conversation list
  const conversationList = getConversationList();

  return {
    conversations: conversationList,
    currentConversationId,
    saveConversation,
    loadConversation,
    deleteConversation,
    startNewConversation,
  };
}

