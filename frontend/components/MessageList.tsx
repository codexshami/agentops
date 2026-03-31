"use client";

import { Message } from "@/lib/types";
import { formatDistanceToNow } from "date-fns";
import ReactMarkdown from "react-markdown";
import CodeBlock from "./CodeBlock";
import styles from "@/styles/chat.module.css";

interface Props {
  messages: Message[];
  loading: boolean;
}

export default function MessageList({ messages, loading }: Props) {
  return (
    <div className={styles.messageList}>
      {messages.length === 0 ? (
        <div className={styles.emptyState}>
          <h2>Welcome to NextGen AI Agent</h2>
          <p>Start a conversation by typing your message below</p>
        </div>
      ) : (
        messages.map((msg) => (
          <div key={msg.id} className={`${styles.message} ${styles[msg.role]}`}>
            <div className={styles.messageContent}>
              <ReactMarkdown components={{ code: CodeBlock as any }}>
                {msg.content}
              </ReactMarkdown>
            </div>
            <div className={styles.messageFooter}>
              <span className={styles.timestamp}>
                {formatDistanceToNow(new Date(msg.created_at), { addSuffix: true })}
              </span>
              {msg.tokens_used > 0 && (
                <span className={styles.tokens}>Tokens: {msg.tokens_used}</span>
              )}
            </div>
          </div>
        ))
      )}
      {loading && (
        <div className={`${styles.message} ${styles.assistant}`}>
          <div className={styles.loadingDots}>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}
    </div>
  );
}