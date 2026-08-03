# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from app.extensions import db
from app.config import default_roles, default_admin

class Role(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40),unique=True,nullable=False)

    def __repr__(self):
        return self.name

    def get_role_by_name(self):
        try:
            res = db.session.query(Role).filter(Role.name == self.name).first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()

        return res
    
    def get_total_roles(self):
        try:
            res = db.session.query(func.count(Role.id)).first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
        return res

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
            

    # Função que verifica se o papel de admin existe no banco, 
    # retornando o ID registrado
    def get_default_admin(self):

        # Verificar se já existe no banco
        try:
            res = db.session.query(Role.id).filter_by(name='Admin').scalar()

        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
        return res

    def get_all_roles(self):
        try:
            res = db.session.query(Role).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
        return res

    def remove_default_roles(self):
        print("Cleaning roles...")

        try:
            db.session.query(Role).filter(Role.name.in_(default_roles)).delete(synchronize_session=False)

            db.session.commit()
            print("Cleaning finished!")

        except Exception as e:
            db.session.rollback()
            print(f"Cleaning error: {e}")