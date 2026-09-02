"use client";

import React, { useState, useEffect, useCallback } from "react";
import { Film, AlertTriangle, Eye, FileText, MessageSquare, BarChart2, RefreshCw, Menu, X } from "lucide-react";
import type { Alert, ScriptDeviation, DashboardStats, TrustReport, ChatMessage, ActiveTab, DirectorDecision } from "@/lib/types";
import { fetchAlerts, fetchDeviations, fetchDashboardStats, fetchTrustReport, sendChatMessage, recordDirectorDecision } from "@/lib/api";

import DashboardView from "@/components/DashboardView";
import AlertDetailView from "@/components/AlertDetailView";
import ScriptDeviationsView from "@/components/ScriptDeviationsView";
import ChatView from "@/components/ChatView";
import TrustReportView from "@/components/TrustReportView";

// ─── Nav tab definitions ──────────────────────────────────────────────────

const TABS: { id: ActiveTab; label: string; icon: React.ElementType; badge?: (alerts: Alert[], devs: ScriptDeviation[]) => number | null }[] = [
  { id: "dashboard",   label: "Dashboard",          icon: Film },
  { id: "alerts",      label: "Continuity Alerts",  icon: AlertTriangle,  badge: (a) => a.length || null },
  { id: "deviations",  label: "Script Deviations",  icon: FileText,       badge: (_, d) => d.length || null },
  { id: "chat",        label: "Chat with Shadow",   icon: MessageSquare },
  { id: "report",      label: "Trust Report",       icon: BarChart2 },
];

const BADGE_COLORS: Record<ActiveTab, string> = {
  dashboard:  "",
  alerts:     "bg-severity-critical text-white",
  deviations: "bg-severity-warning text-black",
  chat:       "",
  report:     "",
};

// ─── Root page ────────────────────────────────────────────────────────────

