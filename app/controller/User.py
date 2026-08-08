from app.model.User import User

from datetime import datetime, timedelta, timezone
import hashlib, base64, json, jwt
from app.config import app_config, app_active

from app.controller.Email import EmailController

config = app_config[app_active]

class UserController():
    def __init__(self):
        self.user_model = User()
        self.email_controller = EmailController()

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

        print("Usuário retornado pelo email: ", result)

        #Caso o usuário exista o result não será None
        if result is not None:
            """
            Verifica se o password que o usuário
            enviou, agora convertido em hash, é
            igual ao password que foi pego no
            banco de dados para esse usuário.
            """
            res = self.user_model.verify_password(password, result.password)
            print(f"Verificou a senha? {res}")
            # Se for o mesmo retornará True
            if res:
                return result
            else:
                return {}
        return {}
    
    def recovery(self, email):
        """
        Função que envia um token de recuperação de senha
        para um e-mail fornecido
        """
        print("Email informado: ", email)
        self.user_model.email = email
        res = self.user_model.get_user_by_email()

        print(f"Usuário retornado pelo email: {res}")

        if res is not None:
            user_id = res.id
            username = res.username

            recovery_code = self.generate_auth_token({
                'id': user_id,
                'username': username
            }, exp=5)

            try:
                # Atualiza o usuário no banco
                self.user_model.id = res.id
                res = self.user_model.update({
                    'recovery_code': recovery_code
                })

                print(res)

                if res:
                    # Se atualizou, cria a mensagem de texto e a rota de acesso
                    content_text = f'Olá {username}. Para realizar a alteração de senha,' \
                    f'você precisa acessar a seguinte url: {config.URL_MAIN}new-password/{recovery_code}'
                else:
                    # Em caso de falha, retorna mensagem de erro
                    return {
                        'status_code': 401,
                        'body': 'Erro de acesso ao usuário'
                    }
                print(content_text)

            except:
                return {
                    'status_code': 401,
                    'body': 'Erro ao processar recuperação de senha'
                }

            try:
                # Envia o email para o usuário
                result = self.email_controller.send_email(email, "Recuperação de senha", content_text)

            except:
                return {
                    'status_code': 401,
                    'body': 'Erro no serviço de email. Por favor, entre em contato com administrador...'
                }

        else:
            result = {
                'status_code': 401,
                'body': 'Usuário inexistente'
            }

        return result

    def get_user_by_recovery(self, recovery_password):
        """Obtem usuário no banco pelo código de recuperação"""
        self.user_model.recovery_code = recovery_password
        return self.user_model.get_user_by_recovery()

    def new_password(self, user_id, password):
        """Atualiza a senha de um usuário"""
        self.user_model.set_password(password)
        self.user_model.id = user_id

        return self.user_model.update({
            'password': self.user_model.password
        })
    
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

