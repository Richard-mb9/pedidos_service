#!/bin/bash

cleanup() {
  echo "Encerrando containers..."
  sudo docker-compose -f docker-compose-test.yml down
}
trap cleanup EXIT

echo "Iniciando containers..."
if ! sudo docker-compose -f docker-compose-test.yml up -d; then
  echo "Falha ao iniciar docker-compose. Verificando logs..."
  sudo docker-compose logs
  exit 1
fi

echo "Aguardando serviços..."
sleep 5

if ! sudo docker-compose -f docker-compose-test.yml ps | grep -q "Up"; then
  echo "Containers não estão rodando corretamente"
  sudo docker-compose -f docker-compose-test.yml logs
  exit 1
fi

echo "Executando testes..."
pytest --cov=./src --cov-report=html -W ignore::DeprecationWarning

TEST_EXIT_CODE=$?
sudo docker-compose -f docker-compose-test.yml down

echo ""
echo "=========================================="
if [ $TEST_EXIT_CODE -eq 0 ]; then
  echo "Testes finalizados com sucesso!"
else
  echo "Testes finalizaram com falhas"
fi
echo "Relatório de cobertura: $(pwd)/htmlcov/index.html"

exit $TEST_EXIT_CODE