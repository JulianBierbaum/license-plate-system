cd services/analytics-service

uv sync
docker build -t julianbierbaum/license-plate-system:analytics-service .
docker push julianbierbaum/license-plate-system:analytics-service

cd ..

cd auth-service

uv sync
docker build -t julianbierbaum/license-plate-system:auth-service .
docker push julianbierbaum/license-plate-system:auth-service

cd ..

cd data-collection-service

uv sync
docker build -t julianbierbaum/license-plate-system:data-collection-service .
docker push julianbierbaum/license-plate-system:data-collection-service

cd ..

cd notification-service

docker build -t julianbierbaum/license-plate-system:notification-service .
uv sync
docker push julianbierbaum/license-plate-system:notification-service

cd ..

cd web-service

npm install
docker build -t julianbierbaum/license-plate-system:web-service .
docker push julianbierbaum/license-plate-system:web-service

cd ..