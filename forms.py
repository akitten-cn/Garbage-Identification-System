from flask_wtf import FlaskForm  # FlaskForm 为表单基类
from wtforms import StringField, PasswordField, SubmitField  # 导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired, ValidationError


class LoginForm(FlaskForm):
    account = StringField(
        # 标签
        label="账号",
        # 验证器
        validators=[
            DataRequired('请输入用户名')
        ],
        description="账号",
        # 附加选项,会自动在前端判别
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号!",
            "required": 'required'  # 表示输入框不能为空，并有提示信息
        }
    )

    pwd = PasswordField(
        # 标签
        label="密码",
        # 验证器
        validators=[
            DataRequired('请输入密码')
        ],
        description="密码",

        # 附加选项(主要是前端样式),会自动在前端判别
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码!",
            "required": 'required'  # 表示输入框不能为空
        }
    )

    submit = SubmitField(
        label="登录",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )
