from app.model.User import User

from datetime import datetime, timedelta, timezone
import hashlib, base64, json, jwt
from app.config import app_config, app_active

config = app_config[app_active]

class UserController():
    def __init__(self):
        self.user_model = User()

    ''' Autenticação JWT '''
    # Função que faz a autenticação através de um token de acesso
    def verify_auth_token(self, access_token):
        status = 401
        print("Iniciando verificação de token...")

        # Faz a autenticação do token
        try:
            jwt.decode(access_token, config.SECRET, algorithms='HS256')
            message = 'Token Válido'
            status = 200

        # Tratamento de tokens inválidos
        except jwt.ExpiredSignatureError:
            message = 'Token expirado, realize um novo login'

        except:
            message = 'Token inválido'

        return {
            'message': message,
            'status': status
        }

    # Função que gera um token de autenticação
    def generate_auth_token(self, data, exp=30, time_exp=False):

        # Determina o tempo de expiracao do token
        if time_exp == True:
            date_time = data['exp']
        else:
            # Calcula com base no horário atual
            date_time = datetime.now(timezone.utc) + timedelta(minutes=exp)

        # Cria o dicionário com os dados a serem autenticados
        dict_jwt = {
            'id': data['id'],
            'username': data['username'],
            'exp': date_time
        }

        # Encapsula os dados no formato token a partir do encode do jwt
        access_token = jwt.encode(dict_jwt, config.SECRET, algorithm='HS256')

        return access_token

    def login(self, email, password):
        #Pega os dados de e-mail e salva no 
        # atributo da model de usuário.
        self.user_model.email = email
        #Verifica se o usuário existe no banco de dados
        result = self.user_model.get_user_by_email()

        #Caso o usuário exista o result não será None
        if result is not None:
            """
            Verifica se o password que o usuário
            enviou, agora convertido em hash, é
            igual ao password que foi pego no
            banco de dados para esse usuário.
            """
            res = self.user_model.verify_password(password, result.password)
            # Se for o mesmo retornará True
            if res:
                return result
            else:
                return {}
        return {}
    
    def recovery(self, email):
        """
        A recuperação de e-mail será criada no
        capítulo 11. Trabalhando com serviços de
        e-mail.
        """
        return ''
    
    def get_user_by_id(self, user_id):
        result = {}
        try:
            self.user_model.id = user_id
            res = self.user_model.get_user_by_id()
            result = {
                'id': res.id,
                'name': res.username,
                'email': res.email,
                'date_created': res.date_created
            }
            print(result)
            status = 200
        except Exception as e:
            print(e)
            result = []
            status = 400
        finally:
            return {
                'result': result,
                'status': status
            }

    def get_admin_login(self, user_id):
        self.user_model.id = user_id
        res = self.user_model.get_user_by_id()
        #print(res)
        return res

