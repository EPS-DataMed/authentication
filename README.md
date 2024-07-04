# Authentication

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=EPS-DataMed_authentication&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=EPS-DataMed_authentication) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=EPS-DataMed_authentication&metric=coverage)](https://sonarcloud.io/summary/new_code?id=EPS-DataMed_authentication) [![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=EPS-DataMed_authentication&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=EPS-DataMed_authentication)

Serviço do DataMed responsável pelo gerenciamento de autenticação de usuários e permissões

## Requisitos

- Python 3.9 ou superior
- SQLite (ou outro banco de dados de sua escolha)

Lembre-se de criar um arquivo .env com suas informações para que o projeto funcione.

Na pasta base do repositório foi criado um arquivo .env de exemplo para ser seguido.

## Instalação

1. Clone o repositório:

2. Crie um ambiente virtual
```
python -m venv venv
source venv/bin/activate 
```
Obs: No Windows use `venv\Scripts\activate`

3. Instale as dependências:
```
pip install -r requirements.txt
```

4. Rode o projeto
```
uvicorn app.main:app --reload
```

Obs: para rodar os testes:
```
pytest
```