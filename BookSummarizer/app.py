from flask import Flask, render_template, request, jsonify
from summarizer import Summarizer
from utils.pdf_extractor import extract_pdf_text
from utils.history_manager import HistoryManager
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

summarizer = Summarizer()
history = HistoryManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        title    = data.get('title', '').strip()
        author   = data.get('author', '').strip()
        content  = data.get('content', '').strip()
        style    = data.get('style', 'short')
        language = data.get('language', 'english')
        tone     = data.get('tone', 'story')
        if not content:
            return jsonify({'error': 'No content provided'}), 400
        result = summarizer.analyze(title, author, content, style, language, tone)
        history.save(title, author, style, result)
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/extract-pdf', methods=['POST'])
def extract_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files allowed'}), 400
        text = extract_pdf_text(file)
        return jsonify({'success': True, 'text': text, 'word_count': len(text.split())})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify({'history': history.get_all()})

@app.route('/api/history/clear', methods=['DELETE'])
def clear_history():
    history.clear()
    return jsonify({'success': True})

@app.route('/api/history/<int:idx>', methods=['DELETE'])
def delete_history(idx):
    history.delete(idx)
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
