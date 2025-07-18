cd services/analytics-service

docker build -t julianbierbaum/license-plate-system:analytics-service .

wait 1

docker push julianbierbaum/license-plate-system:analytics-service

cd ..

cd auth-service

docker build -t julianbierbaum/license-plate-system:auth-service .

wait 1

docker push julianbierbaum/license-plate-system:auth-service

cd ..

cd data-collection-service

docker build -t julianbierbaum/license-plate-system:data-collection-service .

wait 1

docker push julianbierbaum/license-plate-system:data-collection-service

cd ..

cd notification-service

docker build -t julianbierbaum/license-plate-system:notification-service .

wait 1

docker push julianbierbaum/license-plate-system:notification-service

cd ..

cd web-service

docker build -t julianbierbaum/license-plate-system:web-service .

wait 1

docker push julianbierbaum/license-plate-system:web-service

cd ..