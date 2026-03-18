import json, os
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "history.json")

class HistoryManager:
    def _load(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def _write(self, data):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save(self, title, author, style, result):
        h = self._load()
        h.insert(0, {
            "title": title,
            "author": author,
            "style": style,
            "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
            "pitch": result.get("one_line_pitch", ""),
            "full_result": result
        })
        self._write(h[:50])

    def get_all(self):
        return self._load()

    def delete(self, idx):
        h = self._load()
        if 0 <= idx < len(h):
            h.pop(idx)
            self._write(h)

    def clear(self):
        self._write([])
