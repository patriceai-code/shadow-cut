# Shadow Cut — Judge Q&A Prep
## Anticipated Questions & Bulletproof Answers

---

## CATEGORY 1: Technical Architecture

### Q: "Why YOLO + Gemini instead of just using Gemini alone?"
**A:** "Three reasons. First, cost — YOLO is free and local. Processing every frame through Gemini would cost $200+ per movie. Our cascade costs $7. Second, speed — YOLO runs in real-time on the DIT's laptop. Gemini takes 20-40 seconds per take. Third, verifiability — YOLO gives us structured bounding boxes and confidence scores we can show the director. Gemini alone is a black box. Together, they're transparent and economical."

### Q: "What happens if YOLO misses a prop?"
**A:** "Flash-Lite's job is specifically to catch what YOLO misses. We send Flash-Lite the full video plus YOLO's math and ask: 'Did YOLO miss anything important?' In our tests, YOLO catches ~85% of visible prop changes. Flash-Lite catches another 10%. The remaining 5% are either too subtle for computer vision or genuinely don't matter to the plot. We document this limitation honestly — 95% coverage, not 100%."

### Q: "How do you handle low-light or night shoots where YOLO struggles?"
**A:** "Two things. First, we only send YOLO props from the script vocabulary — it doesn't waste cycles trying to identify unknown objects in bad light. Second, Flash-Lite's semantic analysis compensates. If YOLO says 'I'm 40% confident there's a watch here,' Flash-Lite looks at the frame and says 'Yes, that's a watch, and it's on the right wrist.' The models complement each other's weaknesses."

### Q: "Why Firestore instead of a proper vector database?"
**A:** "For our data volume, Firestore IS a proper vector database. We're storing ~2KB per take. For 500 takes, that's 1MB of structured data. Firestore's native vector search handles this effortlessly. Vertex AI Vector Search is overkill — it has a $0.50/hour minimum and complex setup. For a hackathon and even for indie productions, Firestore is the right tool. We can migrate to Vertex if we scale to blockbusters with 5,000+ takes."

### Q: "What if the director dismisses every alert? Does Shadow become useless?"
**A:** "No — Shadow learns. If the director dismisses 'watch position' alerts three times, Shadow's DirectorTrust score for that category drops from 1.0 to 0.5. Future watch alerts get deprioritized to 'warning' instead of 'critical.' But if the watch is a CRITICAL prop per the Plot Graph, Shadow still flags it — just more quietly. The director can also override the learning in Settings. Shadow adapts, it doesn't give up."

---

## CATEGORY 2: Business & Market

### Q: "Studiovity and ScriptE already exist. How are you different?"
**A:** "Those tools track continuity in scripts and notes. Shadow Cut tracks continuity in pixels. Studiovity flags that 'the letter should be folded' in the script. Shadow Cut sees that the letter is actually open in Take 4 and alerts the director while they're still on set. We're the only tool that processes uploaded footage with computer vision in real-time during production."

### Q: "Who pays for this? Studios or indies?"
**A:** "Both. For indies, $7 per movie is nothing — it's cheaper than one hour of script supervisor time. For studios, the ROI is 7,000x. One prevented reshoot day saves $50,000-$100,000. The script supervisor crisis affects everyone — studios can't hire enough, indies can't afford them. Shadow Cut augments both."

### Q: "What's your moat?"
**A:** "Two things. First, the Plot Knowledge Graph — it's not just prop lists, it's narrative logic. Setup/payoff links, emotional arcs, cross-scene dependencies. That gets better with every script we parse. Second, historical accuracy data. After 10 productions, Shadow knows 'watch position alerts are 94% accurate, performance energy alerts are 72% accurate.' That calibration data is proprietary and improves over time."

### Q: "Why would a director trust an AI over a human script supervisor?"
**A:** "They don't have to choose — Shadow augments, not replaces. The human script supervisor still does what humans do best: creative judgment, actor interaction, on-set diplomacy. Shadow does what humans are bad at: remembering every prop position in every take across 30 days of non-linear shooting. It's a partnership. The director still directs. The Shadow just remembers."

---

## CATEGORY 3: Hackathon & Implementation

### Q: "You had one week with a laptop. How much of this is real vs. mock?"
**A:** "The architecture is real — YOLO runs locally, Gemini API calls work, Firestore stores data, Cloud Run hosts the UI. The mock data proves the pipeline logic. What we need real hardware for is: processing actual 4-minute takes end-to-end, testing latency on real video, and filming the demo clips. The intellectual heavy lifting — prompts, schemas, confidence logic — is done and tested."

