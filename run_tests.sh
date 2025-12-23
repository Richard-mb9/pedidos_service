#!/bin/bash

cleanup() {
  echo "Encerrando containers..."
  sudo docker-compose down
}
trap cleanup EXIT

echo "Iniciando containers..."
if ! sudo docker-compose up -d; then
  echo "Falha ao iniciar docker-compose. Verificando logs..."
  sudo docker-compose logs
  exit 1
fi

echo "Aguardando serviços..."
sleep 5

# Verifica se os containers estão de pé
if ! sudo docker-compose ps | grep -q "Up"; then
  echo "Containers não estão rodando corretamente"
  sudo docker-compose logs
  exit 1
fi

echo "Executando testes..."
pytest --cov=./src --cov-report=html -W ignore::DeprecationWarning

TEST_EXIT_CODE=$?
sudo docker-compose down

echo ""
echo "=========================================="
if [ $TEST_EXIT_CODE -eq 0 ]; then
  echo "Testes finalizados com sucesso!"
else
  echo "Testes finalizaram com falhas"
fi
echo "Relatório de cobertura: $(pwd)/htmlcov/index.html"

exit $TEST_EXIT_CODE