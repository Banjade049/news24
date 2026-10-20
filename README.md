# ⚡ NewsPulse — Project Reference & Architecture

> **Shortcut Context File**: You can reference this anytime by typing `@newspulse` or `@newspulse.md`.

---

## 📌 Project Overview
- **Name**: **NewsPulse** (formerly News24)
- **Live URL**: [https://Banjade049.github.io/news24/](https://Banjade049.github.io/news24/)
- **Local Workspace**: [`/home/samrat/news24/`](file:///home/samrat/news24/)
- **GitHub Repository**: `git@github.com:Banjade049/news24.git` (Branch: `main`)
- **Host**: GitHub Pages (Free 24/7, works when laptop is turned OFF)
- **Local Preview**: `http://localhost:5050/`

---

## 🌟 Key Features
1. **🇳🇵 17 Top Nepal Portals**: OnlineKhabar, BBC Nepali, Ratopati, Setopati, Nagarik News, Baahrakhari, Nepal Live, Himal Khabar, Khabarhub, Bizmandu, Clickmandu, Deshsanchar, Ujyaalo, Lokaantar, Reporters Nepal, Swasthya Khabar, OnlineKhabar English.
2. **⚽ Man City & Football Tracker**: BBC Sport, Sky Sports, City Xtra + match score parser.
3. **🌍 World News**: BBC World, CNN, Al Jazeera, The Guardian.
4. **💻 Tech & IT**: TechCrunch, The Verge, Wired, Ars Technica, Engadget, GSMArena.
5. **🌦️ Kathmandu Weather Widget**: Live weather from Open-Meteo API (zero keys, CORS-enabled).
6. **🔊 Text-to-Speech Read Aloud**: Reads headlines & summaries with native browser speech synthesis (`hi-IN` / `en-US`).
7. **🎮 Daily News Quiz**: Auto-generates 5-question multiple choice quizzes directly from today's real headlines.
8. **📓 NotebookLM Integration**: Client-side localStorage save + auto-clipboard copy of URLs for NotebookLM source ingestion.
9. **📱 PWA & Offline Support**: Service Worker (`v4`) caching for offline reading and Home Screen install on iOS & Android.

---

## ⚡ Technical Stack
- **Architecture**: 100% Client-Side Pure HTML5, CSS3, Vanilla JavaScript (No Node/React server required).
- **Dual Conversion Engine**: Primary `api.rss2json.com` with instant failover to `feed2json.org` (eliminates rate limits/HTTP 429).
- **Timezone Precision**: Accurate UTC date parsing to prevent "5 ghanta agadi" timestamp drift.
- **Micro-Batching**: Fetches feeds in concurrent batches of 6 for speed and mobile browser stability.

---

## 📁 Key Files
- [`index.html`](file:///home/samrat/news24/index.html) — Core single-page application & UI
- [`sw.js`](file:///home/samrat/news24/sw.js) — Service worker (Cache version: `news24-v4`)
- [`manifest.json`](file:///home/samrat/news24/manifest.json) — PWA manifest configuration
- [`apple-touch-icon.png`](file:///home/samrat/news24/apple-touch-icon.png) — iOS Home Screen icon
