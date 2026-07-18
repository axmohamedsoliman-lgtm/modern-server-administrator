# Modern Server Administrator

> A desktop-class server management tool — multi-process orchestration, real-time dashboard, encrypted updates.

[![Stack](https://img.shields.io/badge/stack-Python_%7C_Flask-3776AB?style=flat-square&logo=python)](.)
[![Platform](https://img.shields.io/badge/platform-Windows_%7C_Linux-lightgrey?style=flat-square)](.)
[![Lines](https://img.shields.io/badge/core_engine-2%2C300%2B_lines-orange?style=flat-square)](.)
[![Status](https://img.shields.io/badge/status-Active-success?style=flat-square)](.)

---

## What It Is

Modern Server Administrator (MSA) is a production tool for managing multiple local web servers simultaneously — Nginx, PHP, Node, custom processes — from a single interface. It has a real-time web dashboard, an encrypted update delivery system, and remote analytics.

---

## What It Solves

Running multiple local dev servers typically means juggling multiple terminal windows, not knowing which crashed, and manually restarting processes. MSA turns that into a single dashboard with live status, process control, real-time logs streamed via SSE, and instant filesystem-based change detection.

---

## Technical Highlights

- **Multi-threaded Flask backend** (2,300+ lines) — orchestrates multiple server processes simultaneously from a single Python process; serves the management UI and the SSE event stream from the same app
- **Real-time SSE dashboard** — process events (started, crashed, stdout, stderr) streamed to the browser with zero polling
- **Hash-based save state cache** — `save_state_manager.py` computes a SHA-256 directory hash (paths + sizes + mtimes) and skips full re-scans if nothing changed since last launch; persisted via `pickle` for fast startup
- **Filesystem observer** — Watchdog threads detect project file changes instantly and trigger hot-reload without manual restart
- **Encrypted update delivery** — updates are signed and delivered as Fernet-encrypted (AES-128-CBC) payloads; verified via PBKDF2HMAC SHA-256 (100,000 iterations) before being applied
- **Remote analytics** — Supabase-backed usage monitoring, with local data protected by Fernet encryption before transmission

---

## Stack

`Python` · `Flask` · `Watchdog` · `Supabase` · `cryptography (Fernet)` · `PyInstaller`

---

## Files In This Repo

- `save_state_manager.excerpt.py` — Hash-based cache & change detection logic (curated snippet)
- `requirements.txt` — Full dependency list

---

## Screenshots

→ [View full app showcase on the portfolio landing page](https://axmohamedsoliman-lgtm.github.io/Genom-framework-profile-landing-page/)

---

*Full source is private. This repo contains architecture overview and curated implementation snippets.*
