import React from "react";

interface CardProps {
  children: React.ReactNode;
  className?: string;
  glow?: "cyan" | "critical" | "warning" | "success" | false;
}

const glowMap = {
  cyan:     "border-accent-cyan/40 shadow-[0_0_20px_-6px_rgba(0,212,255,0.25)]",
  critical: "border-severity-critical/40 shadow-[0_0_20px_-6px_rgba(255,51,102,0.25)]",
  warning:  "border-severity-warning/40 shadow-[0_0_20px_-6px_rgba(255,170,51,0.25)]",
  success:  "border-severity-success/40 shadow-[0_0_20px_-6px_rgba(51,255,153,0.25)]",
};

export function Card({ children, className = "", glow = false }: CardProps) {
  return (
    <div
      className={[
        "bg-bg-secondary border border-border-subtle rounded-xl",
        glow ? glowMap[glow] : "",
        className,
      ].join(" ")}
    >
      {children}
    </div>
  );
}

interface CardHeaderProps {
  children: React.ReactNode;
  className?: string;
}

export function CardHeader({ children, className = "" }: CardHeaderProps) {
  return (
    <div className={["px-5 py-4 border-b border-border-subtle", className].join(" ")}>
      {children}
    </div>
  );
}

export function CardBody({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <div className={["p-5", className].join(" ")}>{children}</div>;
}
