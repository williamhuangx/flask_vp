from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv('env.local')

app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义消息模型
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# 尝试创建数据库表
with app.app_context():
    try:
        db.create_all()
        print("数据库表创建成功")
    except Exception as e:
        print(f"数据库连接失败: {e}")
        print("应用将继续运行，但数据库功能可能不可用")

@app.route('/')
def index():
    # 从数据库获取最新的联系消息
    try:
        latest_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
        print(f"成功获取 {len(latest_messages)} 条最新消息")
    except Exception as e:
        print(f"获取消息失败: {e}")
        latest_messages = []
    
    return render_template('index.html', latest_messages=latest_messages)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # 处理表单提交
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # 尝试存储到数据库
        try:
            new_message = ContactMessage(name=name, email=email, message=message)
            db.session.add(new_message)
            db.session.commit()
            print(f"消息已存储: {name}, {email}")
        except Exception as e:
            print(f"数据库存储失败: {e}")
        
        return render_template('contact.html', success=True)
    return render_template('contact.html')

@app.route('/admin')
def admin():
    # 从数据库获取所有联系消息
    try:
        all_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
        print(f"成功获取 {len(all_messages)} 条消息")
    except Exception as e:
        print(f"获取消息失败: {e}")
        all_messages = []
    
    return render_template('admin.html', messages=all_messages)

@app.route('/delete/<int:message_id>')
def delete_message(message_id):
    # 删除指定ID的消息
    try:
        message = ContactMessage.query.get(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
            print(f"成功删除消息 ID: {message_id}")
    except Exception as e:
        print(f"删除消息失败: {e}")
    
    return redirect(url_for('admin'))

@app.route('/edit/<int:message_id>', methods=['GET', 'POST'])
def edit_message(message_id):
    # 编辑指定ID的消息
    try:
        message = ContactMessage.query.get(message_id)
        if not message:
            return redirect(url_for('admin'))
        
        if request.method == 'POST':
            # 更新消息内容
            message.name = request.form.get('name')
            message.email = request.form.get('email')
            message.message = request.form.get('message')
            db.session.commit()
            print(f"成功更新消息 ID: {message_id}")
            return redirect(url_for('admin'))
    except Exception as e:
        print(f"编辑消息失败: {e}")
        return redirect(url_for('admin'))
    
    return render_template('edit.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
