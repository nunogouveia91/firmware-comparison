from flask import Flask, redirect, send_from_directory, request, jsonify, make_response
import sqlite3
import os
import csv
import io
import json

try:
    import requests as _http
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    _http = None

app = Flask(__name__, static_folder='src')

DB_PATH = os.path.join(os.path.dirname(__file__), 'budget.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            device_id TEXT UNIQUE NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            color TEXT DEFAULT '#4f8ef7',
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            icon TEXT DEFAULT '📦',
            group_type TEXT DEFAULT 'basic',
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            wallet_id INTEGER NOT NULL,
            category_id INTEGER,
            amount REAL NOT NULL,
            description TEXT DEFAULT '',
            date TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (wallet_id) REFERENCES wallets(id),
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
        );
    ''')
    conn.commit()
    conn.close()


init_db()


# ── Static pages ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect('/budget')


@app.route('/budget')
def budget():
    return send_from_directory('src', 'budget.html')


@app.route('/comparador')
def comparador():
    return send_from_directory('src', 'comparador.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('src', filename)


# ── Users ─────────────────────────────────────────────────────────────────────

@app.route('/api/users/<device_id>', methods=['GET'])
def get_user(device_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, name, device_id, created_at FROM users WHERE device_id = ?', (device_id,))
    user = c.fetchone()
    conn.close()
    if not user:
        return jsonify({'error': 'not found'}), 404
    return jsonify(dict(user))


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json(silent=True) or {}
    device_id = data.get('device_id', '').strip()
    name = data.get('name', 'Utilizador').strip()
    if not device_id:
        return jsonify({'error': 'device_id required'}), 400

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, name, device_id, created_at FROM users WHERE device_id = ?', (device_id,))
    existing = c.fetchone()
    if existing:
        conn.close()
        return jsonify(dict(existing))

    c.execute('INSERT INTO users (name, device_id) VALUES (?, ?)', (name, device_id))
    user_id = c.lastrowid

    # Default wallet
    c.execute('INSERT INTO wallets (user_id, name, color) VALUES (?, ?, ?)',
              (user_id, 'Pessoal', '#4f8ef7'))

    # Default categories
    defaults = [
        ('Alimentação', '🛒', 'basic'),
        ('Transportes', '🚗', 'basic'),
        ('Saúde', '💊', 'basic'),
        ('Casa', '🏠', 'basic'),
        ('Serviços', '📱', 'basic'),
        ('Desporto', '⚽', 'basic'),
        ('Lazer', '🎮', 'free'),
        ('Roupa', '👕', 'free'),
        ('Restaurantes', '🍽️', 'free'),
        ('Poupança', '💰', 'saving'),
        ('Outros', '📦', 'basic'),
    ]
    c.executemany(
        'INSERT INTO categories (user_id, name, icon, group_type) VALUES (?, ?, ?, ?)',
        [(user_id, n, i, g) for n, i, g in defaults]
    )

    conn.commit()
    c.execute('SELECT id, name, device_id, created_at FROM users WHERE id = ?', (user_id,))
    user = dict(c.fetchone())
    conn.close()
    return jsonify(user), 201


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json(silent=True) or {}
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'name required'}), 400
    conn = get_db()
    conn.execute('UPDATE users SET name = ? WHERE id = ?', (name, user_id))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})


# ── Wallets ───────────────────────────────────────────────────────────────────

@app.route('/api/wallets', methods=['GET'])
def get_wallets():
    user_id = request.args.get('user_id', type=int)
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM wallets WHERE user_id = ? ORDER BY id', (user_id,)
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/wallets', methods=['POST'])
def create_wallet():
    data = request.get_json(silent=True) or {}
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO wallets (user_id, name, color) VALUES (?, ?, ?)',
              (data['user_id'], data['name'].strip(), data.get('color', '#4f8ef7')))
    wid = c.lastrowid
    conn.commit()
    row = conn.execute('SELECT * FROM wallets WHERE id = ?', (wid,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201


@app.route('/api/wallets/<int:wallet_id>', methods=['DELETE'])
def delete_wallet(wallet_id):
    conn = get_db()
    conn.execute('DELETE FROM wallets WHERE id = ?', (wallet_id,))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})


# ── Categories ────────────────────────────────────────────────────────────────

@app.route('/api/categories', methods=['GET'])
def get_categories():
    user_id = request.args.get('user_id', type=int)
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM categories WHERE user_id = ? ORDER BY name', (user_id,)
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json(silent=True) or {}
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO categories (user_id, name, icon, group_type) VALUES (?, ?, ?, ?)',
              (data['user_id'], data['name'].strip(), data.get('icon', '📦'), data.get('group_type', 'basic')))
    cid = c.lastrowid
    conn.commit()
    row = conn.execute('SELECT * FROM categories WHERE id = ?', (cid,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201


@app.route('/api/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    conn = get_db()
    conn.execute('DELETE FROM categories WHERE id = ?', (cat_id,))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})


# ── Expenses ──────────────────────────────────────────────────────────────────

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    user_id = request.args.get('user_id', type=int)
    wallet_id = request.args.get('wallet_id', type=int)
    months = request.args.getlist('month')  # ['2026-03', ...]

    query = '''
        SELECT e.id, e.amount, e.description, e.date, e.created_at,
               c.name AS category_name, c.icon AS category_icon, c.group_type,
               w.id AS wallet_id, w.name AS wallet_name, w.color AS wallet_color
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.id
        LEFT JOIN wallets w ON e.wallet_id = w.id
        WHERE e.user_id = ?
    '''
    params = [user_id]

    if wallet_id:
        query += ' AND e.wallet_id = ?'
        params.append(wallet_id)

    if months:
        placeholders = ','.join('?' for _ in months)
        query += f" AND strftime('%Y-%m', e.date) IN ({placeholders})"
        params.extend(months)

    query += ' ORDER BY e.date DESC, e.created_at DESC'

    conn = get_db()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/expenses', methods=['POST'])
def create_expense():
    data = request.get_json(silent=True) or {}
    amount = data.get('amount')
    if not amount or float(amount) <= 0:
        return jsonify({'error': 'invalid amount'}), 400

    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO expenses (user_id, wallet_id, category_id, amount, description, date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['user_id'], data['wallet_id'], data.get('category_id'),
          float(amount), data.get('description', ''), data['date']))
    eid = c.lastrowid
    conn.commit()

    row = conn.execute('''
        SELECT e.id, e.amount, e.description, e.date, e.created_at,
               c.name AS category_name, c.icon AS category_icon, c.group_type,
               w.id AS wallet_id, w.name AS wallet_name, w.color AS wallet_color
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.id
        LEFT JOIN wallets w ON e.wallet_id = w.id
        WHERE e.id = ?
    ''', (eid,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201


@app.route('/api/expenses/<int:exp_id>', methods=['DELETE'])
def delete_expense(exp_id):
    conn = get_db()
    conn.execute('DELETE FROM expenses WHERE id = ?', (exp_id,))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})


# ── Elasticsearch / Kibana Export ─────────────────────────────────────────────

@app.route('/elastic')
def elastic_page():
    return send_from_directory('src', 'elastic.html')


def _es_auth(payload):
    """Return auth kwargs for the requests library based on auth_mode."""
    mode = payload.get('auth_mode', 'basic')
    if mode == 'apikey':
        key = payload.get('api_key', '').strip()
        return {'headers': {'Authorization': f'ApiKey {key}'}} if key else {}
    else:
        user = payload.get('username', '').strip()
        pwd = payload.get('password', '')
        return {'auth': (user, pwd)} if user else {}


def _es_request(method, url, payload, **kwargs):
    """Execute an HTTP request to Elasticsearch with auth and SSL settings."""
    if _http is None:
        raise RuntimeError('A biblioteca "requests" não está instalada.')
    auth_kwargs = _es_auth(payload)
    ssl_verify = payload.get('ssl_verify', True)
    return getattr(_http, method)(
        url,
        verify=ssl_verify,
        timeout=kwargs.pop('timeout', 30),
        **auth_kwargs,
        **kwargs,
    )


def _flatten(obj, parent='', sep='.'):
    """Recursively flatten nested dicts; serialize arrays as JSON strings."""
    items = {}
    for k, v in obj.items():
        key = f'{parent}{sep}{k}' if parent else k
        if isinstance(v, dict):
            items.update(_flatten(v, key, sep))
        elif isinstance(v, list):
            items[key] = json.dumps(v, ensure_ascii=False)
        else:
            items[key] = v
    return items


def _build_es_body(payload, size):
    """Build an Elasticsearch query body from the UI payload."""
    date_field = payload.get('date_field', '@timestamp').strip() or '@timestamp'
    date_from = payload.get('date_from', '').strip()
    date_to = payload.get('date_to', '').strip()
    query_str = payload.get('query_string', '').strip()

    must_clauses = []

    if date_from or date_to:
        rng = {}
        if date_from:
            rng['gte'] = date_from
        if date_to:
            rng['lte'] = date_to
        must_clauses.append({'range': {date_field: rng}})

    if query_str:
        must_clauses.append({'query_string': {'query': query_str, 'analyze_wildcard': True}})

    query = {'bool': {'must': must_clauses}} if must_clauses else {'match_all': {}}

    return {
        'query': query,
        'size': size,
        'sort': [{date_field: {'order': 'desc', 'unmapped_type': 'date'}}],
    }


@app.route('/api/elastic/test', methods=['POST'])
def elastic_test():
    data = request.get_json(silent=True) or {}
    host = data.get('host', '').rstrip('/')
    if not host:
        return jsonify({'error': 'URL obrigatório'}), 400
    if _http is None:
        return jsonify({'error': 'Instala a biblioteca "requests": pip install requests'}), 500
    try:
        r = _es_request('get', f'{host}/', data, timeout=10)
        if r.status_code == 401:
            return jsonify({'error': 'Autenticação falhou (401 Unauthorized)'}), 401
        r.raise_for_status()
        info = r.json()
        return jsonify({
            'ok': True,
            'cluster_name': info.get('cluster_name', ''),
            'version': info.get('version', {}).get('number', ''),
        })
    except _http.exceptions.SSLError:
        return jsonify({'error': 'Erro SSL — desativa a verificação do certificado e tenta novamente.'}), 502
    except _http.exceptions.ConnectionError:
        return jsonify({'error': 'Não foi possível ligar ao host. Verifica o URL e a rede.'}), 502
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/elastic/indices', methods=['POST'])
def elastic_indices():
    data = request.get_json(silent=True) or {}
    host = data.get('host', '').rstrip('/')
    if not host or _http is None:
        return jsonify({'indices': []})
    try:
        r = _es_request('get', f'{host}/_cat/indices?h=index&s=index&format=json', data, timeout=10)
        if not r.ok:
            return jsonify({'indices': []})
        indices = sorted(
            [i['index'] for i in r.json() if not i['index'].startswith('.')],
            key=str.lower,
        )
        return jsonify({'indices': indices})
    except Exception:
        return jsonify({'indices': []})


@app.route('/api/elastic/query', methods=['POST'])
def elastic_query():
    """Preview endpoint — returns up to 5 hits and the total count."""
    data = request.get_json(silent=True) or {}
    host = data.get('host', '').rstrip('/')
    index = data.get('index', '*').strip() or '*'
    if not host:
        return jsonify({'error': 'URL obrigatório'}), 400
    if _http is None:
        return jsonify({'error': 'Instala a biblioteca "requests": pip install requests'}), 500
    try:
        body = _build_es_body(data, size=5)
        r = _es_request('post', f'{host}/{index}/_search', data, json=body, timeout=20)
        if r.status_code == 401:
            return jsonify({'error': 'Autenticação falhou (401)'}), 401
        r.raise_for_status()
        result = r.json()
        total_val = result.get('hits', {}).get('total', {})
        total = total_val.get('value', total_val) if isinstance(total_val, dict) else total_val
        hits = result.get('hits', {}).get('hits', [])
        return jsonify({'total': total, 'hits': hits})
    except _http.exceptions.ConnectionError:
        return jsonify({'error': 'Não foi possível ligar ao host.'}), 502
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/elastic/download', methods=['POST'])
def elastic_download():
    """Full export endpoint using the scroll API for large datasets."""
    data = request.get_json(silent=True) or {}
    host = data.get('host', '').rstrip('/')
    index = data.get('index', '*').strip() or '*'
    fmt = data.get('format', 'csv')
    flatten = data.get('flatten', True)
    max_records = min(int(data.get('max_records', 10000)), 500000)
    batch_size = min(1000, max_records)

    if not host:
        return jsonify({'error': 'URL obrigatório'}), 400
    if _http is None:
        return jsonify({'error': 'Instala a biblioteca "requests": pip install requests'}), 500

    try:
        # ── Initial scroll request ──
        body = _build_es_body(data, size=batch_size)
        r = _es_request('post', f'{host}/{index}/_search?scroll=2m', data, json=body, timeout=30)
        if r.status_code == 401:
            return jsonify({'error': 'Autenticação falhou (401)'}), 401
        r.raise_for_status()
        result = r.json()

        scroll_id = result.get('_scroll_id')
        all_hits = list(result.get('hits', {}).get('hits', []))

        # ── Continue scrolling ──
        while scroll_id and len(all_hits) < max_records:
            r = _es_request(
                'post', f'{host}/_search/scroll', data,
                json={'scroll': '2m', 'scroll_id': scroll_id},
                timeout=30,
            )
            r.raise_for_status()
            result = r.json()
            scroll_id = result.get('_scroll_id', scroll_id)
            batch = result.get('hits', {}).get('hits', [])
            if not batch:
                break
            all_hits.extend(batch)

        # ── Clean up scroll context ──
        if scroll_id:
            try:
                _es_request('delete', f'{host}/_search/scroll', data,
                            json={'scroll_id': scroll_id}, timeout=5)
            except Exception:
                pass

        all_hits = all_hits[:max_records]
        if not all_hits:
            return jsonify({'error': 'Nenhum documento encontrado para os filtros selecionados.'}), 404

        # ── Build records ──
        records = []
        for h in all_hits:
            src = h.get('_source', {})
            rec = {'_id': h.get('_id', ''), '_index': h.get('_index', '')}
            if flatten:
                rec.update(_flatten(src))
            else:
                rec.update(src)
            records.append(rec)

        # ── Serialize ──
        if fmt == 'json':
            output = json.dumps(records, ensure_ascii=False, indent=2, default=str)
            resp = make_response(output)
            resp.headers['Content-Type'] = 'application/json; charset=utf-8'
            resp.headers['Content-Disposition'] = 'attachment; filename=elastic_export.json'
            return resp

        if fmt == 'ndjson':
            output = '\n'.join(json.dumps(r, ensure_ascii=False, default=str) for r in records)
            resp = make_response(output)
            resp.headers['Content-Type'] = 'application/x-ndjson; charset=utf-8'
            resp.headers['Content-Disposition'] = 'attachment; filename=elastic_export.ndjson'
            return resp

        # CSV (default)
        all_keys: list = ['_id', '_index']
        seen_keys: set = {'_id', '_index'}
        for rec in records:
            for k in rec:
                if k not in seen_keys:
                    all_keys.append(k)
                    seen_keys.add(k)

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=all_keys, extrasaction='ignore',
                                lineterminator='\n')
        writer.writeheader()
        for rec in records:
            writer.writerow({k: rec.get(k, '') for k in all_keys})

        resp = make_response('\ufeff' + buf.getvalue())  # BOM for Excel UTF-8
        resp.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
        resp.headers['Content-Disposition'] = 'attachment; filename=elastic_export.csv'
        return resp

    except _http.exceptions.SSLError:
        return jsonify({'error': 'Erro SSL — desativa a verificação do certificado.'}), 502
    except _http.exceptions.ConnectionError:
        return jsonify({'error': 'Não foi possível ligar ao host.'}), 502
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
