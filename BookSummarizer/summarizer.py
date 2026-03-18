import json
import re
import os
import time
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use stable free model
client = genai.GenerativeModel("gemini-2.0-flash-lite")


STYLES = {
    "short": "Write ONE powerful paragraph (130-160 words) capturing the soul and essence of this book.",
    "detailed": "Write a rich comprehensive summary (400-500 words) covering central themes, narrative arc, key arguments, and conclusions.",
    "keypoints": "Extract exactly 12 most important key points as a clean numbered list. Each must be a complete, insightful sentence.",
    "chapter": "Identify and summarize each chapter or major section with clear headings.",
    "lessons": "Extract 10 profound life lessons or practical wisdom readers can apply immediately. Number each one.",
    "study": "Create a complete study guide: main themes, key concepts, important ideas, critical analysis, and exam-ready notes."
}

LANGUAGES = {
    "english": "Respond in polished, elegant English.",
    "hindi": "Poora jawab sirf Hindi mein likho (Devanagari script).",
    "hinglish": "Write in natural Hinglish — the way educated urban Indians speak.",
    "punjabi": "Respond entirely in Punjabi using Gurmukhi script.",
    "urdu": "Poora jawab khoobsurat Urdu mein likho."
}

TONES = {
    "story": "Write in an engaging story-telling style — narrative, vivid, compelling.",
    "simple": "Use very simple, clear, easy-to-understand language. Short sentences.",
    "professional": "Crisp, authoritative, objective — formal and precise.",
    "student": "Clear, accessible, memorable — perfect for study and exam prep."
}


class Summarizer:

    def generate_with_retry(self, prompt):
        """Retry Gemini request if rate limit happens"""
        for _ in range(3):
            try:
                return client.generate_content(prompt)
            except Exception:
                time.sleep(40)
        raise Exception("Gemini API quota exceeded")

    def analyze(self, title, author, content, style, language, tone):

        wc = len(content.split())

        prompt = f"""
You are a world-class AI literary analyst.

Book: "{title or 'Unknown Title'}" by {author or 'Unknown Author'}
Word count: ~{wc} words (~{round(wc/238)} min read)

LANGUAGE: {LANGUAGES.get(language, LANGUAGES['english'])}
TONE: {TONES.get(tone, TONES['story'])}
TASK: {STYLES.get(style, STYLES['short'])}

Return ONLY a valid JSON object with exactly these keys:

{{
"summary": "",
"key_insights": "",
"important_quotes": "",
"chapter_breakdown": "",
"life_lessons": "",
"reading_time_original": {round(wc/238)},
"time_saved": {max(1, round(wc/238) - 3)},
"difficulty_level": "",
"genre_tags": [],
"one_line_pitch": ""
}}

BOOK CONTENT:
------
{content[:8000]}
------

Return ONLY JSON. No markdown.
"""

        response = self.generate_with_retry(prompt)

        raw = response.text.strip()

        # remove markdown
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"^```\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw).strip()

        try:
            return json.loads(raw)

        except json.JSONDecodeError:

            m = re.search(r"\{[\s\S]*\}", raw)

            try:
                return json.loads(m.group(0)) if m else self._fallback(raw, wc)
            except Exception:
                return self._fallback(raw, wc)

    def _fallback(self, raw, wc):
        return {
            "summary": raw,
            "key_insights": "",
            "important_quotes": "",
            "chapter_breakdown": "",
            "life_lessons": "",
            "reading_time_original": round(wc / 238),
            "time_saved": max(1, round(wc / 238) - 3),
            "difficulty_level": "",
            "genre_tags": [],
            "one_line_pitch": ""
        }
