from flask import Blueprint, request, jsonify, session
import hashlib
import os

auth_bp = Blueprint('auth', __name__)

# Hash das credenciais para segurança (não ficam visíveis no código)
# usuário: agronorte, senha: ferriagronorte
USUARIO_HASH = hashlib.sha256('agronorte'.encode()).hexdigest()
SENHA_HASH = hashlib.sha256('ferriagronorte'.encode()).hexdigest()

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint para autenticação do usuário"""
    try:
        data = request.get_json()
        
        if not data or 'usuario' not in data or 'senha' not in data:
            return jsonify({'success': False, 'message': 'Usuário e senha são obrigatórios'}), 400
        
        usuario = data['usuario'].strip()
        senha = data['senha'].strip()
        
        # Verificar credenciais usando hash
        usuario_hash = hashlib.sha256(usuario.encode()).hexdigest()
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        if usuario_hash == USUARIO_HASH and senha_hash == SENHA_HASH:
            # Criar sessão
            session['authenticated'] = True
            session['usuario'] = usuario
            return jsonify({'success': True, 'message': 'Login realizado com sucesso'})
        else:
            return jsonify({'success': False, 'message': 'Usuário ou senha incorretos'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro interno do servidor'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Endpoint para logout do usuário"""
    try:
        session.clear()
        return jsonify({'success': True, 'message': 'Logout realizado com sucesso'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro interno do servidor'}), 500

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    """Endpoint para verificar se o usuário está autenticado"""
    try:
        if session.get('authenticated'):
            return jsonify({'authenticated': True, 'usuario': session.get('usuario')})
        else:
            return jsonify({'authenticated': False})
    except Exception as e:
        return jsonify({'authenticated': False, 'message': 'Erro interno do servidor'}), 500

@auth_bp.route('/protected', methods=['GET'])
def protected():
    """Endpoint protegido - exemplo de como verificar autenticação"""
    try:
        if not session.get('authenticated'):
            return jsonify({'success': False, 'message': 'Acesso negado. Faça login primeiro.'}), 401
        
        return jsonify({'success': True, 'message': 'Acesso autorizado', 'usuario': session.get('usuario')})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro interno do servidor'}), 500

