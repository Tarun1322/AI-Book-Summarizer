from groq import Groq
import json, re, os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

STYLES = {
    'short': 'Write ONE powerful paragraph (130-160 words) capturing the soul and essence of this book.',
    'detailed': 'Write a rich comprehensive summary (400-500 words) covering central themes, narrative arc, key arguments, and conclusions.',
    'keypoints': 'Extract exactly 12 most important key points as a clean numbered list.',
    'chapter': 'Identify and summarize each chapter or major section with clear headings.',
    'lessons': 'Extract 10 profound life lessons readers can apply immediately.',
    'study': 'Create a complete study guide with themes, concepts and exam notes.'
}

LANGUAGES = {
    'english': 'Respond in polished, elegant English.',
    'hindi': 'Poora jawab sirf Hindi mein likho.',
    'hinglish': 'Write in natural Hinglish.',
    'punjabi': 'Respond entirely in Punjabi.',
    'urdu': 'Poora jawab Urdu mein likho.'
}

TONES = {
    'story': 'Write in engaging storytelling style.',
    'simple': 'Use simple easy language.',
    'professional': 'Formal and precise.',
    'student': 'Clear and easy for students.'
}


class Summarizer:

    def analyze(self, title, author, content, style, language, tone):

        wc = len(content.split())

        prompt = f"""
You are a world-class AI literary analyst.

Book: "{title or 'Unknown Title'}"
Author: "{author or 'Unknown Author'}"

LANGUAGE: {LANGUAGES.get(language)}
TONE: {TONES.get(tone)}
TASK: {STYLES.get(style)}

Return ONLY JSON:

{{
"summary":"",
"key_insights":"",
"important_quotes":"",
"chapter_breakdown":"",
"life_lessons":"",
"reading_time_original":{round(wc/238)},
"time_saved":{max(1, round(wc/238)-3)},
"difficulty_level":"",
"genre_tags":["tag1","tag2","tag3"],
"one_line_pitch":""
}}

CONTENT:
{content[:8000]}
"""

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.choices[0].message.content.strip()

        raw = re.sub(r'^```json\s*', '', raw)
        raw = re.sub(r'^```\s*', '', raw)
        raw = re.sub(r'\s*```$', '', raw).strip()

        try:
            return json.loads(raw)

        except json.JSONDecodeError:

            m = re.search(r'\{[\s\S]*\}', raw)

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
