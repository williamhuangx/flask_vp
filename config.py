import os
from dotenv import load_dotenv

_ = load_dotenv('.env.local')

class Config:
    SECRET_KEY: str = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Vercel PostgreSQL (Neon) 配置
    PG_HOST: str = os.environ.get('PGHOST', 'ep-patient-lab-a1isve8g-pooler.ap-southeast-1.aws.neon.tech')
    PG_DATABASE: str = os.environ.get('PGDATABASE', 'neondb')
    PG_USER: str = os.environ.get('PGUSER', 'neondb_owner')
    PG_PASSWORD: str = os.environ.get('PGPASSWORD', 'npg_BTxJi97ZEYRr')
    PG_PORT: str = os.environ.get('PGPORT', '5432')
    PG_SSLMODE: str = os.environ.get('PGSSLMODE', 'require')

    # 构建数据库连接 URI（使用 pgbouncer 池化连接）
    DB_URI: str = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}?sslmode={PG_SSLMODE}"
