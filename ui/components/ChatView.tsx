"use client";

import React, { useRef, useEffect } from "react";
import { MessageSquare, Send, RefreshCw, Sparkles } from "lucide-react";
import type { ChatMessage } from "@/lib/types";

const SUGGESTION_CHIPS = [
  "Why is 37:08 a retake?",
  "Did Ben follow the script for the table?",
  "What props changed state in Scene 13?",
  "Show all CRITICAL alerts",
  "How confident is Shadow in the footwear flag?",
  "What's the script rule for the lighter fluid?",
];

// ─── Markdown Formatter ───────────────────────────────────────────────────

function InlineMarkdown({ text }: { text: string }) {
  const parts: React.ReactNode[] = [];
  const regex = /(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)/g;
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.substring(lastIndex, match.index));
    }
    const token = match[0];
    if (token.startsWith("**") && token.endsWith("**")) {
      parts.push(
        <strong key={match.index} className="font-semibold text-white">
          {token.slice(2, -2)}
        </strong>
      );
    } else if (token.startsWith("`") && token.endsWith("`")) {
      parts.push(
        <code key={match.index} className="px-1.5 py-0.5 rounded bg-black/50 text-accent-cyan font-mono text-xs">
          {token.slice(1, -1)}
        </code>
      );
    } else if (token.startsWith("*") && token.endsWith("*")) {
      parts.push(
        <em key={match.index} className="italic text-text-primary">
          {token.slice(1, -1)}
        </em>
      );
    }
    lastIndex = regex.lastIndex;
  }

  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex));
  }

  return <>{parts}</>;
}

function FormattedMarkdown({ content }: { content: string }) {
  const lines = content.split("\n");
  const elements: React.ReactNode[] = [];
  let listItems: string[] = [];

  const flushList = (keyPrefix: string) => {
    if (listItems.length > 0) {
      elements.push(
        <ul key={`${keyPrefix}-ul`} className="my-1.5 space-y-1 pl-4 list-disc text-text-secondary">
          {listItems.map((item, idx) => (
            <li key={idx} className="text-xs leading-relaxed">
              <InlineMarkdown text={item} />
            </li>
          ))}
        </ul>
      );
      listItems = [];
    }
  };

  lines.forEach((line, i) => {
    const trimmed = line.trim();
    if (trimmed.startsWith("* ") || trimmed.startsWith("- ")) {
      listItems.push(trimmed.slice(2));
    } else if (/^\d+\.\s/.test(trimmed)) {
      listItems.push(trimmed.replace(/^\d+\.\s/, ""));
    } else {
      flushList(`line-${i}`);
      if (!trimmed) {
        return;
      }
      if (trimmed.startsWith("### ")) {
        elements.push(
          <h4 key={i} className="text-xs font-bold text-accent-cyan uppercase tracking-wider mt-2.5 mb-1">
            <InlineMarkdown text={trimmed.slice(4)} />
          </h4>
        );
      } else if (trimmed.startsWith("## ")) {
        elements.push(
          <h3 key={i} className="text-sm font-bold text-white mt-2.5 mb-1">
            <InlineMarkdown text={trimmed.slice(3)} />
          </h3>
        );
      } else if (trimmed.startsWith("# ")) {
        elements.push(
          <h2 key={i} className="text-base font-bold text-white mt-2.5 mb-1">
            <InlineMarkdown text={trimmed.slice(2)} />
          </h2>
        );
      } else {
        elements.push(
          <p key={i} className="text-xs leading-relaxed text-text-secondary my-1">
            <InlineMarkdown text={trimmed} />
          </p>
        );
      }
    }
  });

  flushList("final");
  return <div className="space-y-0.5">{elements}</div>;
}

// ─── Message bubble ────────────────────────────────────────────────────────

interface BubbleProps {
  message: ChatMessage;
}

