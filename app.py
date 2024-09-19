from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 实例初始化环境信息文件
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'  设置签名所需的钥匙
login_manager = LoginManager(app)  # 实例化扩展类

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qwe123@192.168.3.25/laji'

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
# 热更新HTML模板文件

db = SQLAlchemy(app)
# 在扩展类实例化前加载配置
login_manager.login_view = 'login'  # 定义错误提示信息


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户ID作为参数
    from model import User
    user = User.query.get(int(user_id))  # 用ID作为user模型的主键查询对应的用户
    return user  # 返回用户对象



import views, errors, forms

if __name__ == '__main__':
    app.run(debug=True)
