import os
from dotenv import load_dotenv

# 加载 env.local 文件中的环境变量
load_dotenv('env.local')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # PostgreSQL 配置
    # 从环境变量 DATABASE_URL 读取，使用 env.local 中的配置
    DB_URI = os.environ.get('DATABASE_URL')
    
    # 如果没有设置 DATABASE_URL，则使用默认值
    if not DB_URI:
        PGHOST = os.environ.get('PGHOST', 'ep-curly-cloud-a1z3ive4-pooler.ap-southeast-1.aws.neon.tech')
        PGUSER = os.environ.get('PGUSER', 'neondb_owner')
        PGPASSWORD = os.environ.get('PGPASSWORD', 'npg_0lkJQcK6pVUv')
        PGDATABASE = os.environ.get('PGDATABASE', 'neondb')
        DB_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}?sslmode=require"
