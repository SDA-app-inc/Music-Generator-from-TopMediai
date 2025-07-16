# Music-Generator-from-TopMediai
### Для локального запуска  
1.Создаем на корне проекта .env
```dotenv
POSTGRES_USER=postgres
POSTGRES_PASS=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_NAME=postgres


PROXY_IP=
PROXY_PORT=
PROXY_USER=
PROXY_PASS=
TOPMEDIAI_TOKEN=
TOP_MEDIA_API_KEY=
EMAIL_TOP_MEDIA=
TOP_MEDIA_PASSWORD=


DATABASE_URL=postgres+asyncpg://postgres:postgres@db:5432/postgres
```
python app/manage.py 

Миграции alembic применяются автоматически при запуске
приложения 



