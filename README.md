## Movie Magic

O projeto **Movie Magic** se trata de utilizar o banco de dados Pagila para análise e criação de um modelo de churn, assim como um método de deploy.

### MovieMagic_Analise.ipynb

Este arquivo Jupyter Notebook faz parte do projeto **Movie Magic** e tem como objetivo realizar uma análise exploratória dos dados contidos no banco de dados Pagila. O notebook utiliza a biblioteca SQL Alchemy para executar consultas ao banco de dados e responder a algumas perguntas específicas sobre os dados. As análises e insights obtidos são valiosos para entender melhor o dataset e podem ser úteis para tomar decisões informadas no projeto.

### churn_model.ipynb

Este arquivo Jupyter Notebook faz parte do projeto **Movie Magic** e é responsável por criar um modelo de churn utilizando os dados do banco de dados Pagila. O notebook abrange as seguintes etapas:

1. Análise e pré-processamento dos dados: Os dados são carregados a partir do banco de dados e são realizadas etapas de limpeza e tratamento.

2. Modelagem: Dois modelos são testados - Random Forest e Regressão Logística - para prever o churn dos clientes. O notebook inclui ajuste de hiperparâmetros (tuning) e avaliação de desempenho dos modelos.

3. Exportação do Modelo: O modelo Random Forest é escolhido como o melhor e é exportado para um arquivo PKL para uso posterior.

### app.py

O arquivo `app.py` é uma parte fundamental do projeto **Movie Magic**. Ele desempenha um papel importante na identificação de clientes em risco de churn e no envio de e-mails personalizados para incentivar esses clientes a retornar à locadora de filmes **Movie Magic**.

Para utilizar o `app.py`, siga estas etapas:

1. Certifique-se de que todas as bibliotecas necessárias estão instaladas. Você pode instalá-las executando `pip install pandas joblib sqlalchemy smtplib email.mime.text email.mime.multipart`.

2. Antes de executar o script, configure um arquivo `config.json` no diretório `config` com as informações de configuração necessárias. O arquivo `config.json` deve conter as informações do seu banco de dados PostgreSQL.

3. Execute o `app.py`. Ele analisará os dados do banco de dados e identificará os clientes com alto risco de churn.

4. Você será solicitado a escolher uma opção:
   - Opção 1: Enviar e-mail para prevenção de churn e salvar os dados em um arquivo CSV.
   - Opção 2: Apenas salvar os dados em um arquivo CSV.

5. Se você escolher a Opção 1, o script enviará e-mails personalizados para os clientes identificados em risco de churn. Certifique-se de configurar suas informações de e-mail (smtp_server, smtp_port, username e password) no script para que os e-mails possam ser enviados.

6. Se você escolher a Opção 2, o script salvará os dados em um arquivo CSV no diretório atual.

Lembre-se de que a funcionalidade de envio de e-mails requer a configuração de um servidor SMTP e uma conta de e-mail válida. Certifique-se de configurar essas informações corretamente no script para que os e-mails possam ser enviados com sucesso.

## Formato do arquivo json.
{
  "db_user": "seu_usuario",
  "db_password": "sua_senha",
  "db_name": "nome_do_banco_de_dados",
  "db_host": "host_do_banco_de_dados"
}