### Q: "What if Gemini Flash-Lite hallucinates an alert?"
**A:** "Three safeguards. First, Flash-Lite never works alone — it validates YLO's pre-computed flags, not raw video. Second, the confidence engine requires >85% confidence AND CRITICAL plot weight to trigger a notification. Below that, it's silently logged for chat queries. Third, every alert shows its evidence trail. The director can tap 'Why?' and see the exact frame, bounding box, and script rule. If it's wrong, they dismiss it and Shadow learns."

### Q: "Why IBM Bob? Couldn't you have built this with Copilot or Cursor?"
**A:** "Bob is required for the IBM track, but we went deeper than compliance. Bob's MCP framework IS our runtime architecture. Bob didn't just help us code — Bob built the @tool-decorated MCP servers that our Gemini agents call at runtime. When the director asks a question, the Chat Agent calls Bob's query_memory tool via MCP protocol. That's not 'using an IDE.' That's integrating Bob's agentic infrastructure into our product."

### Q: "What happens if Confluent goes down during the demo?"
**A:** "We have a fallback webhook. If Confluent is unavailable, the Cloud Function that triggers on video upload directly calls POST /webhook/take-uploaded. The pipeline processes identically — same validation, same agents, same alerts. The only difference is the event path. We built this because 'strongly encouraged' doesn't mean 'required to work perfectly during judging.' The fallback is 20 lines of code and zero additional infrastructure."

---

## CATEGORY 4: Edge Cases & Limitations

### Q: "What about actors improvising? Does Shadow flag every change?"
**A:** "No — the Plot Knowledge Graph filters noise. If an actor improvises a line but the prop states are correct, Shadow stays silent. It only flags deviations from the script's CRITICAL rules. If the improvisation changes a prop state — e.g., the actor opens a letter that should stay folded — THEN it alerts. The script is the filter, not the prison."

### Q: "How do you handle CGI/VFX shots where props don't physically exist?"
**A:** "Shadow processes uploaded footage. If the prop is a VFX element not yet composited, YOLO won't see it and won't flag it. That's correct — there's nothing to track yet. For hybrid shots with practical props and VFX elements, YOLO tracks the practical props and Shadow flags those. VFX continuity is handled in post by the VFX supervisor with different tools. Shadow focuses on what the camera actually sees."

### Q: "What about costume and makeup continuity?"
**A:** "YOLO-World is open-vocabulary — we can add 'scar,' 'tattoo,' 'blood stain' to the script vocabulary and track them like any prop. In v1, we focused on props because they're the highest-frequency continuity errors. Costume and makeup tracking is on the roadmap and uses the same architecture — just different object classes."

### Q: "Your latency is 20-40 seconds per take. Is that fast enough?"
**A:** "For a proof-of-concept, yes. The DIT uploads a take, Shadow processes it in the background, and the director gets a notification if something matters. They're not staring at a loading screen — they're directing the next shot. In production, we'd parallelize: YOLO runs on the DIT cart in real-time, Flash-Lite processes in the cloud, and alerts arrive within 5-10 seconds of upload. The 20-40 second figure is for the hackathon demo on standard hardware."

---

## CATEGORY 5: The Killer Questions (If Judges Are Impressed)

### Q: "If you won $7,500, what would you build next?"
**A:** "Three things. First, edge deployment — run Gemma 4 on the DIT's laptop for zero-latency processing and zero cloud cost. Second, multi-camera sync — track the same prop across 3-4 simultaneous camera angles. Third, editor integration — export Shadow's data directly into Premiere Pro as markers, so the editor sees continuity alerts while assembling the rough cut."

### Q: "Why should we pick you over a team of 5 people?"
**A:** "Because I had to think harder. A team of 5 can divide frontend, backend, demo video, and docs. I had to design an architecture so clean that one person with one week could build it. That constraint produced a simpler, more focused product. Every feature justifies its existence in the 3-minute demo. There's no bloat, no 'nice-to-haves,' no scope creep. Shadow Cut is what happens when you have to be ruthless about what matters."

### Q: "What's the biggest thing you learned?"
**A:** "That the demo video is 40% of the decision. I spent weeks on architecture, but the 3-minute video is what judges actually watch. If I could do it again, I'd storyboard the video on Day 1 and build the product to fit the narrative — not the other way around. The best hackathon projects aren't the most complex. They're the ones that tell the clearest story in 3 minutes."

---

## DELIVERY TIPS

- **Keep answers under 30 seconds.** Judges have limited attention.
- **Lead with the number.** "$7 per movie, 7,000x ROI" is more memorable than paragraphs.
- **Admit limitations proudly.** "YOLO catches 95%, not 100%" builds more trust than claiming perfection.
- **Reference the demo.** "If you look at the alert card at 1:15 in our video..."
- **Smile when you say the tagline.** "The director still directs. The Shadow just remembers."

---

*Practice these out loud. Twice. The difference between a good answer and a winning answer is confidence, not content.*
