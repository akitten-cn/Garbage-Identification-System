from app import db, app
from views import user_datastore
from werkzeug.security import generate_password_hash,check_password_hash

# 权限初始化文件
# 初始化超级管理员账号
with app.app_context():
    admin = user_datastore.create_user(username='admin', password='123456')
    # 生成普通用户角色和admin用户角色
    user_role = user_datastore.create_role(name='User', description='Generic user role')
    admin_role = user_datastore.create_role(name='Admin', description='Admin user role')
    Root_role = user_datastore.create_role(name='Root', description='Root user role')
    # 为admin添加Admin角色
    user_datastore.add_role_to_user(admin, Root_role)

# 创建应用程序上下文

    # 提交数据库会话
    db.session.commit()
