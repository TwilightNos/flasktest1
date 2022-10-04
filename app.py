# pip install flask_sqlalchemy
# pip install flask-mysqldb

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
# 设置密钥以使用flash传送信息
app.secret_key = 'cloudcomputing'

# 在环境变量中设置本地数据库
usr = os.environ.get('DBUSER')
pw = os.environ.get('DBPW')
n = os.environ.get('DBNAME')

# 连接数据库
# 设置数据库连接地址
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://{}:{}@127.0.0.1:3306/{}'.format(usr,pw,n)
# 跟踪数据库的修改 不建议开启
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 显示数据库处理过程 不建议开启
# app.config['SQLALCHEMY_ECHO'] = True
# 创建数据库
db = SQLAlchemy(app)


# 测试连接，连接成功后删除
sql = 'select * from Users'
result = db.session.execute(sql)
print(result.fetchall())


# 初始界面
@app.route('/')
def index():
    return render_template('index.html')


# 登录界面
@app.route('/login',methods = ['GET','POST'])
def login():
    # 当请求为POST时处理传入信息
    if request.method == 'POST':
        # 从request中获取表单传入的信息
        email = request.form['email']
        password = request.form['password']
        # 报错信息
        error = None
        # 从数据库中获取信息
        sql = "select * from users where email = '" + email +"'"
        result = db.session.execute(sql).fetchone()
        if result:
            username,password_indb = result[0],result[2]
        # 验证传入的信息
        if not email:
            error = 'Email Is Required.'
        elif not password:
            error = 'Password Is Required.'
        elif not result:
            error = 'Invalid Email.'
        elif password_indb != password:
            error = 'Incorrect Password.'
        else:
            return render_template('content.html')
        # 将错误信息发送给html
        flash(error)
    return render_template('login.html')

@app.route('/register',methods = ['GET','POST'])
def register():
    # 当请求为POST时处理传入信息
    if request.method == 'POST':
        # 获取表单信息
        info = []
        for i in request.form.values():
            info.append(i)
        email,username,password,confirm_password = info
        error = None
        # 去数据库中搜索有无重复项
        sql = "select * from users where email = '" + email + "'"
        result = db.session.execute(sql).fetchone()

        # 校验输入信息
        if not email:
            error = 'Email Is Required.'
        elif not username:
            error = 'Username is Required.'
        elif not password or not confirm_password:
            error = 'Password Is Required.'
        elif password != confirm_password:
            error = 'Two Passwords Do Not Match.'
        elif result:
            error = 'Email has already registered.'
        else:
            # 向数据库中插入信息，邮件两侧需要加引号
            sql_reg = f"insert into users values ({username},'"+email+f"',{password})"
            db.session.execute(sql_reg)
            # 如果是修改数据库中信息，那么执行完sql语句后一定要commit
            db.session.commit()
            return render_template('content.html')

        flash(error)
    return render_template('register.html')

if __name__ == '__main__':
    app.run()
