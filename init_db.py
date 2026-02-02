#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建 PostgreSQL 数据库中的表结构
"""

import psycopg2
from config import Config


def create_tables():
    """创建数据库表结构"""
    # 连接到数据库
    conn = None
    try:
        # 解析连接URI
        import re
        match = re.match(r'postgresql://(.*?):(.*?)@(.*?)/(.*)', Config.DB_URI)
        if match:
            user, password, host, database = match.groups()
            # 移除可能的端口号
            if ':' in host:
                host = host.split(':')[0]
        else:
            # 使用默认值
            user = 'neondb_owner'
            password = 'npg_0lkJQcK6pVUv'
            host = 'ep-curly-cloud-a1z3ive4-pooler.ap-southeast-1.aws.neon.tech'
            database = 'neondb'

        # 连接到数据库
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=database,
            sslmode='require'
        )
        conn.autocommit = True
        
        # 创建游标
        with conn.cursor() as cursor:
            # 创建 users 表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    logo_data BYTEA,
                    logo_content_type VARCHAR(100),
                    address TEXT,
                    tel VARCHAR(50),
                    fac VARCHAR(50),
                    is_active BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            print("创建 users 表成功")
            
            # 创建 orders 表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    no VARCHAR(100),
                    nama VARCHAR(255),
                    terima_tgl DATE,
                    telpon VARCHAR(50),
                    selesal_tgl DATE,
                    alamat TEXT,
                    kode VARCHAR(100),
                    bram_karat1 VARCHAR(100),
                    bram_karat2 VARCHAR(100),
                    bram_karat3 VARCHAR(100),
                    bram_karat4 VARCHAR(100),
                    bram_karat5 VARCHAR(100),
                    bram_karat6 VARCHAR(100),
                    bram_karat7 VARCHAR(100),
                    bram_karat8 VARCHAR(100),
                    bram_karat9 VARCHAR(100),
                    bram_karat10 VARCHAR(100),
                    toko VARCHAR(255),
                    spl_qc VARCHAR(255),
                    pesanan_tiba_dikirim_tanggal DATE,
                    order_name VARCHAR(255),
                    order_amount DECIMAL,
                    status VARCHAR(50),
                    description TEXT,
                    image_data BYTEA,
                    image_content_type VARCHAR(100),
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            print("创建 orders 表成功")
            
    except Exception as e:
        print(f"创建表失败: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    print("开始初始化数据库...")
    create_tables()
    print("数据库初始化完成！")
