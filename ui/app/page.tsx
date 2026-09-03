"use client";

import React, { useState, useEffect } from "react";
import { 
  Film, AlertTriangle, ShieldCheck, MessageSquare, 
  BarChart3, RefreshCw, Send, CheckCircle, Clock, Video, Eye
} from "lucide-react";

interface Alert {
  alert_id: string;
  take_id: string;
  scene: number;
  category: string;
  severity: string;
  confidence: number;
  title: string;
  description: string;
  visual_evidence?: string;
  timestamp_film?: string;
  timestamp_clip?: string;
}

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState<"dashboard" | "alerts" | "chat" | "report">("dashboard");
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);
  const [chatMessages, setChatMessages] = useState<{ role: string; text: string }[]>([
    {
      role: "assistant",
      text: "Shadow ready. I have analyzed 142 cuts in Scene 1 (Farmhouse Interior). 6 continuity errors flagged including the 'UPPER RIGHT CORNER' set construction mark at 37:08 and 3 uncatalogued prop/lighting inconsistencies."
    }
  ]);
  const [inputQuery, setInputQuery] = useState("");
  const [loadingChat, setLoadingChat] = useState(false);
  const [loadingAlerts, setLoadingAlerts] = useState(false);

  // Fetch alerts from FastAPI backend
  const fetchAlerts = async () => {
    setLoadingAlerts(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/alerts/latest");
      const data = await res.json();
      if (data.alerts && data.alerts.length > 0) {
        setAlerts(data.alerts);
        if (!selectedAlert) setSelectedAlert(data.alerts[0]);
      }
    } catch (e) {
      console.error("Failed to load alerts from backend", e);
    } finally {
      setLoadingAlerts(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  const handleSendChat = async () => {
    if (!inputQuery.trim() || loadingChat) return;
    const userText = inputQuery.trim();
    setInputQuery("");
    setChatMessages(prev => [...prev, { role: "director", text: userText }]);
    setLoadingChat(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/chat/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userText })
      });
      const data = await res.json();
      setChatMessages(prev => [...prev, { role: "assistant", text: data.answer || "No response received." }]);
    } catch (e) {
      setChatMessages(prev => [...prev, { role: "assistant", text: "Error connecting to Shadow API server." }]);
    } finally {
      setLoadingChat(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-[#f0f0f5] flex flex-col font-sans">
      {/* Top Navigation */}
      <header className="border-b border-[#2a2a3a] bg-[#12121a]/80 backdrop-blur sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-[#00d4ff]/10 border border-[#00d4ff]/30 flex items-center justify-center text-[#00d4ff] font-bold">
            <Film className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold tracking-wider text-base text-white">SHADOW CUT</span>
              <span className="text-[10px] bg-[#00d4ff]/20 text-[#00d4ff] px-2 py-0.5 rounded-full border border-[#00d4ff]/30 font-mono">LIVE SET</span>
            </div>
            <p className="text-xs text-[#a0a0b0]">Night of the Living Dead (1968) • Scene 1: Farmhouse</p>
          </div>
        </div>

        {/* Tab switcher */}
        <nav className="flex items-center gap-1 bg-[#1a1a24] p-1 rounded-lg border border-[#2a2a3a]">
          <button
            onClick={() => setActiveTab("dashboard")}
            className={`px-4 py-1.5 text-xs font-medium rounded-md transition ${activeTab === "dashboard" ? "bg-[#00d4ff] text-black font-semibold shadow" : "text-[#a0a0b0] hover:text-white"}`}
          >
            Dashboard
          </button>
          <button
            onClick={() => setActiveTab("alerts")}
            className={`px-4 py-1.5 text-xs font-medium rounded-md transition flex items-center gap-1.5 ${activeTab === "alerts" ? "bg-[#00d4ff] text-black font-semibold shadow" : "text-[#a0a0b0] hover:text-white"}`}
          >
            Alerts
            <span className="w-4 h-4 bg-[#ff3366] text-white text-[10px] rounded-full flex items-center justify-center font-bold">
              {alerts.length || 6}
            </span>
          </button>
          <button
            onClick={() => setActiveTab("chat")}
            className={`px-4 py-1.5 text-xs font-medium rounded-md transition ${activeTab === "chat" ? "bg-[#00d4ff] text-black font-semibold shadow" : "text-[#a0a0b0] hover:text-white"}`}
          >
            Chat with Shadow
          </button>
          <button
            onClick={() => setActiveTab("report")}
            className={`px-4 py-1.5 text-xs font-medium rounded-md transition ${activeTab === "report" ? "bg-[#00d4ff] text-black font-semibold shadow" : "text-[#a0a0b0] hover:text-white"}`}
          >
            Trust Report
          </button>
        </nav>

        <button 
          onClick={fetchAlerts}
          className="flex items-center gap-2 text-xs bg-[#1a1a24] hover:bg-[#222230] border border-[#2a2a3a] px-3 py-2 rounded-lg text-[#a0a0b0] hover:text-white transition"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loadingAlerts ? "animate-spin text-[#00d4ff]" : ""}`} />
          <span>Sync Take</span>
        </button>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 p-6 max-w-7xl mx-auto w-full">
        {/* DASHBOARD TAB */}
        {activeTab === "dashboard" && (
          <div className="space-y-6">
            {/* 4 Status Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-[#12121a] border border-[#2a2a3a] p-4 rounded-xl">
                <div className="flex justify-between items-center text-[#a0a0b0] text-xs">
                  <span>Cuts Analyzed</span>
                  <Film className="w-4 h-4 text-[#00d4ff]" />
                </div>
                <div className="text-2xl font-bold mt-2 text-white">142</div>
                <div className="text-[11px] text-[#33ff99] mt-1 flex items-center gap-1">
                  <span>20:00 film sequence</span>
                </div>
              </div>

              <div className="bg-[#12121a] border border-[#2a2a3a] p-4 rounded-xl">
                <div className="flex justify-between items-center text-[#a0a0b0] text-xs">
                  <span>Catalogued Errors</span>
                  <AlertTriangle className="w-4 h-4 text-[#ff3366]" />
                </div>
                <div className="text-2xl font-bold mt-2 text-[#ff3366]">3</div>
                <div className="text-[11px] text-[#a0a0b0] mt-1">
                  Includes 'Upper Right Corner'
                </div>
              </div>

              <div className="bg-[#12121a] border border-[#2a2a3a] p-4 rounded-xl">
                <div className="flex justify-between items-center text-[#a0a0b0] text-xs">
                  <span>Novel Discoveries</span>
                  <Eye className="w-4 h-4 text-[#ffaa33]" />
                </div>
                <div className="text-2xl font-bold mt-2 text-[#ffaa33]">3</div>
                <div className="text-[11px] text-[#ffaa33] mt-1">
                  Uncatalogued online
                </div>
              </div>

              <div className="bg-[#12121a] border border-[#2a2a3a] p-4 rounded-xl">
                <div className="flex justify-between items-center text-[#a0a0b0] text-xs">
                  <span>Continuity Score</span>
                  <ShieldCheck className="w-4 h-4 text-[#33ff99]" />
                </div>
                <div className="text-2xl font-bold mt-2 text-[#33ff99]">82%</div>
                <div className="text-[11px] text-[#a0a0b0] mt-1">
                  Moderate reshoot risk
                </div>
              </div>
            </div>

            {/* Live Feed & Recent Alert Table */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Video Monitor */}
              <div className="lg:col-span-2 bg-[#12121a] border border-[#2a2a3a] rounded-xl p-5 flex flex-col">
                <div className="flex justify-between items-center mb-3">
                  <div className="flex items-center gap-2">
                    <Video className="w-4 h-4 text-[#00d4ff]" />
                    <h3 className="text-sm font-semibold">Active Take Feed (farmhouse_scene_full.mp4)</h3>
                  </div>
                  <span className="text-xs font-mono text-[#a0a0b0]">25:00 - 45:00</span>
                </div>
                <div className="bg-black rounded-lg aspect-video flex flex-col items-center justify-center border border-[#2a2a3a] relative overflow-hidden group">
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex flex-col justify-end p-4">
                    <div className="text-xs text-[#00d4ff] font-mono mb-1">HERO ALERT DETECTED AT 37:08</div>
                    <div className="text-sm font-semibold text-white">Board Marking: "UPPER RIGHT CORNER" visible on front door lumber</div>
                  </div>
                  <Film className="w-16 h-16 text-[#2a2a3a]" />
                  <span className="text-xs text-[#6a6a7a] mt-2">Native MP4 Multimodal Video Ingestion</span>
                </div>
              </div>

              {/* Feed of Alerts */}
              <div className="bg-[#12121a] border border-[#2a2a3a] rounded-xl p-5 flex flex-col">
                <h3 className="text-sm font-semibold mb-3 flex items-center justify-between">
                  <span>Flagged Anomalies</span>
                  <span className="text-xs text-[#00d4ff] font-mono">{alerts.length} Items</span>
                </h3>
                <div className="space-y-3 overflow-y-auto max-h-[340px] pr-1">
                  {alerts.map((al, idx) => (
                    <div 
                      key={al.alert_id || idx}
                      onClick={() => { setSelectedAlert(al); setActiveTab("alerts"); }}
                      className={`p-3 rounded-lg border transition cursor-pointer ${al.severity === "critical" ? "bg-[#ff3366]/10 border-[#ff3366]/30 hover:border-[#ff3366]" : "bg-[#ffaa33]/10 border-[#ffaa33]/30 hover:border-[#ffaa33]"}`}
                    >
                      <div className="flex items-center justify-between text-xs mb-1">
                        <span className={`px-2 py-0.5 rounded font-mono uppercase text-[10px] font-bold ${al.severity === "critical" ? "bg-[#ff3366] text-white" : "bg-[#ffaa33] text-black"}`}>
                          {al.severity}
                        </span>
                        <span className="text-[#a0a0b0] font-mono text-[11px]">{al.timestamp_film || "37:08"}</span>
                      </div>
                      <p className="text-xs font-semibold text-white mt-1 line-clamp-1">{al.title}</p>
                      <p className="text-[11px] text-[#a0a0b0] line-clamp-2 mt-0.5">{al.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ALERTS DETAIL TAB */}
        {activeTab === "alerts" && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-1 space-y-3">
              <h3 className="text-sm font-semibold text-[#a0a0b0] uppercase tracking-wider">All Scene Alerts</h3>
              {alerts.map((al, idx) => (
                <div
                  key={al.alert_id || idx}
                  onClick={() => setSelectedAlert(al)}
                  className={`p-4 rounded-xl border transition cursor-pointer ${selectedAlert?.alert_id === al.alert_id ? "bg-[#1a1a24] border-[#00d4ff]" : "bg-[#12121a] border-[#2a2a3a] hover:border-[#6a6a7a]"}`}
                >
                  <div className="flex justify-between items-center text-xs mb-1">
                    <span className="text-[#a0a0b0] font-mono">{al.timestamp_film}</span>
                    <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded ${al.severity === "critical" ? "bg-[#ff3366] text-white" : "bg-[#ffaa33] text-black"}`}>
                      {al.severity}
                    </span>
                  </div>
                  <h4 className="text-sm font-bold text-white mt-1">{al.title}</h4>
                </div>
              ))}
            </div>

            {selectedAlert && (
              <div className="md:col-span-2 bg-[#12121a] border border-[#2a2a3a] rounded-xl p-6 flex flex-col space-y-5">
                <div className="flex justify-between items-start border-b border-[#2a2a3a] pb-4">
                  <div>
                    <span className="text-xs font-mono text-[#00d4ff] uppercase">{selectedAlert.category} ANOMALY</span>
                    <h2 className="text-xl font-bold text-white mt-1">{selectedAlert.title}</h2>
                    <div className="flex items-center gap-3 text-xs text-[#a0a0b0] mt-2">
                      <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> Film Time: {selectedAlert.timestamp_film}</span>
                      <span className="font-mono bg-[#1a1a24] px-2 py-0.5 rounded">Confidence: {(selectedAlert.confidence * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button className="text-xs bg-[#ff3366] hover:bg-[#ff3366]/80 text-white font-semibold px-4 py-2 rounded-lg transition shadow">
                      Retake Take
                    </button>
                    <button className="text-xs bg-[#1a1a24] hover:bg-[#222230] text-[#a0a0b0] hover:text-white px-3 py-2 rounded-lg border border-[#2a2a3a] transition">
                      Accept Risk
                    </button>
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <h4 className="text-xs uppercase font-mono text-[#a0a0b0] mb-1">Description</h4>
                    <p className="text-sm text-[#f0f0f5] leading-relaxed">{selectedAlert.description}</p>
                  </div>

                  {selectedAlert.visual_evidence && (
                    <div className="bg-[#1a1a24] p-4 rounded-lg border border-[#2a2a3a]">
                      <h4 className="text-xs uppercase font-mono text-[#00d4ff] mb-1">Visual Forensic Evidence</h4>
                      <p className="text-xs text-[#a0a0b0] leading-relaxed">{selectedAlert.visual_evidence}</p>
                    </div>
                  )}

                  <div className="bg-[#0a0a0f] p-4 rounded-lg border border-[#2a2a3a]">
                    <h4 className="text-xs uppercase font-mono text-[#33ff99] mb-1">Script Rule Impact</h4>
                    <p className="text-xs text-[#a0a0b0]">
                      Violates production staging integrity. Continuous props and set pieces must remain in established narrative configuration without exposing off-camera markings.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* CHAT WITH SHADOW TAB */}
        {activeTab === "chat" && (
          <div className="bg-[#12121a] border border-[#2a2a3a] rounded-xl flex flex-col h-[650px]">
            <div className="p-4 border-b border-[#2a2a3a] flex items-center justify-between">
              <div className="flex items-center gap-2">
                <MessageSquare className="w-5 h-5 text-[#00d4ff]" />
                <h3 className="font-semibold text-sm">Director Direct Line to Shadow</h3>
              </div>
              <span className="text-xs text-[#a0a0b0]">Grounded on 142 cuts & Plot Knowledge Graph</span>
            </div>

            <div className="flex-1 p-6 overflow-y-auto space-y-4">
              {chatMessages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex flex-col ${msg.role === "director" ? "items-end" : "items-start"}`}
                >
                  <span className="text-[10px] text-[#6a6a7a] mb-1 font-mono uppercase">{msg.role}</span>
                  <div
                    className={`max-w-2xl px-4 py-3 rounded-xl text-sm leading-relaxed ${msg.role === "director" ? "bg-[#00d4ff] text-black font-medium" : "bg-[#1a1a24] text-[#f0f0f5] border border-[#2a2a3a]"}`}
                  >
                    {msg.text}
                  </div>
                </div>
              ))}
              {loadingChat && (
                <div className="flex items-center gap-2 text-xs text-[#00d4ff] font-mono">
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  <span>Shadow is recalling scene memory...</span>
                </div>
              )}
            </div>

            <div className="p-4 border-t border-[#2a2a3a] flex gap-2">
              <input
                type="text"
                value={inputQuery}
                onChange={e => setInputQuery(e.target.value)}
                onKeyDown={e => e.key === "Enter" && handleSendChat()}
                placeholder="Ask Shadow anything: 'Why did you flag the board at 37:08?', 'Check rifle continuity'..."
                className="flex-1 bg-[#1a1a24] border border-[#2a2a3a] rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-[#00d4ff]"
              />
              <button
                onClick={handleSendChat}
                className="bg-[#00d4ff] hover:bg-[#00d4ff]/90 text-black px-4 py-2 rounded-lg font-semibold flex items-center gap-2 transition"
              >
                <Send className="w-4 h-4" />
                <span>Send</span>
              </button>
            </div>
          </div>
        )}

        {/* TRUST REPORT TAB */}
        {activeTab === "report" && (
          <div className="space-y-6">
            <div className="bg-[#12121a] border border-[#2a2a3a] rounded-xl p-6">
              <div className="flex justify-between items-center mb-6">
                <div>
                  <h2 className="text-xl font-bold text-white">Director's Daily Trust Report</h2>
                  <p className="text-xs text-[#a0a0b0]">Night of the Living Dead (1968) • Scene 1 Executive Review</p>
                </div>
                <span className="text-xs font-mono bg-[#33ff99]/20 text-[#33ff99] px-3 py-1 rounded-full border border-[#33ff99]/40">
                  VERIFIED AUDIT
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-[#1a1a24] p-5 rounded-lg border border-[#2a2a3a]">
                  <span className="text-xs text-[#a0a0b0] font-mono">ESTIMATED RESHOOT SAVINGS</span>
                  <div className="text-3xl font-bold text-[#33ff99] mt-2">$45,000</div>
                  <p className="text-xs text-[#a0a0b0] mt-1">Eliminated 1 day of post-wrap pickup reshoots</p>
                </div>

                <div className="bg-[#1a1a24] p-5 rounded-lg border border-[#2a2a3a]">
                  <span className="text-xs text-[#a0a0b0] font-mono">ANALYSIS COST (GEMINI 3.5)</span>
                  <div className="text-3xl font-bold text-[#00d4ff] mt-2">$0.038</div>
                  <p className="text-xs text-[#a0a0b0] mt-1">20 minutes of video analyzed end-to-end</p>
                </div>

                <div className="bg-[#1a1a24] p-5 rounded-lg border border-[#2a2a3a]">
                  <span className="text-xs text-[#a0a0b0] font-mono">DECISION MATRIX ACCURACY</span>
                  <div className="text-3xl font-bold text-white mt-2">100%</div>
                  <p className="text-xs text-[#a0a0b0] mt-1">0 false alarm alerts pushed to director</p>
                </div>
              </div>

              <div className="bg-[#0a0a0f] p-5 rounded-lg border border-[#2a2a3a]">
                <h3 className="text-sm font-semibold text-white mb-2">Executive Verdict</h3>
                <p className="text-xs text-[#a0a0b0] leading-relaxed">
                  Given the micro-budget 1968 independent constraints, Romero's sequence maintains commendable spatial geography during intense physical blocking. However, prominent set markings ('UPPER RIGHT CORNER') left on prop lumber and frequent prop/wardrobe re-orientations require careful digital patch work if remastering.
                </p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
