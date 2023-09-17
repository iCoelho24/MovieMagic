import pandas as pd
import joblib
from sqlalchemy import create_engine
import warnings
import json
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

warnings.filterwarnings("ignore")
pd.set_option('display.float_format', lambda x: '%.2f' % x)

Model = joblib.load("Modelo_churn_RF")

with open('config/config.json', 'r') as config_file:
    config = json.load(config_file)

DB_USER = config['db_user']
DB_PASSWORD = config['db_password']
DB_NAME = config['db_name']
DB_HOST = config['db_host']

# Configurações do servidor SMTP do Gmail e informações da conta de e-mail
smtp_server = 'smtp.gmail.com'
smtp_port = 587
username = ''
password = ''

###########
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

data = """
SELECT 
        CUSTOMER.CUSTOMER_ID,
        INVENTORY.FILM_ID,
        PAYMENT.AMOUNT,
        RENTAL.RENTAL_DATE,
        INVENTORY.STORE_ID,
        RENTAL.STAFF_ID,
        FILM.RENTAL_DURATION
FROM CUSTOMER
JOIN PAYMENT ON PAYMENT.CUSTOMER_ID = CUSTOMER.CUSTOMER_ID
JOIN RENTAL ON RENTAL.CUSTOMER_ID = CUSTOMER.CUSTOMER_ID
JOIN INVENTORY ON INVENTORY.INVENTORY_ID = RENTAL.INVENTORY_ID
JOIN FILM ON FILM.FILM_ID = INVENTORY.FILM_ID
"""

data = pd.read_sql_query(data, engine)

customer_data = """
SELECT 
        customer_id, 
        first_name as nome, 
        last_name as sobrenome, 
        email 
FROM CUSTOMER
"""

customer_data = pd.read_sql_query(customer_data, engine)

customer_id = data['customer_id']

def tratamento(data):
    # Excluindo a coluna customer_id
    data.drop('customer_id', axis=1, inplace=True)

    # Deixando a data no formato UNIX
    data['rental_date'] = data['rental_date'].apply(lambda x: x.timestamp())

tratamento(data)
pred = Model.predict(data)
data['churn'] = pred

data['customer_id'] = customer_id
data = data[data['churn'] == 1]

data = data.drop_duplicates(subset=['customer_id'])
df_merged = data.merge(customer_data, on='customer_id')[['customer_id', 'nome', 'sobrenome', 'email', 'churn']]

print("******************************")
print("Opções disponíveis:")
print("1. Enviar e-mail para prevenção de churn e salvar o arquivo em CSV.")
print("2. Apenas salvar o arquivo em CSV.")
print("******************************")

escolha = input("Por favor, insira 1 ou 2 para fazer a sua escolha: ")

if escolha == '1':
    print("Você escolheu enviar o e-mail para prevenção de churn e salvar o arquivo em CSV.")
    nome_arquivo = input("Por favor, insira o nome do arquivo CSV para salvar os dados: ")

    if not nome_arquivo.endswith('.csv'):
        nome_arquivo += '.csv'
        
    df_merged.to_csv(nome_arquivo, index=False)

    print(f"Os dados foram salvos no arquivo {nome_arquivo}.")

    print('Agora iremos começar a enviar os e-mails.')

    for index, row in df_merged.iterrows():
        receiver_email = row['email']
        
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()

        # Efetuar login na conta de e-mail
        smtp.login(username, password)

        # Criar mensagem de e-mail
        sender_email = ''
        subject = 'Volte a nos visitar.'
        message = """        
        Prezado,

        Esperamos que este e-mail o encontre bem. Na Movie Magic, valorizamos muito a sua preferência e estamos ansiosos para tê-lo de volta como nosso cliente.

        Percebemos que você não visitou nossa locadora recentemente, e gostaríamos de lhe oferecer um incentivo especial para que volte a aproveitar nossos serviços. Estamos oferecendo um desconto exclusivo de 15%' em sua próxima locação de filmes!

        Na Movie Magic, temos uma vasta seleção de filmes dos mais variados gêneros, desde os clássicos até os lançamentos mais recentes. Temos certeza de que você encontrará algo que desperte o seu interesse.

        Para aproveitar este desconto especial, basta usar o código de cupom "VOLTE15" no momento do pagamento em nossa loja física ou ao alugar online em nosso site.

        Não deixe passar essa oportunidade de desfrutar de uma ótima noite de entretenimento com filmes de qualidade a um preço reduzido.

        Esperamos vê-lo em breve na Movie Magic. Se tiver alguma dúvida ou precisar de assistência, não hesite em nos contatar.

        Obrigado por escolher a Movie Magic como sua locadora de filmes de confiança.

        Atenciosamente,
        Equipe Movie Magic
        """

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        smtp.sendmail(sender_email, receiver_email, msg.as_string())

        smtp.quit()

    print('Parabéns, todos os e-mail foram enviados.')
elif escolha == '2':
    print("Você escolheu apenas salvar o arquivo em CSV.")
    nome_arquivo = input("Por favor, insira o nome do arquivo CSV para salvar os dados: ")

    if not nome_arquivo.endswith('.csv'):
        nome_arquivo += '.csv'
        
    df_merged.to_csv(nome_arquivo, index=False)

    print(f"Os dados foram salvos no arquivo {nome_arquivo}.")
else:
    print("Opção inválida. Por favor, insira 1 ou 2 para fazer a sua escolha.")