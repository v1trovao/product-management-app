# -*- coding: utf-8 -*-
from app.extensions import db
from sqlalchemy import func

class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),unique=True,nullable=False)
    description=db.Column(db.Text(),nullable=False)

    # Apresentar os resultados na tela de forma mais legível
    # mas ainda permite acessar os atributos do objeto
    def __repr__(self):
        return self.name

    # Função que retorna todos os objetos Categoria do banco
    def get_total_category(self):
        try:
            res = db.session.query(func.count(Category.id)).first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res