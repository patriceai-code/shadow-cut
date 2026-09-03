"use client";

import React, { useState, useEffect } from "react";
import { 
  Film, AlertTriangle, ShieldCheck, MessageSquare, 
  RefreshCw, Send, Clock, Video, Eye, FileText, CheckCircle2, XCircle
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
  technical_impact?: string;
  director_action_required?: string;
  timestamp_film?: string;
  timestamp_clip?: string;
}

interface ScriptDeviation {
  timestamp_film: string;
  scripted_element: string;
  filmed_reality: string;
  severity: string;
  objective_impact: string;
}

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState<"dashboard" | "alerts" | "deviations" | "chat" | "report">("dashboard");
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [deviations, setDeviations] = useState<ScriptDeviation[]>([]);
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);
  const [chatMessages, setChatMessages] = useState<{ role: string; text: string }[]>([
    {
      role: "assistant",
      text: "Shadow ready. Screenplay Scene 12-16 (Farmhouse Siege) cross-referenced against 142 cuts. 1 CRITICAL error flagged for RETAKE ('UPPER RIGHT CORNER' crew board marking at 37:08, 100% confidence), 2 items flagged for DIRECTOR REVIEW, and 1 actor performance script deviation noted."
    }
  ]);
  const [inputQuery, setInputQuery] = useState("");
  const [loadingChat, setLoadingChat] = useState(false);
  const [loadingAlerts, setLoadingAlerts] = useState(false);
  const [userDecisions, setUserDecisions] = useState<{ [id: string]: string }>({});

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

  const fetchDeviations = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/script/deviations");
      const data = await res.json();
      if (data.deviations) {
        setDeviations(data.deviations);
      }
    } catch (e) {
      console.error("Failed to load script deviations", e);
    }
  };

  useEffect(() => {
    fetchAlerts();
    fetchDeviations();
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

  const recordDecision = (alertId: string, decision: "retake" | "accept" | "dismiss") => {
    setUserDecisions(prev => ({ ...prev, [alertId]: decision }));
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
            <p className="text-xs text-[#a0a0b0]">Night of the Living Dead (1968) • Script-Grounded Supervision</p>
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
            Continuity Alerts
            <span className="w-4 h-4 bg-[#ff3366] text-white text-[10px] rounded-full flex items-center justify-center font-bold">
              {alerts.length || 4}
            </span>
          </button>
          <button
            onClick={() => setActiveTab("deviations")}
            className={`px-4 py-1.5 text-xs font-medium rounded-md transition flex items-center gap-1.5 ${activeTab === "deviations" ? "bg-[#00d4ff] text-black font-semibold shadow" : "text-[#a0a0b0] hover:text-white"}`}
          >
            Script Deviations
            <span className="w-4 h-4 bg-[#ffaa33] text-black text-[10px] rounded-full flex items-center justify-center font-bold">
              {deviations.length || 2}
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

              <div className="bg-[#12121a] border border-[#ff3366]/40 p-4 rounded-xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-16 h-16 bg-[#ff3366]/10 rounded-bl-full pointer-events-none" />
                <div className="flex justify-between items-center text-[#a0a0b0] text-xs">
                  <span>Retake Required</span>
                  <AlertTriangle className="w-4 h-4 text-[#ff3366]" />
                </div>
                <div className="text-2xl font-bold mt-2 text-[#ff3366]">1</div>
                <div className="text-[11px] text-[#ff3366] font-mono mt-1">
                  37:08 'UPPER RIGHT CORNER'
                </div>
              </div>

              <div className="bg-[#12121a] border border-[#ffaa33]/40 p-4 rounded-xl">
                <div className="flex justify-between items-center text-[#a0a0b0] text-xs">
                  <span>Director Review</span>
                  <Eye className="w-4 h-4 text-[#ffaa33]" />
                </div>
                <div className="text-2xl font-bold mt-2 text-[#ffaa33]">2</div>
                <div className="text-[11px] text-[#a0a0b0] mt-1">
                  Lighter Fluid & Footwear
                </div>
              </div>

              <div className="bg-[#12121a] border border-[#2a2a3a] p-4 rounded-xl">
                <div className="flex justify-between items-center text-[#a0a0b0] text-xs">
                  <span>Script Compliance</span>
                  <FileText className="w-4 h-4 text-[#00d4ff]" />
                </div>
                <div className="text-2xl font-bold mt-2 text-[#00d4ff]">84%</div>
                <div className="text-[11px] text-[#a0a0b0] mt-1">
                  Table action modified
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
                    <h3 className="text-sm font-semibold">Take Monitor (Scene 12-16 Farmhouse Siege)</h3>
                  </div>
                  <span className="text-xs font-mono text-[#a0a0b0]">25:00 - 45:00</span>
                </div>
                <div className="bg-black rounded-lg aspect-video flex flex-col items-center justify-center border border-[#2a2a3a] relative overflow-hidden group">
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex flex-col justify-end p-4">
                    <div className="text-xs text-[#ff3366] font-mono mb-1 font-bold">🚨 RETAKE REQUIRED AT 37:08 (100% CONFIDENCE)</div>
                    <div className="text-sm font-semibold text-white">Visible Crew Handwriting on Barricade Plank: 'UPPER RIGHT CORNER'</div>
                  </div>
                  <Film className="w-16 h-16 text-[#2a2a3a]" />
                  <span className="text-xs text-[#6a6a7a] mt-2">Screenplay-Grounded Multimodal Video Pipeline</span>
                </div>
              </div>

              {/* Feed of Alerts */}
              <div className="bg-[#12121a] border border-[#2a2a3a] rounded-xl p-5 flex flex-col">
                <h3 className="text-sm font-semibold mb-3 flex items-center justify-between">
                  <span>Flagged Continuity Queue</span>
                  <span className="text-xs text-[#00d4ff] font-mono">{alerts.length} Items</span>
                </h3>
                <div className="space-y-3 overflow-y-auto max-h-[340px] pr-1">
                  {alerts.map((al, idx) => (
                    <div 
                      key={al.alert_id || idx}
                      onClick={() => { setSelectedAlert(al); setActiveTab("alerts"); }}
                      className={`p-3 rounded-lg border transition cursor-pointer ${al.director_action_required === "RETAKE REQUIRED" ? "bg-[#ff3366]/10 border-[#ff3366]/50 hover:border-[#ff3366]" : "bg-[#1a1a24] border-[#2a2a3a] hover:border-[#6a6a7a]"}`}
                    >
                      <div className="flex items-center justify-between text-xs mb-1">
                        <span className={`px-2 py-0.5 rounded font-mono uppercase text-[10px] font-bold ${al.director_action_required === "RETAKE REQUIRED" ? "bg-[#ff3366] text-white animate-pulse" : al.director_action_required === "DIRECTOR REVIEW REQUIRED" ? "bg-[#ffaa33] text-black" : "bg-[#2a2a3a] text-[#a0a0b0]"}`}>
                          {al.director_action_required || al.severity}
                        </span>
                        <span className="text-[#a0a0b0] font-mono text-[11px]">{al.timestamp_film}</span>
                      </div>
                      <p className="text-xs font-semibold text-white mt-1 line-clamp-1">{al.title}</p>
                      <p className="text-[11px] text-[#a0a0b0] line-clamp-2 mt-0.5">{al.visual_evidence || al.description}</p>
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
              <h3 className="text-sm font-semibold text-[#a0a0b0] uppercase tracking-wider">Continuity Queue</h3>
              {alerts.map((al, idx) => (
                <div
                  key={al.alert_id || idx}
                  onClick={() => setSelectedAlert(al)}
                  className={`p-4 rounded-xl border transition cursor-pointer ${selectedAlert?.alert_id === al.alert_id ? "bg-[#1a1a24] border-[#00d4ff]" : "bg-[#12121a] border-[#2a2a3a] hover:border-[#6a6a7a]"}`}
                >
                  <div className="flex justify-between items-center text-xs mb-1">
                    <span className="text-[#a0a0b0] font-mono">{al.timestamp_film}</span>
                    <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded ${al.director_action_required === "RETAKE REQUIRED" ? "bg-[#ff3366] text-white" : al.director_action_required === "DIRECTOR REVIEW REQUIRED" ? "bg-[#ffaa33] text-black" : "bg-[#2a2a3a] text-[#a0a0b0]"}`}>
                      {al.director_action_required || al.severity}
                    </span>
                  </div>
                  <h4 className="text-sm font-bold text-white mt-1">{al.title}</h4>
                  {userDecisions[al.alert_id] && (
                    <div className="mt-2 text-[10px] font-mono uppercase text-[#00d4ff] flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" />
                      <span>Director Decision: {userDecisions[al.alert_id]}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {selectedAlert && (
              <div className="md:col-span-2 bg-[#12121a] border border-[#2a2a3a] rounded-xl p-6 flex flex-col space-y-5">
                <div className="flex justify-between items-start border-b border-[#2a2a3a] pb-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono text-[#00d4ff] uppercase">{selectedAlert.category} AUDIT</span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase ${selectedAlert.director_action_required === "RETAKE REQUIRED" ? "bg-[#ff3366] text-white" : "bg-[#ffaa33] text-black"}`}>
                        {selectedAlert.director_action_required}
                      </span>
                    </div>
                    <h2 className="text-xl font-bold text-white mt-1">{selectedAlert.title}</h2>
                    <div className="flex items-center gap-3 text-xs text-[#a0a0b0] mt-2">
                      <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> Film Time: {selectedAlert.timestamp_film}</span>
                      <span className="font-mono bg-[#1a1a24] px-2 py-0.5 rounded">Confidence: {(selectedAlert.confidence * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                  
                  {/* Human-in-the-Loop Director Action Buttons */}
                  <div className="flex gap-2">
                    <button 
                      onClick={() => recordDecision(selectedAlert.alert_id, "retake")}
                      className={`text-xs font-semibold px-4 py-2 rounded-lg transition shadow flex items-center gap-1.5 ${userDecisions[selectedAlert.alert_id] === "retake" ? "bg-[#ff3366] text-white ring-2 ring-white" : "bg-[#ff3366]/90 hover:bg-[#ff3366] text-white"}`}
                    >
                      <XCircle className="w-3.5 h-3.5" />
                      <span>Retake Take</span>
                    </button>
                    <button 
                      onClick={() => recordDecision(selectedAlert.alert_id, "accept")}
                      className={`text-xs px-3 py-2 rounded-lg border border-[#2a2a3a] transition flex items-center gap-1.5 ${userDecisions[selectedAlert.alert_id] === "accept" ? "bg-[#00d4ff] text-black font-semibold" : "bg-[#1a1a24] hover:bg-[#222230] text-[#a0a0b0] hover:text-white"}`}
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Accept Risk</span>
                    </button>
                    <button 
                      onClick={() => recordDecision(selectedAlert.alert_id, "dismiss")}
                      className="text-xs bg-[#1a1a24] hover:bg-[#222230] text-[#6a6a7a] hover:text-[#a0a0b0] px-3 py-2 rounded-lg border border-[#2a2a3a] transition"
                    >
                      Dismiss
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
                      <h4 className="text-xs uppercase font-mono text-[#00d4ff] mb-1">Objective Forensic Evidence</h4>
                      <p className="text-xs text-[#a0a0b0] leading-relaxed">{selectedAlert.visual_evidence}</p>
                    </div>
                  )}

                  {selectedAlert.technical_impact && (
                    <div className="bg-[#0a0a0f] p-4 rounded-lg border border-[#2a2a3a]">
                      <h4 className="text-xs uppercase font-mono text-[#ffaa33] mb-1">Technical & Narrative Impact</h4>
                      <p className="text-xs text-[#a0a0b0] leading-relaxed">{selectedAlert.technical_impact}</p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* SCRIPT DEVIATIONS TAB */}
        {activeTab === "deviations" && (
          <div className="space-y-6">
            <div className="bg-[#12121a] border border-[#2a2a3a] rounded-xl p-6">
              <div className="flex justify-between items-center mb-4">
                <div>
                  <h2 className="text-xl font-bold text-white">Screenplay vs Filmed Performance Deviations</h2>
                  <p className="text-xs text-[#a0a0b0]">Grounded cross-reference against Romero & Russo (1968) Shooting Screenplay</p>
                </div>
                <span className="text-xs font-mono bg-[#00d4ff]/20 text-[#00d4ff] px-3 py-1 rounded-full border border-[#00d4ff]/40">
                  SCRIPT AUDIT ACTIVE
                </span>
              </div>

              <div className="space-y-4">
                {deviations.map((dev, idx) => (
                  <div key={idx} className="bg-[#1a1a24] border border-[#2a2a3a] rounded-lg p-4 space-y-2">
                    <div className="flex justify-between items-center text-xs">
                      <span className="font-mono text-[#00d4ff]">{dev.timestamp_film}</span>
                      <span className={`uppercase text-[10px] font-bold px-2 py-0.5 rounded ${dev.severity === "warning" ? "bg-[#ffaa33] text-black" : "bg-[#2a2a3a] text-[#a0a0b0]"}`}>
                        {dev.severity}
                      </span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-2">
                      <div className="bg-[#0a0a0f] p-3 rounded border border-[#2a2a3a]">
                        <span className="text-[10px] font-mono text-[#a0a0b0] block mb-1 uppercase">Written in Screenplay</span>
                        <p className="text-xs text-white">{dev.scripted_element}</p>
                      </div>
                      <div className="bg-[#0a0a0f] p-3 rounded border border-[#2a2a3a]">
                        <span className="text-[10px] font-mono text-[#33ff99] block mb-1 uppercase">Performed on Camera</span>
                        <p className="text-xs text-[#f0f0f5]">{dev.filmed_reality}</p>
                      </div>
                    </div>
                    <p className="text-xs text-[#a0a0b0] italic pt-1">{dev.objective_impact}</p>
                  </div>
                ))}
              </div>
            </div>
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
              <span className="text-xs text-[#a0a0b0]">Grounded on 1968 Screenplay & 142 Film Cuts</span>
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
                  <span>Shadow is recalling screenplay memory...</span>
                </div>
              )}
            </div>

            <div className="p-4 border-t border-[#2a2a3a] flex gap-2">
              <input
                type="text"
                value={inputQuery}
                onChange={e => setInputQuery(e.target.value)}
                onKeyDown={e => e.key === "Enter" && handleSendChat()}
                placeholder="Ask Shadow: 'Why is 37:08 a retake?', 'Did Ben follow the script for the table?'..."
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
                  <p className="text-xs text-[#a0a0b0]">Night of the Living Dead (1968) • Scene 12-16 Executive Audit</p>
                </div>
                <span className="text-xs font-mono bg-[#33ff99]/20 text-[#33ff99] px-3 py-1 rounded-full border border-[#33ff99]/40">
                  SCRIPT-GROUNDED AUDIT
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-[#1a1a24] p-5 rounded-lg border border-[#2a2a3a]">
                  <span className="text-xs text-[#a0a0b0] font-mono">ESTIMATED RESHOOT SAVINGS</span>
                  <div className="text-3xl font-bold text-[#33ff99] mt-2">$45,000</div>
                  <p className="text-xs text-[#a0a0b0] mt-1">Eliminated 1 day of post-wrap pickup reshoots</p>
                </div>

                <div className="bg-[#1a1a24] p-5 rounded-lg border border-[#2a2a3a]">
                  <span className="text-xs text-[#a0a0b0] font-mono">COMPUTE COST (GEMINI 3.5)</span>
                  <div className="text-3xl font-bold text-[#00d4ff] mt-2">$0.046</div>
                  <p className="text-xs text-[#a0a0b0] mt-1">20 minutes of footage audited with screenplay</p>
                </div>

                <div className="bg-[#1a1a24] p-5 rounded-lg border border-[#2a2a3a]">
                  <span className="text-xs text-[#a0a0b0] font-mono">DIRECTOR AUTONOMY RATING</span>
                  <div className="text-3xl font-bold text-white mt-2">100%</div>
                  <p className="text-xs text-[#a0a0b0] mt-1">AI provides evidence; director exercises decision</p>
                </div>
              </div>

              <div className="bg-[#0a0a0f] p-5 rounded-lg border border-[#2a2a3a]">
                <h3 className="text-sm font-semibold text-white mb-2">Executive Verdict</h3>
                <p className="text-xs text-[#a0a0b0] leading-relaxed">
                  Comprehensive audit of the 20-minute Farmhouse Siege sequence reveals several notable script deviations and severe production continuity errors. Most critically, an unmasked production marking ('UPPER RIGHT CORNER') is visibly written on a reinforcement wood plank during the living room boarding scene. Wardrobe and prop tracking show occasional discrepancies, notably Barbra's footwear states and the Charcoal Lighter fluid container placement across cuts.
                </p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
