from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = "categorias_galeria"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False, unique=True)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome}

    def cadastrar(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Já existe uma categoria com este nome.")

    def atualizar(self, novo_nome):
        try:
            self.nome = novo_nome
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Já existe outra categoria com este nome.")

    def deletar(self):
        if Midia.query.filter_by(categoria_id=self.id).count() > 0:
            raise ValueError("Não é possível excluir: existem mídias vinculadas a esta categoria.")
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def listar_todas(cls):
        return [c.to_dict() for c in cls.query.order_by(cls.id.asc()).all()]

class Midia(db.Model):
    __tablename__ = "midias"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias_galeria.id", ondelete="RESTRICT"), nullable=False)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    url_midia = db.Column(db.String(500), nullable=False)
    tipo_midia = db.Column(db.Enum("foto", "video"), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    visualizacoes = db.Column(db.Integer, nullable=False, default=0)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, server_default=func.now())
    categoria = db.relationship("Categoria", backref=db.backref("midias", lazy=True))

    def to_dict(self):
        return {
            "id": self.id, "categoria_id": self.categoria_id,
            "categoria_nome": self.categoria.nome if self.categoria else None,
            "titulo": self.titulo, "descricao": self.descricao, "url_midia": self.url_midia,
            "tipo_midia": self.tipo_midia, "ano": self.ano, "visualizacoes": self.visualizacoes,
            "ativo": bool(self.ativo), "criado_em": self.criado_em.isoformat() if self.criado_em else None
        }

    def cadastrar(self):
        db.session.add(self)
        db.session.commit()
        return self

    def atualizar(self, dados):
        if "titulo" in dados: self.titulo = dados["titulo"]
        if "descricao" in dados: self.descricao = dados["descricao"]
        if "url_midia" in dados: self.url_midia = dados["url_midia"]
        if "tipo_midia" in dados: self.tipo_midia = dados["tipo_midia"]
        if "ano" in dados: self.ano = int(dados["ano"])
        if "ativo" in dados: self.ativo = bool(dados["ativo"])
        db.session.commit()
        return self

    def alternar_status(self):
        self.ativo = not bool(self.ativo)
        db.session.commit()
        return self

    @classmethod
    def listar_todas_admin(cls):
        return [m.to_dict() for m in cls.query.order_by(cls.id.asc()).all()]

class Apoiador(db.Model):
    __tablename__ = "apoiadores"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_empresa = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    logo_url = db.Column(db.String(500), nullable=False)
    site_url = db.Column(db.String(500), nullable=True)
    visualizacoes = db.Column(db.Integer, nullable=False, default=0)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id, "nome_empresa": self.nome_empresa, "descricao": self.descricao,
            "logo_url": self.logo_url, "site_url": self.site_url, "visualizacoes": self.visualizacoes,
            "ativo": bool(self.ativo)
        }

    def cadastrar(self):
        db.session.add(self)
        db.session.commit()
        return self

    def atualizar(self, dados):
        if "nome_empresa" in dados: self.nome_empresa = dados["nome_empresa"]
        if "descricao" in dados: self.descricao = dados["descricao"]
        if "logo_url" in dados: self.logo_url = dados["logo_url"]
        if "site_url" in dados or "maps_url" in dados: self.site_url = dados.get("site_url") or dados.get("maps_url")
        if "ativo" in dados: self.ativo = bool(dados["ativo"])
        db.session.commit()
        return self

    def alternar_status(self):
        self.ativo = not bool(self.ativo)
        db.session.commit()
        return self

    @classmethod
    def listar_todos_admin(cls):
        return [a.to_dict() for a in cls.query.order_by(cls.id.asc()).all()]

class EstatisticaGrupo(db.Model):
    __tablename__ = "estatisticas_grupo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantidade_participantes = db.Column(db.Integer, nullable=False, default=48)
    quantidade_torneios = db.Column(db.Integer, nullable=False, default=14)
    ano_fundacao = db.Column(db.Integer, nullable=False, default=2019)

    def to_dict(self):
        return {
            "id": self.id, "quantidade_participantes": self.quantidade_participantes,
            "quantidade_torneios": self.quantidade_torneios, "ano_fundacao": self.ano_fundacao
        }

    @classmethod
    def obter_estatisticas(cls):
        est = cls.query.first()
        if not est:
            est = cls(quantidade_participantes=48, quantidade_torneios=14, ano_fundacao=2019)
            db.session.add(est)
            db.session.commit()
        return est

    def atualizar_metricas(self, participantes, torneios, ano_fundacao):
        if participantes is not None: self.quantidade_participantes = int(participantes)
        if torneios is not None: self.quantidade_torneios = int(torneios)
        if ano_fundacao is not None: self.ano_fundacao = int(ano_fundacao)
        db.session.commit()
        return self