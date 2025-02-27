# database.py
import sqlite3
from datetime import datetime, timedelta

def criar_banco_dados():
    conn = sqlite3.connect('assinaturas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            data_cadastro TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assinaturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            canal_id TEXT NOT NULL,
            plano TEXT NOT NULL,
            metodo_pagamento TEXT NOT NULL,
            data_inicio TEXT NOT NULL,
            data_fim TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES usuarios (user_id)
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_usuario(user_id, username, first_name, last_name):
    conn = sqlite3.connect('assinaturas.db')
    cursor = conn.cursor()
    data_cadastro = datetime.now().isoformat()
    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (user_id, username, first_name, last_name, data_cadastro)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name, data_cadastro))
    conn.commit()
    conn.close()

def adicionar_assinatura(user_id, plano, metodo_pagamento, canal_id):
    conn = sqlite3.connect('assinaturas.db')
    cursor = conn.cursor()

    # Verifica se o usuário já tem uma assinatura ativa para o mesmo canal
    cursor.execute('''
        SELECT data_fim FROM assinaturas
        WHERE user_id = ? AND canal_id = ? AND status = 'ativa'
        ORDER BY data_fim DESC
        LIMIT 1
    ''', (user_id, canal_id))
    resultado = cursor.fetchone()

    if resultado:
        # Se houver uma assinatura ativa, calcula a nova data_fim
        data_fim_existente = datetime.fromisoformat(resultado[0])
        if plano == "mensal":
            nova_data_fim = data_fim_existente + timedelta(days=30)
        elif plano == "anual":
            nova_data_fim = data_fim_existente + timedelta(days=365)
        elif plano == "vitalicia":
            nova_data_fim = datetime.max  # Data distante no futuro
    else:
        # Se não houver assinatura ativa, cria uma nova
        data_inicio = datetime.now().isoformat()
        if plano == "mensal":
            nova_data_fim = datetime.now() + timedelta(days=30)
        elif plano == "anual":
            nova_data_fim = datetime.now() + timedelta(days=365)
        elif plano == "vitalicia":
            nova_data_fim = datetime.max  # Data distante no futuro

    # Adiciona a nova assinatura ao banco de dados
    data_inicio = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO assinaturas (user_id, canal_id, plano, metodo_pagamento, data_inicio, data_fim, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, canal_id, plano, metodo_pagamento, data_inicio, nova_data_fim.isoformat(), 'ativa'))

    conn.commit()
    conn.close()

def verificar_assinaturas_usuario(user_id):
    conn = sqlite3.connect('assinaturas.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT canal_id, plano, data_fim FROM assinaturas
        WHERE user_id = ? AND status = 'ativa' AND data_fim > ?
    ''', (user_id, datetime.now().isoformat()))
    assinaturas = cursor.fetchall()
    conn.close()
    return assinaturas

def cancelar_assinatura(user_id, canal_id):
    conn = sqlite3.connect('assinaturas.db')
    cursor = conn.cursor()

    # Atualiza o status da assinatura para 'cancelada'
    cursor.execute('''
        UPDATE assinaturas
        SET status = 'cancelada'
        WHERE user_id = ? AND canal_id = ? AND status = 'ativa'
    ''', (user_id, canal_id))

    conn.commit()
    conn.close()

def verificar_assinaturas_expiradas(bot):
    conn = sqlite3.connect('assinaturas.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_id, canal_id FROM assinaturas
        WHERE data_fim < ? AND status = 'ativa'
    ''', (datetime.now().isoformat(),))
    assinaturas_expiradas = cursor.fetchall()

    for user_id, canal_id in assinaturas_expiradas:
        # Remove o usuário do canal (implemente essa função)
        remover_usuario_do_canal(bot, user_id, canal_id)

        # Atualiza o status da assinatura
        cursor.execute('''
            UPDATE assinaturas
            SET status = 'expirada'
            WHERE user_id = ? AND canal_id = ?
        ''', (user_id, canal_id))

    conn.commit()
    conn.close()