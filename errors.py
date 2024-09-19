from app import app
from flask import render_template

# 错误状态处理文件
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html'), 404  # 返回模板和状态码


@app.errorhandler(400)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('400.html'), 400  # 返回模板和状态码


@app.errorhandler(500)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('500.html'), 500  # 返回模板和状态码
