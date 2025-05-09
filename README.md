### Запуск
```
export PYTHONPATH=$(pwd)
poetry run python app/run.py
```

### Запуск тестов
```
poetry run pytest
```

### Линтеры 
```
poetry run black ./
poetry run flake8
poetry run mypy --ignore-missing-import --explicit-package-bases --check-untyped-defs ./
```


### Миграции ДБ
```
poetry run alembic revision --autogenerate -m "Initial"
poetry run alembic revision --autogenerate -m "Описание изменений"
poetry run alembic upgrade head
```

   


### Запуск с докером
```bash
# (С докером)
docker-compose build
docker-compose up -d

docker compose -f docker/local/docker-compose.yml up -d backend

```