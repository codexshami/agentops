"use client";

import { useState, useEffect, useRef } from "react";
import { apiClient } from "@/lib/api";
import { Message, Conversation } from "@/lib/types";
import MessageList from "./MessageList";
import InputBox from "./InputBox";
import styles from "@/styles/chat.module.css";

export default function ChatInterface() {
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    initializeConversation();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [conversation?.messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const initializeConversation = async () => {
    try {
      const newConversation = await apiClient.createConversation();
      setConversation(newConversation);
    } catch (err) {
      setError("Failed to initialize conversation");
    }
  };

  const handleSendMessage = async (message: string) => {
    if (!conversation) return;

    setLoading(true);
    setError("");

    try {
      const response = await apiClient.sendMessage({
        message,
        conversation_id: conversation.id,
      });

      setConversation((prev) => {
        if (!prev) return null;
        return {
          ...prev,
          messages: [
            ...prev.messages,
            {
              id: "temp-user",
              role: "user",
              content: message,
              tokens_used: 0,
              created_at: new Date().toISOString(),
            },
            {
              id: response.message_id,
              role: "assistant",
              content: response.response,
              tokens_used: response.tokens_used,
              created_at: response.timestamp,
            },
          ],
        };
      });
    } catch (err: any) {
      setError(err.message || "Failed to send message");
    } finally {
      setLoading(false);
    }
  };

  const handleNewConversation = async () => {
    await initializeConversation();
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.chatHeader}>
        <h1>NextGen AI Agent</h1>
        <button onClick={handleNewConversation} className={styles.newChatBtn}>
          + New Chat
        </button>
      </div>

      {error && <div className={styles.error}>{error}</div>}

      <MessageList messages={conversation?.messages || []} loading={loading} />
      <div ref={messagesEndRef} />

      <InputBox onSend={handleSendMessage} disabled={loading} />
    </div>
  );
}