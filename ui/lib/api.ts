import type { Alert, ScriptDeviation, DashboardStats, TrustReport } from "./types";

const BASE = typeof window !== "undefined" ? "/api" : (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api");

async function safeFetch<T>(url: string, options?: RequestInit): Promise<T | null> {
  try {
    const res = await fetch(url, options);
    if (!res.ok) return null;
    return res.json() as Promise<T>;
  } catch {
    return null;
  }
}

export async function fetchAlerts(): Promise<Alert[]> {
  const data = await safeFetch<{ alerts: Alert[] }>(`${BASE}/alerts/latest`);
  return data?.alerts ?? [];
}

export async function fetchDeviations(): Promise<ScriptDeviation[]> {
  const data = await safeFetch<{ deviations: ScriptDeviation[] }>(`${BASE}/script/deviations`);
  return data?.deviations ?? [];
}

export async function fetchDashboardStats(): Promise<DashboardStats | null> {
  return safeFetch<DashboardStats>(`${BASE}/dashboard/stats`);
}

export async function fetchTrustReport(): Promise<TrustReport | null> {
  return safeFetch<TrustReport>(`${BASE}/reports/daily`);
}

export async function sendChatMessage(question: string): Promise<string> {
  const data = await safeFetch<{ answer: string }>(`${BASE}/chat/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  return data?.answer ?? "Error connecting to Shadow API server.";
}

export async function recordDirectorDecision(
  alertId: string,
  decision: "retake" | "accept" | "dismiss"
): Promise<void> {
  await safeFetch(`${BASE}/alerts/${alertId}/decision`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ decision }),
  });
}
