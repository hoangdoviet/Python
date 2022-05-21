## Requirements
- Python 3.8
- PostgresSQL 13
- Redis 


## Install
Install Poetry - Tool for dependency management and packaging in Python

```
poetry install
poetry shell
```

```
alembic stamp head
alembic revision --autogenerate -m "update db" 
alembic upgrade head

```

