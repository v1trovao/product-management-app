import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.config import app_active, app_config

config = app_config[app_active]

class EmailController():
    def send_email(self, t_email, subject, content_text, f_email="contato@site.com.br"):

        print(f"Para quem? {t_email}")
        print(f"Assunto: {subject}")
        print(f"Conteúdo: {content_text}")
        # Estrutura do email
        message = Mail(
            from_email=f_email,       # Destinatário
            to_emails=t_email,        # Remetente
            subject=subject,          # Assunto
            html_content=content_text # Conteúdo
        )

        try:
            # Instância do Cliente de Email, informado pela chave API
            sg = SendGridAPIClient(config.SENDGRID_API_KEY)

            print(sg.api_key)

            # O cliente faz o envio da mensagem e guarda a resposta
            response = sg.send(message)

            #print(response)

            # 200 ou 202 para envio com sucesso
            return {
                'status_code': response.status_code,
                'body': response,
                'headers': response.headers
            }
        except Exception as e:
            print(e)
            raise e

