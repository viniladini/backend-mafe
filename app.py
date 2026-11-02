from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import check_password_hash
from config import Config
from models import db, Categoria, Midia, Apoiador, EstatisticaGrupo

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/api/*": {"origins": "*"}})
db.init_app(app)

def resposta_padrao(sucesso, dados=None, mensagem="", status_code=200):
    return jsonify({
        "sucesso": sucesso, "success": sucesso,
        "dados": dados if dados is not None else [],
        "mensagem": mensagem
    }), status_code

@app.route("/api/status", methods=["GET"])
def status():
    return resposta_padrao(True, {"servidor": "online"}, "API Flask MAFE rodando com sucesso!", 200)

@app.route("/api/login", methods=["POST"])
def login():
    dados = request.get_json(silent=True) or {}
    usuario = (dados.get("usuario") or dados.get("username") or "").strip()
    senha = str(dados.get("senha") or dados.get("password") or "")
    if usuario == app.config["ADMIN_USER"] and check_password_hash(app.config["ADMIN_PASSWORD_HASH"], senha):
        return resposta_padrao(True, {"usuario": usuario, "token": "token_jwt_mafe"}, "Login realizado com sucesso.", 200)
    return resposta_padrao(False, None, "Usuário ou senha incorretos!", 401)

@app.route("/api/admin/categorias", methods=["GET", "POST"])
def gerenciar_categorias():
    if request.method == "GET":
        return resposta_padrao(True, Categoria.listar_todas(), "Categorias listadas.", 200)
    dados = request.get_json(silent=True) or {}
    nova = Categoria(nome=(dados.get("nome") or "").strip()).cadastrar()
    return resposta_padrao(True, nova.to_dict(), "Categoria cadastrada.", 200)

@app.route("/api/admin/categorias/<int:id>", methods=["PUT", "DELETE"])
def modificar_categoria(id):
    cat = Categoria.query.get_or_404(id)
    if request.method == "PUT":
        cat.atualizar((request.get_json(silent=True) or {}).get("nome"))
        return resposta_padrao(True, cat.to_dict(), "Categoria atualizada.", 200)
    cat.deletar()
    return resposta_padrao(True, {"id": id}, "Categoria excluída.", 200)

@app.route("/api/admin/midias", methods=["GET", "POST"])
def gerenciar_midias():
    if request.method == "GET":
        return resposta_padrao(True, Midia.listar_todas_admin(), "Mídias listadas.", 200)
    d = request.get_json(silent=True) or {}
    nova = Midia(
        categoria_id=d.get("categoria_id"), titulo=d.get("titulo"),
        descricao=d.get("descricao"), url_midia=d.get("url_midia"),
        tipo_midia=d.get("tipo_midia", "foto"), ano=d.get("ano", 2026)
    ).cadastrar()
    return resposta_padrao(True, nova.to_dict(), "Mídia cadastrada.", 200)

@app.route("/api/admin/midias/<int:id>/status", methods=["PATCH"])
@app.route("/api/admin/midias/<int:id>", methods=["DELETE"])
def status_midia(id):
    midia = Midia.query.get_or_404(id)
    midia.alternar_status()
    return resposta_padrao(True, midia.to_dict(), "Status alterado.", 200)

@app.route("/api/admin/apoiadores", methods=["GET", "POST"])
def gerenciar_apoiadores():
    if request.method == "GET":
        return resposta_padrao(True, Apoiador.listar_todos_admin(), "Apoiadores listados.", 200)
    d = request.get_json(silent=True) or {}
    novo = Apoiador(
        nome_empresa=d.get("nome_empresa"), descricao=d.get("descricao"),
        logo_url=d.get("logo_url"), site_url=d.get("site_url") or d.get("maps_url")
    ).cadastrar()
    return resposta_padrao(True, novo.to_dict(), "Apoiador cadastrado.", 200)

@app.route("/api/admin/apoiadores/<int:id>/status", methods=["PATCH"])
@app.route("/api/admin/apoiadores/<int:id>", methods=["DELETE"])
def status_apoiador(id):
    ap = Apoiador.query.get_or_404(id)
    ap.alternar_status()
    return resposta_padrao(True, ap.to_dict(), "Status alterado.", 200)

@app.route("/api/admin/estatisticas", methods=["GET", "PUT"])
def gerenciar_estatisticas():
    est = EstatisticaGrupo.obter_estatisticas()
    if request.method == "GET":
        return resposta_padrao(True, est.to_dict(), "Estatísticas obtidas.", 200)
    d = request.get_json(silent=True) or {}
    est.atualizar_metricas(d.get("quantidade_participantes"), d.get("quantidade_torneios"), d.get("ano_fundacao"))
    return resposta_padrao(True, est.to_dict(), "Estatísticas atualizadas.", 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)