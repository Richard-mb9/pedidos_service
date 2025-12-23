# Pedidos Service

Serviço de gerenciamento de pedidos desenvolvido com FastAPI, MongoDB e RabbitMQ.

## Tecnologias Utilizadas

- **Python 3.12**
- **FastAPI** - Framework web moderno e de alta performance
- **MongoDB** - Banco de dados NoSQL para persistência de dados
- **RabbitMQ** - Message broker para comunicação assíncrona
- **Uvicorn** - Servidor ASGI de alta performance
- **Pytest** - Framework de testes
- **Docker** - Containerização da aplicação

## Dependências

A aplicação depende das seguintes infraestruturas:

- **MongoDB** - Banco de dados principal
- **RabbitMQ** - Fila de mensagens para processamento assíncrono

## Rodando a Aplicação

### Com Docker (Recomendado)

Para rodar a aplicação completa com todas as dependências, utilize o Docker Compose:

```bash
docker-compose up
```

Este comando irá inicializar:

- MongoDB (porta 27017)
- RabbitMQ (porta 5672 e interface de gerenciamento na porta 15672)
- Orders Service (porta 8000)

### Acessando a Aplicação

Após a aplicação estar em execução, ela estará disponível em:

- **API**: http://localhost:8000
- **Documentação OpenAPI (ReDoc)**: http://localhost:8000/doc/redoc
- **RabbitMQ Management**: http://localhost:15672 (usuário: guest, senha: guest)

## Documentação da API

A aplicação disponibiliza documentação interativa OpenAPI através do ReDoc. Após iniciar a aplicação, acesse:

**http://localhost:8000/doc/redoc**

A documentação contém todos os endpoints disponíveis, modelos de dados, e exemplos de uso.

## Testes

### Rodando os Testes Automatizados

Para executar os testes automatizados, utilize o script fornecido:

```bash
./run_tests.sh
```

### O que o script de testes faz:

1. Inicializa um container RabbitMQ de teste usando o arquivo `docker-compose-test.yml`
2. Aguarda os serviços estarem prontos
3. Executa os testes com pytest
4. Gera relatório de cobertura de código
5. Limpa os containers de teste automaticamente ao finalizar

### Relatório de Cobertura

Após executar os testes, um relatório de cobertura HTML é gerado em:

```
htmlcov/index.html
```

Abra este arquivo em seu navegador para visualizar a cobertura de código detalhada.

## Variáveis de Ambiente

A aplicação utiliza variáveis de ambiente para configuração. Um arquivo `.env.local` deve estar presente na raiz do projeto com as seguintes variáveis:

```env
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DATABASE=orders
MONGO_USER=mongo
MONGO_PASSWORD=mongo

MQ_HOST=localhost
MQ_PORT=5672
MQ_USER=guest
MQ_PASSWORD=guest
```

**Nota**: Ao rodar com Docker Compose, as variáveis de ambiente são configuradas automaticamente nos containers.

## Desenvolvimento

### Instalando Dependências Localmente

Para desenvolvimento local, crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Rodando Localmente (sem Docker)

1. Certifique-se de ter MongoDB e RabbitMQ rodando localmente
2. Configure as variáveis de ambiente no arquivo `.env.local`
3. Execute a aplicação:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Qualidade de Código

O projeto utiliza as seguintes ferramentas para garantir a qualidade do código:

- **Black** - Formatação de código
- **Flake8** - Linting
- **Pylint** - Análise estática
- **Pytest** - Testes unitários e de integração
- **Coverage** - Cobertura de código

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto é privado e proprietário.