export default function ShadowCutDashboard() {
  const [activeTab, setActiveTab]     = useState<ActiveTab>("dashboard");
  const [alerts, setAlerts]           = useState<Alert[]>([]);
  const [deviations, setDeviations]   = useState<ScriptDeviation[]>([]);
  const [stats, setStats]             = useState<DashboardStats | null>(null);
  const [report, setReport]           = useState<TrustReport | null>(null);
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);
  const [userDecisions, setUserDecisions] = useState<Record<string, DirectorDecision>>({});
  const [chatMessages, setChatMessages]   = useState<ChatMessage[]>([
    {
      role: "assistant",
      text: "Shadow ready. Screenplay Scene 12–16 (Farmhouse Siege) cross-referenced against 142 cuts. 1 CRITICAL error flagged for RETAKE ('UPPER RIGHT CORNER' crew board marking at 37:08, 100% confidence), 2 items flagged for DIRECTOR REVIEW, and 1 actor performance script deviation noted.",
    },
  ]);
  const [chatInput, setChatInput]   = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [syncing, setSyncing]         = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // ── Data fetching ───────────────────────────────────────────────

  const loadAll = useCallback(async () => {
    setSyncing(true);
    const [newAlerts, newDevs, newStats, newReport] = await Promise.all([
      fetchAlerts(),
      fetchDeviations(),
      fetchDashboardStats(),
      fetchTrustReport(),
    ]);
    if (newAlerts.length) {
      setAlerts(newAlerts);
      if (!selectedAlert) setSelectedAlert(newAlerts[0]);
    }
    if (newDevs.length) setDeviations(newDevs);
    if (newStats) setStats(newStats);
    if (newReport) setReport(newReport);
    setSyncing(false);
  }, [selectedAlert]);

  useEffect(() => { loadAll(); }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  // ── Chat ────────────────────────────────────────────────────────

  const handleSend = async () => {
    const text = chatInput.trim();
    if (!text || chatLoading) return;
    setChatInput("");
    setChatMessages((prev) => [...prev, { role: "director", text }]);
    setChatLoading(true);
    const answer = await sendChatMessage(text);
    setChatMessages((prev) => [...prev, { role: "assistant", text: answer }]);
    setChatLoading(false);
  };

  // ── Director decisions ──────────────────────────────────────────

  const handleDecision = useCallback(async (alertId: string, decision: DirectorDecision) => {
    setUserDecisions((prev) => ({ ...prev, [alertId]: decision }));
    await recordDirectorDecision(alertId, decision);
  }, []);

  // ── Nav helpers ─────────────────────────────────────────────────

  const navigate = (tab: ActiveTab) => {
    setActiveTab(tab);
    setMobileMenuOpen(false);
  };

  const alertCount = alerts.length;
  const devCount   = deviations.length;

  // ─────────────────────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-bg-primary text-text-primary flex flex-col font-sans">
      {/* ── Top Nav ─────────────────────────────────────────────── */}
      <header className="sticky top-0 z-50 border-b border-border-subtle bg-bg-secondary/90 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center gap-4">
          {/* Brand */}
          <div className="flex items-center gap-3 shrink-0">
            <div className="w-8 h-8 rounded-lg bg-accent-cyan/10 border border-accent-cyan/30 flex items-center justify-center">
              <Film className="w-4 h-4 text-accent-cyan" />
            </div>
            <div className="hidden sm:block">
              <div className="flex items-center gap-2">
                <span className="font-bold tracking-wider text-sm text-white">SHADOW CUT</span>
                <span className="text-[9px] bg-accent-cyan/20 text-accent-cyan px-1.5 py-0.5 rounded-full border border-accent-cyan/30 font-mono">
                  LIVE SET
                </span>
              </div>
              <p className="text-[10px] text-text-secondary leading-none">Night of the Living Dead (1968)</p>
            </div>
          </div>

          {/* Desktop tabs */}
          <nav className="hidden md:flex items-center gap-0.5 bg-[#1a1a24] p-1 rounded-lg border border-border-subtle ml-4 flex-1 justify-center">
            {TABS.map((tab) => {
              const Icon = tab.icon;
              const badge = tab.badge?.(alerts, deviations);
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => navigate(tab.id)}
                  className={[
                    "relative flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md transition",
                    isActive
                      ? "bg-accent-cyan text-black font-semibold"
                      : "text-text-secondary hover:text-text-primary",
                  ].join(" ")}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{tab.label}</span>
                  {badge && badge > 0 && (
                    <span className={[
                      "w-4 h-4 rounded-full flex items-center justify-center text-[9px] font-bold",
                      BADGE_COLORS[tab.id] || "bg-accent-cyan/20 text-accent-cyan",
                    ].join(" ")}>
                      {badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>

          {/* Sync button */}
          <button
            onClick={loadAll}
            className="hidden sm:flex items-center gap-1.5 text-xs bg-[#1a1a24] hover:bg-[#222230] border border-border-subtle px-3 py-2 rounded-lg text-text-secondary hover:text-text-primary transition ml-auto"
          >
            <RefreshCw className={["w-3.5 h-3.5", syncing ? "animate-spin text-accent-cyan" : ""].join(" ")} />
            <span className="hidden lg:inline">Sync Take</span>
          </button>

          {/* Mobile hamburger */}
          <button
            className="md:hidden ml-auto p-2 rounded-lg border border-border-subtle text-text-secondary hover:text-text-primary transition"
            onClick={() => setMobileMenuOpen((v) => !v)}
          >
            {mobileMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
          </button>
        </div>

        {/* Mobile dropdown menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-border-subtle bg-bg-secondary px-4 py-2 space-y-1">
            {TABS.map((tab) => {
              const Icon = tab.icon;
              const badge = tab.badge?.(alerts, deviations);
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => navigate(tab.id)}
                  className={[
                    "w-full flex items-center gap-2 px-3 py-2.5 rounded-lg text-sm transition",
                    isActive ? "bg-accent-cyan text-black font-semibold" : "text-text-secondary hover:text-text-primary hover:bg-white/5",
                  ].join(" ")}
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{tab.label}</span>
                  {badge && badge > 0 && (
                    <span className={["ml-auto w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold", BADGE_COLORS[tab.id] || "bg-accent-cyan/20 text-accent-cyan"].join(" ")}>
                      {badge}
                    </span>
                  )}
                </button>
              );
            })}
            <div className="pt-1 pb-2">
              <button
                onClick={() => { loadAll(); setMobileMenuOpen(false); }}
                className="w-full flex items-center justify-center gap-2 text-xs bg-[#1a1a24] border border-border-subtle px-3 py-2 rounded-lg text-text-secondary"
              >
                <RefreshCw className={["w-3.5 h-3.5", syncing ? "animate-spin text-accent-cyan" : ""].join(" ")} />
                Sync Take
              </button>
            </div>
          </div>
        )}
      </header>

      {/* ── Live status ticker ────────────────────────────────────── */}
      <div className="border-b border-border-subtle bg-[#0d0d16] px-4 sm:px-6 py-1.5 flex items-center gap-4 overflow-x-auto hide-scrollbar text-[10px] font-mono text-text-muted shrink-0">
        <span className="flex items-center gap-1.5 shrink-0">
          <span className="w-1.5 h-1.5 rounded-full bg-severity-critical animate-pulse" />
          <span className="text-severity-critical font-bold">RETAKE @ 37:08</span>
        </span>
        <span className="shrink-0 opacity-40">|</span>
        <span className="shrink-0">Scene 12–16 Farmhouse Siege</span>
        <span className="shrink-0 opacity-40">|</span>
        <span className="shrink-0">{alertCount || 4} flags active</span>
        <span className="shrink-0 opacity-40">|</span>
        <span className="shrink-0 text-severity-success">Shadow online · Model: Gemini 3.1 Pro + Flash Lite</span>
      </div>

      {/* ── Main Content ─────────────────────────────────────────── */}
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 py-6">
        {activeTab === "dashboard" && (
          <DashboardView
            alerts={alerts}
            stats={stats}
            loadingAlerts={syncing}
            onRefresh={loadAll}
            onSelectAlert={(a) => setSelectedAlert(a)}
            onNavigateToAlerts={() => navigate("alerts")}
          />
        )}

        {activeTab === "alerts" && (
          <AlertDetailView
            alerts={alerts}
            selectedAlert={selectedAlert}
            onSelectAlert={(a) => setSelectedAlert(a)}
            userDecisions={userDecisions}
            onDecision={handleDecision}
          />
        )}

        {activeTab === "deviations" && (
          <ScriptDeviationsView deviations={deviations} />
        )}

        {activeTab === "chat" && (
          <ChatView
            messages={chatMessages}
            inputValue={chatInput}
            loading={chatLoading}
            onInputChange={setChatInput}
            onSend={handleSend}
          />
        )}

        {activeTab === "report" && (
          <TrustReportView report={report} />
        )}
      </main>

      {/* ── Footer ──────────────────────────────────────────────── */}
      <footer className="border-t border-border-subtle px-6 py-3 flex flex-wrap items-center justify-between gap-2 text-[10px] text-text-muted font-mono">
        <span>SHADOW CUT · AI Script Supervisor · Powered by Gemini 3.1 Pro + IBM watsonx</span>
        <span>© 2026 · Director retains 100% decision authority</span>
      </footer>
    </div>
  );
}
