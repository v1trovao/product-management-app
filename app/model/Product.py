# -*- coding: utf-8 -*-
from markupsafe import Markup
from sqlalchemy.orm import relationship
from sqlalchemy import func, desc, asc, distinct, text
from app.model.User import User
from app.model.Category import Category
from app.extensions import db

class Product(db.Model):
    id              =db.Column(db.Integer,primary_key=True)
    name            =db.Column(db.String(20),unique=True,nullable=False)
    description     =db.Column(db.Text(),nullable=False)
    qtd             =db.Column(db.Integer,nullable=True,default=0)
    image           =db.Column(db.Text(),nullable=True)
    price           =db.Column(db.Numeric(10,2),nullable=False)
    date_created    =db.Column(db.DateTime(6),default=db.func.current_timestamp(),
                               nullable=False)
    last_update     =db.Column(db.DateTime(6),onupdate=db.func.current_timestamp(), 
                               nullable=False)
    status          =db.Column(db.Boolean(),default=1,nullable=True)
    user_created    =db.Column(db.Integer,db.ForeignKey(User.id),nullable=False)
    category        =db.Column(db.Integer,db.ForeignKey(Category.id),nullable=False)
    usuario=relationship(User)
    categoria=relationship(Category)

    # Função db que retorna uma lista com todos os produtos registrados 
    def get_total_product(self):
        try:
            res = db.session.query(func.count(Product.id)).first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res
        
    def get_last_products(self):
        try:
            res = db.session.query(Product).order_by(Product.date_created).limit(5).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res

        
    # Função db que retorna uma lista dos produtos registrados com base no limite
    def get_all(self, limit):
        try:
            if limit is None:
                # Faz a consulta por todos os produtos do banco
                res = db.session.query(Product).all()
            
            else:
                res = db.session.query(Product).order_by(Product.date_created).limit(limit).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            # Após finalizar a consulta, encerra a conexão e retorna o resultado
            db.session.close()
            return res
    
    def get_product_by_id(self):
        try:
            #res = db.session.query(Product).filter(Product.id == self.id).first()
            res = db.session.get(Product, self.id)
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return (res)
    
    # Função que adiciona um objeto Produto e salva no banco
    # Obs: O commit() e o rollback(), após executarem já finalizam a conexão, 
    # sem precisar do db.session.close()
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        
        # Se houver erro, desfaz a operação
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    # Função que atualiza um objeto salvo no banco
    def update(self, obj):
        try:
            # Inicia a consulta buscando o produto pelo ID e atualizando 
            res = db.session.query(Product).filter(Product.id == self.id).update(obj)
            db.session.commit()
            return True
        except Exception as e:
            # Se houver erro, desfaz a operação
            print(e)
            db.session.rollback()
            return False
    
    # Função que deleta um objeto salvo no banco
    def delete(self):
        try:
            db.session.query(Product).filter(Product.id == self.id).delete()
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
    

    def __repr__(self):
        return f'{self.id}-{self.name}'
    
    @property
    def image_preview(self):
        if self.image:
            return Markup(f'<img src="{self.image}" width="80">')
        return 'Image'