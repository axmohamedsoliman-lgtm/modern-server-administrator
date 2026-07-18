# Modern Server Administrator

> A multi-server orchestration platform. Real-time monitoring, encrypted updates, instant startup — packaged as a standalone executable.

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](.)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](.)
[![PowerShell](https://img.shields.io/badge/PowerShell-5391FE?style=flat-square&logo=powershell&logoColor=white)](.)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white)](.)
[![Status](https://img.shields.io/badge/status-Active-success?style=flat-square)](.)

**[→ Live Demo](https://genom-showcase.pages.dev/applications/modern-server/)** · [Portfolio](https://genom-showcase.pages.dev/)

---

## What It Is

MSA is a desktop application that manages multiple local web servers from a single Python process. It provides a real-time SSE dashboard, hash-based state caching for instant startup, and encrypted OTA update delivery. Ships as a standalone `.exe` via PyInstaller — no Python install required on the end user's machine.

---

## Core Architecture

**Flask backend (2,300+ lines)** — single-process multi-server orchestration:
- Spawns and monitors server processes as subprocesses
- Streams live stdout/stderr to the web UI via Server-Sent Events
- Serves the management dashboard as a static SPA

**State cache** — directory hash comparison for instant restarts:

```python
# save_state_manager.excerpt.py — Hash-Based Cache & Change Detection
def _calculate_directory_hash(self, directory: str) -> str:
    hasher = hashlib.sha256()
    EXCLUDE = {'.git', 'node_modules', '__pycache__', '.data'}
    for root, dirs, files in os.walk(directory):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDE)
        for fname in sorted(files):
            fpath = os.path.join(root, fname)
            stat = os.stat(fpath)
            entry = f"{os.path.relpath(root, directory)}/{fname}:{stat.st_size}:{stat.st_mtime:.0f}"
            hasher.update(entry.encode('utf-8', errors='replace'))
    return hasher.hexdigest()
```

**Encrypted update delivery** — Fernet symmetric encryption with PBKDF2HMAC SHA-256 key derivation.

---

## Engineering Highlights

- **Real-time Watchdog** — filesystem observer threads detect project changes the instant they happen
- **SHA-256 directory hash cache** — paths + sizes + mtimes hashed; cache hit = zero re-scan on launch
- **Supabase analytics** — remote usage monitoring with local encryption protecting credentials
- **PowerShell orchestration** — automated build and deployment scripts manage the full release pipeline

---

## Skills Demonstrated

`Python` `Flask` `JavaScript` `PowerShell` `Supabase` `AES Encryption` `Filesystem Automation` `Real-Time SSE` `Multi-Process Management` `PyInstaller`
