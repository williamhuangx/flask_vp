import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # PostgreSQL 配置
    # 使用 Neon PostgreSQL 连接
    DB_URI = "postgresql://neondb_owner:npg_BTxJi97ZEYRr@ep-patient-lab-a1isve8g-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
