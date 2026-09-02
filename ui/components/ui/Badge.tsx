import React from "react";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "critical" | "warning" | "success" | "cyan" | "muted";
  pulse?: boolean;
  className?: string;
}

const variantClasses: Record<NonNullable<BadgeProps["variant"]>, string> = {
  critical: "bg-severity-critical text-white",
  warning:  "bg-severity-warning text-black",
  success:  "bg-severity-success text-black",
  cyan:     "bg-accent-cyan/20 text-accent-cyan border border-accent-cyan/40",
  muted:    "bg-bg-elevated text-text-secondary border border-border-subtle",
};

export function Badge({ children, variant = "muted", pulse = false, className = "" }: BadgeProps) {
  return (
    <span
      className={[
        "inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold uppercase font-mono tracking-wide",
        variantClasses[variant],
        pulse ? "animate-pulse" : "",
        className,
      ].join(" ")}
    >
      {children}
    </span>
  );
}

export function severityVariant(s?: string): BadgeProps["variant"] {
  if (!s) return "muted";
  const lc = s.toLowerCase();
  if (lc.includes("retake") || lc === "critical") return "critical";
  if (lc.includes("review") || lc === "warning") return "warning";
  if (lc === "success" || lc === "info") return "success";
  return "muted";
}
