"""
save_state_manager.excerpt.py — Hash-Based Cache & Change Detection (curated snippet)

This is a representative excerpt showing the core caching strategy used by
Modern Server Administrator's save state system.

Full source is private.
"""

import os
import pickle
import hashlib
import threading
from pathlib import Path
from typing import Optional


class SaveStateManager:
    """
    Hash-based cache manager for fast startup without re-scanning the filesystem.

    On first launch: scans all project directories, builds a state snapshot, persists to .pkl
    On subsequent launches: computes a lightweight directory hash; if unchanged, loads from cache.
    Change detection uses file paths + sizes + modification times — not file content.
    """

    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, '.data')
        self.save_state_path = os.path.join(self.data_dir, 'save_state.pkl')
        self.cache_lock = threading.RLock()

    def _calculate_directory_hash(self, directory: str) -> str:
        """
        SHA-256 hash of directory structure (paths + sizes + mtimes).
        Excludes build artifacts and dependency folders to prevent false invalidations.
        """
        try:
            hasher = hashlib.sha256()
            EXCLUDE = {'.git', 'node_modules', '__pycache__', '.data', 'logs', 'dist', 'build'}

            for root, dirs, files in os.walk(directory):
                dirs[:] = sorted(d for d in dirs if d not in EXCLUDE)
                rel_root = os.path.relpath(root, directory)

                for fname in sorted(files):
                    fpath = os.path.join(root, fname)
                    try:
                        stat = os.stat(fpath)
                        entry = f"{rel_root}/{fname}:{stat.st_size}:{stat.st_mtime:.0f}"
                        hasher.update(entry.encode('utf-8', errors='replace'))
                    except OSError:
                        pass

            return hasher.hexdigest()
        except Exception:
            return ''

    def load_or_rebuild(self, scanner_fn) -> dict:
        """
        Core cache logic:
        1. Load persisted state (if exists)
        2. Compute current directory hash
        3. If hash matches → return cache (skip full scan)
        4. If hash differs → run scanner_fn, persist new state
        """
        with self.cache_lock:
            cached = self._load_pickle()
            current_hash = self._calculate_directory_hash(self.base_dir)

            if cached and cached.get('directory_hash') == current_hash:
                return cached['state']

            # Hash mismatch or no cache — run the full scan
            new_state = scanner_fn()
            self._save_pickle({'directory_hash': current_hash, 'state': new_state})
            return new_state

    def _load_pickle(self) -> Optional[dict]:
        try:
            with open(self.save_state_path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return None

    def _save_pickle(self, data: dict):
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.save_state_path, 'wb') as f:
            pickle.dump(data, f)
