"""
Enhanced Study Sonship AI - Full-Featured Bible Study Platform
Connected to live PostgreSQL database with AI-generated translations
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5433')),
    'database': os.getenv('DB_NAME', 'sonship_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'supersecretpassword')
}

def get_db():
    """Get database connection"""
    return psycopg2.connect(**DB_CONFIG)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/books')
def get_books():
    """Get list of all books with translation progress"""
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    book,
                    COUNT(*) as verse_count,
                    COUNT(CASE WHEN insight IS NOT NULL THEN 1 END) as commentary_count
                FROM verses
                GROUP BY book
                ORDER BY MIN(id)
            """)
            books = cur.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'books': [dict(row) for row in books]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chapter/<book>/<int:chapter>')
def get_chapter(book, chapter):
    """Get chapter with verses and commentary"""
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    verse_number,
                    verse_text,
                    insight,
                    updated_at
                FROM verses
                WHERE book = %s AND chapter = %s
                ORDER BY verse_number
            """, (book, chapter))
            verses = cur.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'book': book,
            'chapter': chapter,
            'verses': [dict(row) for row in verses]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search')
def search():
    """Search verses and commentary"""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 50, type=int)
    
    if not query:
        return jsonify({'success': False, 'error': 'Query required'}), 400
    
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    book,
                    chapter,
                    verse_number,
                    verse_text,
                    insight,
                    updated_at
                FROM verses
                WHERE verse_text ILIKE %s OR insight ILIKE %s
                ORDER BY id
                LIMIT %s
            """, (f'%{query}%', f'%{query}%', limit))
            results = cur.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'query': query,
            'results': [dict(row) for row in results],
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get translation statistics"""
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Overall stats
            cur.execute("""
                SELECT 
                    COUNT(*) as total_verses,
                    COUNT(CASE WHEN insight IS NOT NULL THEN 1 END) as verses_with_commentary,
                    COUNT(DISTINCT book) as books_count,
                    MAX(updated_at) as last_update
                FROM verses
            """)
            stats = cur.fetchone()
            
            # Recent translations
            cur.execute("""
                SELECT book, chapter, verse_number, updated_at
                FROM verses
                ORDER BY updated_at DESC
                LIMIT 10
            """)
            recent = cur.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': dict(stats),
            'recent_translations': [dict(row) for row in recent]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/progress')
def get_progress():
    """Get translation progress by book"""
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    book,
                    COUNT(*) as total_verses,
                    COUNT(CASE WHEN insight IS NOT NULL THEN 1 END) as completed_verses,
                    ROUND(COUNT(CASE WHEN insight IS NOT NULL THEN 1 END) * 100.0 / COUNT(*), 2) as percentage
                FROM verses
                GROUP BY book
                ORDER BY MIN(id)
            """)
            progress = cur.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'progress': [dict(row) for row in progress]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/verse/<book>/<int:chapter>/<int:verse>')
def get_verse(book, chapter, verse):
    """Get a single verse"""
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    book,
                    chapter,
                    verse_number,
                    verse_text,
                    insight,
                    updated_at
                FROM verses
                WHERE book = %s AND chapter = %s AND verse_number = %s
            """, (book, chapter, verse))
            result = cur.fetchone()
        conn.close()
        
        if result:
            return jsonify({
                'success': True,
                'verse': dict(result)
            })
        else:
            return jsonify({'success': False, 'error': 'Verse not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

