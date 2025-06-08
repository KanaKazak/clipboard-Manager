from flask import jsonify
from flask import request, render_template
import flask
import sqlite3
import os

app = flask.Flask(__name__)

# Define the path to the SQLite database
# Assuming the database is located in the parent directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, '..', 'clipboard.db')

@app.route('/')
def index():
    # Render index.html template
    return flask.render_template('index.html')

@app.route('/history')
def history():
    # Get page number from query parameter, default 1
    page = request.args.get('page', default=1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get total number of entries for page count
    cursor.execute("SELECT COUNT(*) FROM clipboard_history")
    total_entries = cursor.fetchone()[0]

    # Fetch entries for this page
    cursor.execute(
        "SELECT * FROM clipboard_history ORDER BY timestamp DESC LIMIT ? OFFSET ?",
        (per_page, offset)
    )
    history = cursor.fetchall()
    conn.close()

    total_pages = (total_entries + per_page - 1) // per_page  # ceiling division

    return render_template(
        'history.html',
        history=history,
        page=page,
        total_pages=total_pages
    )

@app.route('/api/history')
def api_history():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clipboard_history ORDER BY timestamp DESC LIMIT 20")
    history = cursor.fetchall()
    conn.close()

    # Convert data to list of dicts for JSON serialization
    history_list = [
        {"id": row[0], "content": row[1], "timestamp": row[2]}
        for row in history
    ]
    return jsonify(history_list)

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '', type=str)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM clipboard_history WHERE content LIKE ? ORDER BY timestamp DESC LIMIT 50",
        ('%' + query + '%',)
    )
    results = cursor.fetchall()
    conn.close()
    return jsonify([
        {"id": r[0], "content": r[1], "timestamp": r[2]} for r in results
    ])

@app.route('/export/json')
def export_json():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clipboard_history")
    data = cursor.fetchall()
    conn.close()
    return jsonify([
        {"id": r[0], "content": r[1], "timestamp": r[2]} for r in data
    ])

@app.route('/export/csv')
def export_csv():
    import csv
    from io import StringIO
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clipboard_history")
    data = cursor.fetchall()
    conn.close()

    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['id', 'content', 'timestamp'])
    cw.writerows(data)
    return flask.Response(
        si.getvalue(),
        mimetype='text/csv',
        headers={"Content-disposition": "attachment; filename=clipboard_history.csv"}
    )


if __name__ == '__main__':
    app.run(debug=True)
