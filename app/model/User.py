# -*- coding: utf-8 -*-
from sqlalchemy.orm import relationship
from sqlalchemy import func
from app.config import app_config, app_active
from app.model.Role import Role
from app.extensions import db
from passlib.hash import pbkdf2_sha256
from flask_login import UserMixin

# Chamando config e db para conectar o model com o banco de dados
# config = app_config[app_active]

# Um usuário que acessa o sistema, pode ser:
# ADMIN, GERENTE, LOJISTA ou CLIENTE/USUÁRIO
class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(40),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(256),nullable=False)

    date_created=db.Column(db.DateTime(6),default=db.func.current_timestamp(), nullable=False)
    last_update=db.Column(db.DateTime(6),onupdate=db.func.current_timestamp(), nullable=True)

    recovery_code=db.Column(db.String(200),nullable=True)
    active=db.Column(db.Boolean(),default=1,nullable=True)
    role=db.Column(db.Integer,db.ForeignKey(Role.id),nullable=False)
    funcao=relationship(Role, lazy='selectin')

    # Adicione estes métodos
    def get_user_by_email(self):
        """
        Retorna um usuário consultado no banco pelo E-mail
        """
        try:
            res = db.session.query(User).filter(User.email == self.email).first()
        except Exception as e:
            res = [] 
            print(e)
        finally:
            db.session.close()
            return res
    def get_user_by_id(self):
        """
        Retorna o usuário consultado no banco pelo ID
        """
        try:
            res = db.session.query(User).filter(User.id==self.id).first()
        except Exception as e:
            res = []
            print(e)
        finally: 
            db.session.close()
            return res

    def get_user_by_name(self):
        try:
            res = db.session.query(User).filter(User.username==self.username).first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
        return res

    def get_user_by_recovery(self):
        """Retorna um usuário pelo código de recuperação"""
        try:
            res = db.session.query(User).filter(User.recovery_code==self.recovery_code).first()
        except Exception as e:
            res = None
            print(e)
        finally:
            db.session.close()
        return res
    
    def save(self):
        try:
            db.session.add(self)
            #print("Salvando...")
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
    
    def update(self, obj):
        """
        Atualiza os dados de um usuário no banco
        """
        try:
            res = db.session.query(User).filter(User.id == self.id).update(obj)
            db.session.commit()
            return True

        except Exception as e:
            print(e)
            db.session.rollback()
            return False
    
    def hash_password(self, password):
        try:
            return pbkdf2_sha256.hash(password)
        except Exception as e:
            print("Erro ao criptografar senha %s" % e)

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def verify_password(self, password_no_hash, password_database):
        try:
            return pbkdf2_sha256.verify(password_no_hash, password_database)
        
        except ValueError:
            return False
    
    def __repr__(self):
        return f'{self.id} - {self.username}'
    
    def get_total_users(self):
        try:
            res = db.session.query(func.count(User.id)).first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res;