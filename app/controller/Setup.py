from app.model.User import User
from app.model.Role import Role

from datetime import datetime, timedelta, timezone

from app.config import app_config, app_active
from app.config import default_roles, default_admin

config = app_config[app_active]

class SetupController():
    def __init__(self):
        self.user_model = User()
        self.role_model = Role()

    def create_default_roles(self):

        # Limpar valores padrão
        # self.role_model.remove_default_roles()

        # Percorre a lista de funções padrão
        for role_name in default_roles:
        
            self.role_model.name = role_name
            role_exist = self.role_model.get_role_by_name()

            # Verifica se a função já existe no banco
            if not role_exist:
                # Senão existe, registra a função no banco
                print(f"Adicionando...{role_name}")

                new_role = self.role_model.__class__()
                new_role.name = role_name
                new_role.save()

        # Verificar as roles existentes no banco
        roles = self.role_model.get_all_roles()
        print(roles)

    def create_default_admin(self):

        # Obtem o id associado ao admin 
        admin_role = self.role_model.get_default_admin()

        # Confirma se já existe admin padrão no banco
        self.user_model.email = default_admin['email']
        res = self.user_model.get_user_by_email()

        if not res:
            print("ADMIN ainda não foi registrado")
            print("-> Adicionando o default...")
            self.user_model.username = default_admin['username']
            self.user_model.password = self.user_model.hash_password(default_admin['password'])
            self.user_model.date_created = datetime.now(timezone.utc)
            self.user_model.last_update = datetime.now(timezone.utc)
            self.user_model.role = admin_role
            self.user_model.save()
        else:
            print("Admin já registrado...")

    def check_admin(self):
        self.user_model.username = default_admin['username']
        return self.user_model.get_user_by_name() is not None
    
    def set_default_values(self):
        pass
        