function MessageBubble({ message }: BubbleProps) {
  const isDirector = message.role === "director";
  return (
    <div className={["flex flex-col gap-1", isDirector ? "items-end" : "items-start"].join(" ")}>
      <span className="text-[10px] font-mono text-text-muted uppercase tracking-wider px-1">
        {isDirector ? "Director" : "Shadow"}
      </span>
      <div
        className={[
          "max-w-2xl rounded-2xl px-4 py-3 text-sm leading-relaxed",
          isDirector
            ? "bg-accent-cyan text-black font-medium rounded-br-none"
            : "bg-[#1a1a24] text-text-primary border border-border-subtle rounded-bl-none",
        ].join(" ")}
      >
        {isDirector ? (
          <div>{message.text}</div>
        ) : (
          <FormattedMarkdown content={message.text} />
        )}
      </div>
      {message.timestamp && (
        <span className="text-[9px] font-mono text-text-muted px-1">{message.timestamp}</span>
      )}
    </div>
  );
}

// ─── Typing indicator ─────────────────────────────────────────────────────

function TypingIndicator() {
  return (
    <div className="flex items-start gap-2">
      <div className="bg-[#1a1a24] border border-border-subtle rounded-2xl rounded-bl-none px-4 py-3 flex items-center gap-1.5">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="w-1.5 h-1.5 rounded-full bg-accent-cyan/60 animate-bounce"
            style={{ animationDelay: `${i * 0.15}s` }}
          />
        ))}
      </div>
    </div>
  );
}

// ─── Chat View ─────────────────────────────────────────────────────────────

interface ChatViewProps {
  messages: ChatMessage[];
  inputValue: string;
  loading: boolean;
  onInputChange: (v: string) => void;
  onSend: () => void;
}

export default function ChatView({ messages, inputValue, loading, onInputChange, onSend }: ChatViewProps) {
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to newest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  const handleChip = (text: string) => {
    onInputChange(text);
    inputRef.current?.focus();
  };

  return (
    <div className="bg-bg-secondary border border-border-subtle rounded-xl flex flex-col h-[680px] md:h-[720px]">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-4 border-b border-border-subtle shrink-0">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-accent-cyan/10 border border-accent-cyan/30 flex items-center justify-center">
            <MessageSquare className="w-4 h-4 text-accent-cyan" />
          </div>
          <div>
            <h3 className="text-sm font-semibold">Director Direct Line</h3>
            <p className="text-[10px] text-text-secondary">Grounded on 1968 Screenplay · 142 Film Cuts</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-severity-success animate-pulse" />
          <span className="text-[11px] font-mono text-severity-success">Shadow Online</span>
        </div>
      </div>

      {/* Message list */}
      <div className="flex-1 overflow-y-auto px-5 py-5 space-y-4">
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} message={msg} />
        ))}
        {loading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>

      {/* Suggestion chips */}
      <div className="px-5 py-2 border-t border-border-subtle shrink-0">
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 hide-scrollbar">
          <Sparkles className="w-3 h-3 text-accent-cyan shrink-0" />
          {SUGGESTION_CHIPS.map((chip) => (
            <button
              key={chip}
              onClick={() => handleChip(chip)}
              className="shrink-0 text-[11px] px-3 py-1 rounded-full border border-accent-cyan/30 text-accent-cyan/80 hover:bg-accent-cyan/10 hover:text-accent-cyan transition whitespace-nowrap"
            >
              {chip}
            </button>
          ))}
        </div>
      </div>

      {/* Input bar */}
      <div className="px-4 py-3 border-t border-border-subtle shrink-0">
        <div className="flex gap-2 items-center">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => onInputChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask Shadow about any scene, prop, or continuity flag…"
            disabled={loading}
            className="flex-1 bg-[#1a1a24] border border-border-subtle rounded-xl px-4 py-2.5 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent-cyan/50 disabled:opacity-50 transition"
          />
          <button
            onClick={onSend}
            disabled={loading || !inputValue.trim()}
            className="flex items-center gap-1.5 bg-accent-cyan hover:bg-accent-cyan/90 disabled:opacity-40 disabled:cursor-not-allowed text-black px-4 py-2.5 rounded-xl font-semibold text-sm transition shrink-0"
          >
            {loading ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
            <span className="hidden sm:inline">Send</span>
          </button>
        </div>
      </div>
    </div>
  );
}
