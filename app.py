# loja-de-roupaimport sqlite3
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# 1. CRIAÇÃO DO BANCO DE DADOS SQLITE
def init_db():
    conn = sqlite3.connect('loja_roupas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            tamanho TEXT NOT NULL,
            estoque INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('loja_roupas.db')
    conn.row_factory = sqlite3.Row
    return conn

# 2. DESIGN DA INTERFACE (Tema Azul Bebê / Pastel)
HTML_LAYOUT = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Moda & Estilo - Dashboard</title>
    <style>
        :root {
            --azul-bebe: #E0F2FE;
            --azul-claro-hover: #BAE6FD;
            --azul-destaque: #38BDF8;
            --azul-escuro: #0369A1;
            --fundo: #F8FAFC;
            --texto: #334155;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--fundo);
            color: var(--texto);
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        header {
            background-color: var(--azul-bebe);
            padding: 25px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            margin-bottom: 30px;
            border: 1px solid var(--azul-claro-hover);
        }

        header h1 {
            margin: 0;
            color: var(--azul-escuro);
            font-size: 28px;
            letter-spacing: 0.5px;
        }

        .conteudo {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 25px;
        }

        @media (max-width: 768px) {
            .conteudo { grid-template-columns: 1fr; }
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
            border: 1px solid #E2E8F0;
        }

        .card h2 {
            margin-top: 0;
            color: var(--azul-escuro);
            font-size: 20px;
            border-bottom: 3px solid var(--azul-bebe);
            padding-bottom: 10px;
        }

        .form-group {
            margin-bottom: 18px;
        }

        .form-group label {
            display: block;
            margin-bottom: 6px;
            font-weight: 600;
            font-size: 14px;
        }

        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 1px solid #CBD5E1;
            border-radius: 8px;
            box-sizing: border-box;
            font-size: 14px;
            transition: all 0.3s;
        }

        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: var(--azul-destaque);
            box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.25);
        }

        button {
            background-color: var(--azul-bebe);
            color: var(--azul-escuro);
            border: 1px solid var(--azul-claro-hover);
            padding: 14px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 15px;
            width: 100%;
            transition: background 0.2s, transform 0.1s;
        }

        button:hover {
            background-color: var(--azul-claro-hover);
        }

        button:active {
            transform: scale(0.98);
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 14px;
            text-align: left;
            border-bottom: 1px solid #E2E8F0;
        }

        th {
            background-color: var(--azul-bebe);
            color: var(--azul-escuro);
            font-weight: 600;
            border-radius: 4px;
        }

        tr:hover {
            background-color: #F8FAFC;
        }

        .badge-tamanho {
            background-color: #F1F5F9;
            padding: 4px 8px;
            border-radius: 6px;
            font-weight: bold;
        }

        .btn-excluir {
            background-color: #FEE2E2;
            color: #991B1B;
            padding: 6px 12px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 13px;
            font-weight: 500;
            transition: background 0.2s;
        }

        .btn-excluir:hover {
            background-color: #FCA5A5;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🩵 Loja de Roupas - Gerenciador de Estoque</h1>
        </header>

        <div class="conteudo">
            <div class="card">
                <h2>Cadastrar Nova Peça</h2>
                <form action="/adicionar" method="POST">
                    <div class="form-group">
                        <label for="nome">Nome da Roupa</label>
                        <input type="text" id="nome" name="nome" placeholder="Ex: Vestido Floral Midi" required>
                    </div>
                    <div class="form-group">
                        <label for="preco">Preço (R$)</label>
                        <input type="number" id="preco" name="preco" step="0.01" placeholder="89.90" required>
                    </div>
                    <div class="form-group">
                        <label for="tamanho">Tamanho</label>
                        <select id="tamanho" name="tamanho" required>
                            <option value="PP">PP</option>
                            <option value="P">P</option>
                            <option value="M">M</option>
                            <option value="G">G</option>
                            <option value="GG">GG</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="estoque">Quantidade em Estoque</label>
                        <input type="number" id="estoque" name="estoque" placeholder="Ex: 15" required>
                    </div>
                    <button type="submit">Adicionar ao Estoque</button>
                </form>
            </div>

            <div class="card">
                <h2>Peças em Estoque</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Descrição</th>
                            <th>Tam.</th>
                            <th>Preço</th>
                            <th>Qtd.</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for produto in produtos %}
                        <tr>
                            <td>{{ produto['nome'] }}</td>
                            <td><span class="badge-tamanho">{{ produto['tamanho'] }}</span></td>
                            <td>R$ {{ "%.2f"|format(produto['preco']) }}</td>
                            <td>{{ produto['estoque'] }} un.</td>
                            <td>
                                <a href="/deletar/{{ produto['id'] }}" class="btn-excluir">Excluir</a>
                            </td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="5" style="text-align: center; color: #94A3B8; padding: 30px;">
                                Nenhuma roupa cadastrada ainda.
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
'''

# 3. ROTAS DO SISTEMA
@app.route('/')
def index():
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM produtos ORDER BY id DESC').fetchall()
    conn.close()
    return render_template_string(HTML_LAYOUT, produtos=produtos)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    preco = float(request.form['preco'])
    tamanho = request.form['tamanho']
    estoque = int(request.form['estoque'])

    conn = get_db_connection()
    conn.execute('INSERT INTO produtos (nome, preco, tamanho, estoque) VALUES (?, ?, ?, ?)',
                 (nome, preco, tamanho, estoque))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Garante que o banco SQLite seja criado no início
    app.run(debug=True)
