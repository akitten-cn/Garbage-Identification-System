import os
import random

from app import app, db
from model import *
from flask import request, url_for, redirect, flash, render_template, jsonify
from flask_security import SQLAlchemyUserDatastore, Security, current_user, login_required
from flask_security.utils import login_user, logout_user
import forms
import datetime, time
from shibie import get_detection

# 后端处理文件
# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

security = Security(app, user_datastore)


# db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


"""
 负责的功能
 注册--logging
 登录--login
 登出--logout
 权限管理--'User','Admin','Root'
 用户权限管理 -- user_role (Admin/Root)    -- 修改/change_role (提升为管理员，降为普通用户)（Root）
"""


def gettime():
    current_time = datetime.datetime.now()
    now_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return now_time


@app.route('/user/login', methods=['GET', 'POST'])
def login():  # 登录
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('请输入')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('账号错误')
            return redirect(url_for('login'))
        print(password)
        if password != user.password:
            flash('密码错误')
            return redirect(url_for('login'))
        if user.blacklist == 1:
            flash('存在不文明行为，被管理员拉黑')
            return redirect(url_for('index'))
        flash('登录成功')
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logging', methods=['GET', 'POST'])
def logging():  # 注册
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print(password1)
        if password1 != password2:
            flash('两次输入的密码不同')
            return redirect(url_for('logging'))
        user = User.query.filter_by(username=username).first()
        if user is not None:
            flash('用户已注册')
            return redirect(url_for('login'))
        new_user = user_datastore.create_user(username=username, password=password1)
        normal_role = user_datastore.find_role('User')
        db.session.add(new_user)
        user_datastore.add_role_to_user(new_user, normal_role)
        db.session.commit()
        flash('注册成功')
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('logging.html')


@app.route('/logout')
def logout():  # 登出
    logout_user()
    flash('登出')
    return redirect(url_for('index'))


"""    

# 权限管理
 - 权限
   - 用户 回收员 超级管理员 

# 不文明管理
 - 超级管理员
   - 拉黑

# 首页

# 垃圾识别
 - 上传图片识别
  - 返回识别结果显示详细信息
  
# 垃圾投放
 - 上传图片识别
   - 返回识别后结果，并自动记录积分和不文明行为
     - 不文明行为：垃圾混投放
       - 垃圾：
         - 用户名
         - 社区
         - 可回收数量
         - 不可回收数量
         - 有害数量
         - 厨余垃圾数量

# 积分商城
 - 商城列表
   - 用户
     - 兑换商品-减少积分
   - 回收员、管理员
     - 上传商品
       - 商品：
         - 商品名称
         - 商品数量
         - 商品积分
     - 修改商品
     - 删除商品

# 垃圾科普
 - 科普列表
   - 用户
     - 详情
   - 回收员、管理员
     - 添加科普
       - 科普：
         - 用户名
         - 大类
         - 垃圾名称
         - 垃圾介绍
     - 删除
     - 修改

# 旧物回收
 - 旧物列表
   - 用户
     - 添加
     - 修改
     - 删除
       - 旧物：
         - 用户名
         - 旧物名称
         - 旧物类别
         - 旧物照片
         - 取件码
         - 是否已回收
   - 回收员、管理员
     - 回收
       - 弹框输入取件码

# 社区
 - 社区列表
   - 社区名
   - 可回收剩余数量
   - 不可回收剩余数量
   - 有害剩余数量
   - 厨余剩余数量
     - 回收员、管理员
       - 添加
       - 修改
       - 删除
       - 回收
         - 社区：
           - 社区名
           - 可回收剩余数量
           - 不可回收剩余数量
           - 有害剩余数量
           - 厨余剩余数量
"""


def generate_random_number():
    # 生成随机的六位数
    random_number = random.randint(100000, 999999)
    return random_number


@app.route('/user_role', methods=['GET', 'POST'])
@login_required
def user_role():
    if current_user.has_role('Root'):
        users = User.query.all()
        # print(users)
        return render_template('user_role.html', users=users)
    else:
        flash('请以超级管理员账户登录')
        return redirect(url_for('index'))


@app.route('/promote_role/<string:username>')
@login_required
def promote_role(username):  # 升为管理员
    user = User.query.filter_by(username=username).first()
    adminrole = user_datastore.find_role('Admin')
    userrole = user_datastore.find_role('User')
    user_datastore.remove_role_from_user(user, userrole)
    user_datastore.add_role_to_user(user, adminrole)
    db.session.commit()
    return redirect(url_for('user_role'))


@app.route('/reduce_role/<string:username>')
@login_required
def reduce_role(username):  # 降为普通用户
    user = User.query.filter_by(username=username).first()
    adminrole = user_datastore.find_role('Admin')
    userrole = user_datastore.find_role('User')
    user_datastore.remove_role_from_user(user, adminrole)
    user_datastore.add_role_to_user(user, userrole)
    db.session.commit()
    return redirect(url_for('user_role'))


@app.route('/blacklist', methods=['GET', 'POST'])
@login_required
def blacklist():
    if current_user.has_role('Root'):
        users = User.query.all()
        # print(users)
        return render_template('blacklist.html', users=users)
    else:
        flash('请以超级管理员账户登录')
        return redirect(url_for('index'))


@app.route('/blacklist_user/<int:id>')
@login_required
def blacklist_user(id):  # 拉黑
    user = User.query.filter_by(id=id).first()
    user.blacklist = 1
    db.session.commit()
    return redirect(url_for('blacklist'))


@app.route('/recover_user/<int:id>')
@login_required
def recover_user(id):  # 降为普通用户
    user = User.query.filter_by(id=id).first()
    user.blacklist = 0
    db.session.commit()
    return redirect(url_for('blacklist'))


@app.route('/Trash_detect', methods=['GET', 'POST'])
@login_required
def Trash_detect():
    return render_template('Trash_detect.html')


@app.route("/imageDetect", methods=["POST"])
@login_required
def imgDetect():
    image = request.files["file"]

    # 2、选择保存图片的路径
    basepath = "/static/image/up/"
    path = os.path.dirname(__file__)
    suffix = image.filename.split(".")[1]  # 获取.jpg
    # 获取当前时间
    current_time = datetime.datetime.now()
    name = current_time.strftime("%Y-%m-%d-%H-%M")
    o_img_path = basepath + name + "." + suffix  # 这是/static/images/xxx.jpg
    # 这个可以传参给前端拿到相对路径然后展示图片

    image.save(path + o_img_path)  # 这是绝对路径，因为.save()貌似只能保存绝对路径，但保存的地址也是项目下的/static/images/xxx.jpg
    print(path + o_img_path)
    yuantu_path = name + "." + suffix
    shibie_path, cls_names, cls_num, cls_4, cls_4_counts = get_detection(yuantu_path)
    cls_names = str(cls_names)
    cls_num = str(cls_num)
    cls_4 = str(cls_4)
    cls_4_counts = str(cls_4_counts)
    linshi = Linshi(username=current_user.username, image_path=shibie_path, cls=cls_names, cls_number=cls_num,
                    cls_4=cls_4, cls_4_counts=cls_4_counts)
    db.session.add(linshi)
    db.session.commit()
    return str(linshi.id)


@app.route('/detect_result/<int:id>', methods=['GET'])
@login_required
def detect_result(id):
    linshi = Linshi.query.filter_by(id=id).first()
    image_path = linshi.image_path
    cls = eval(linshi.cls)
    cls_num = eval(linshi.cls_number)
    cls_4 = eval(linshi.cls_4)
    cls_4_counts = eval(linshi.cls_4_counts)
    return render_template('detect_result.html', linshi=linshi,
                           image_path=image_path, cls=cls, cls_num=cls_num, cls_4=cls_4,
                           cls_4_counts=cls_4_counts)


@app.route('/Trash_disposal/<int:page>', methods=['GET', 'POST'])
@login_required
def Trash_disposal(page=None):
    if not page:
        page = 1
    print(page,"asdfasdf")
    if current_user.has_role('Admin') or current_user.has_role('Root'):

        paginate = Trash.query.order_by(Trash.time.desc()).paginate(page=page, per_page=10, error_out=False)
        trashs = paginate.items
        return render_template('Trash_disposal.html', trashs=trashs, paginate=paginate)
    elif current_user.has_role('User'):

        paginate = Trash.query.filter_by(username=current_user.username).order_by(Trash.time.desc()).paginate(page=page,
                                                                                                              per_page=10,
                                                                                                              error_out=False)
        trashs = paginate.items
        return render_template('Trash_disposal.html', trashs=trashs, paginate=paginate)


@app.route('/disposal_trash', methods=['GET', 'POST'])
@login_required
def disposal_trash():
    return render_template('disposal_trash.html')


@app.route('/disposal/<int:id>', methods=['GET', 'POST'])
@login_required
def disposal(id):
    linshi = Linshi.query.filter_by(id=id).first()
    image_path = linshi.image_path
    cls = eval(linshi.cls)
    cls_num = eval(linshi.cls_number)
    cls_4 = eval(linshi.cls_4)
    cls_4_counts = eval(linshi.cls_4_counts)
    communities = Community.query.filter_by().all()
    if request.method == 'POST':
        community_id = request.form.get('community')
        community = Community.query.filter_by(id=community_id).first()
        user = User.query.filter_by(id=current_user.id).first()
        for key, value in cls_4_counts.items():
            if key == '不可回收':
                community.non_recyclable_trash -= int(value)
            elif key == '可回收':
                community.recyclable_trash -= int(value)
                user.integral += int(value)
            elif key == '厨余垃圾':
                community.kitchen_trash -= int(value)
            elif key == '有害垃圾':
                community.hazardous_trash -= int(value)

        if len(cls_4_counts) > 1:
            user.uncivilized += 1
        trash = Trash(username=current_user.username, community=community.community,
                      recyclable_trash=cls_4_counts.get('可回收', 0),
                      non_recyclable_trash=cls_4_counts.get('不可回收', 0),
                      kitchen_trash=cls_4_counts.get('厨余垃圾', 0),
                      hazardous_trash=cls_4_counts.get('有害垃圾', 0), time=gettime())
        db.session.add(trash)
        db.session.commit()
        return redirect(url_for('Trash_disposal'))
    return render_template('disposal.html', linshi=linshi,
                           image_path=image_path, cls=cls, cls_num=cls_num, cls_4=cls_4,
                           cls_4_counts=cls_4_counts, communities=communities)


@app.route('/community', methods=['GET', 'POST'])
@login_required
def community():
    communities = Community.query.all()
    if current_user.has_role('Admin') or current_user.has_role('Root'):
        for community in communities:
            if community.recyclable_trash <= 10 or community.non_recyclable_trash <= 10 or community.hazardous_trash <= 10 or community.kitchen_trash <= 10:
                flash(community.community + '需要回收')
    return render_template('community.html', communities=communities)


@app.route('/community_add', methods=['GET', 'POST'])
@login_required
def community_add():
    if request.method == 'POST':
        community_name = request.form.get('community')
        recyclable_trash = request.form.get('recyclable_trash')
        non_recyclable_trash = request.form.get('non_recyclable_trash')
        hazardous_trash = request.form.get('hazardous_trash')
        kitchen_trash = request.form.get('kitchen_trash')

        community = Community(community=community_name, recyclable_trash=recyclable_trash,
                              non_recyclable_trash=non_recyclable_trash,
                              hazardous_trash=hazardous_trash, kitchen_trash=kitchen_trash,
                              recyclable_trash_original=recyclable_trash,
                              non_recyclable_trash_original=non_recyclable_trash,
                              hazardous_trash_original=hazardous_trash,
                              kitchen_trash_original=kitchen_trash)
        db.session.add(community)
        db.session.commit()
        flash('添加成功')
        return redirect(url_for('community'))
    return render_template('community_add.html')


@app.route('/community_change/<int:id>', methods=['GET', 'POST'])
@login_required
def community_change(id):
    community = Community.query.filter_by(id=id).first()
    if request.method == 'POST':
        recyclable_trash_original = request.form.get('recyclable_trash')
        non_recyclable_trash_original = request.form.get('non_recyclable_trash')
        hazardous_trash_original = request.form.get('hazardous_trash')
        kitchen_trash_original = request.form.get('kitchen_trash')
        community.recyclable_trash = int(recyclable_trash_original) - (
                int(community.recyclable_trash_original) - community.recyclable_trash)
        community.recyclable_trash_original = recyclable_trash_original
        community.non_recyclable_trash = int(non_recyclable_trash_original) - (
                int(community.non_recyclable_trash_original) - community.non_recyclable_trash)
        community.non_recyclable_trash_original = non_recyclable_trash_original
        community.hazardous_trash = int(hazardous_trash_original) - (
                int(community.hazardous_trash_original) - community.hazardous_trash)
        community.hazardous_trash_original = hazardous_trash_original
        community.kitchen_trash = int(kitchen_trash_original) - (
                int(community.kitchen_trash_original) - community.kitchen_trash)
        community.kitchen_trash_original = kitchen_trash_original
        db.session.commit()
        flash('修改成功')
        return redirect(url_for('community'))
    return render_template('community_change.html', community=community)


@app.route('/community_recover/<int:id>', methods=['POST'])
@login_required
def community_recover(id):
    community = Community.query.filter_by(id=id).first()
    community.recyclable_trash = community.recyclable_trash_original

    community.non_recyclable_trash = community.non_recyclable_trash_original

    community.hazardous_trash = community.hazardous_trash_original

    community.kitchen_trash = community.kitchen_trash_original

    db.session.commit()
    flash('回收成功')
    return redirect(url_for('community'))


@app.route('/commodity', methods=['GET', 'POST'])
@login_required
def commodity():
    commodities = Commodity.query.all()

    return render_template('commodity.html', commodities=commodities)


@app.route('/commodity_duihuan', methods=['POST'])
@login_required
def commodity_duihuan():
    data = request.json
    quantity = data.get('quantity')
    id = data.get('id')
    commodity = Commodity.query.filter_by(id=id).first()
    commodity.number = commodity.number - int(quantity)
    user = User.query.filter_by(id=current_user.id).first()
    user.integral = user.integral - int(quantity) * commodity.integral
    db.session.commit()

    return jsonify(
        {'message': '兑换成功', 'new_commodity_number': commodity.number, 'user_integral': user.integral}), 200


@app.route('/commodity_add', methods=['GET', 'POST'])
@login_required
def commodity_add():
    if request.method == 'POST':
        commodity_name = request.form.get('commodity')
        number = request.form.get('number')
        integral = request.form.get('integral')

        commodity = Commodity(commodity=commodity_name, number=number, integral=integral)
        db.session.add(commodity)
        db.session.commit()
        flash('添加成功')
        return redirect(url_for('commodity'))
    return render_template('commodity_add.html')


@app.route('/commodity_change/<int:id>', methods=['GET', 'POST'])
@login_required
def commodity_change(id):
    commodity = Commodity.query.filter_by(id=id).first()
    if request.method == 'POST':
        number = request.form.get('number')
        integral = request.form.get('integral')
        commodity.number = number
        commodity.integral = integral

        db.session.commit()
        flash('修改成功')
        return redirect(url_for('commodity'))
    return render_template('commodity_change.html', commodity=commodity)


@app.route('/commodity_del/<int:id>', methods=['POST'])
@login_required  # 登录保护
def commodity_del(id):
    commodity = Commodity.query.filter_by(id=id).first()
    db.session.delete(commodity)
    db.session.commit()

    flash('删除成功')
    return redirect(url_for('commodity'))


@app.route('/popular_science', methods=['GET', 'POST'])
@login_required
def popular_science():
    popular_sciences = Popular_science.query.filter_by().all()
    return render_template('popular_science.html', popular_sciences=popular_sciences)


@app.route('/popular_science_instance/<int:id>')
@login_required
def popular_science_instance(id):
    popular_science = Popular_science.query.filter_by(id=id).first()
    return render_template('popular_science_instance.html', popular_science=popular_science)


@app.route('/popular_science_change/<int:id>', methods=['GET', 'POST'])
@login_required
def popular_science_change(id):
    popular_science = Popular_science.query.filter_by(id=id).first()
    if request.method == 'POST':
        popular_science.name = request.form.get("name")
        popular_science.classification = request.form.get("classification")
        popular_science.introduction = request.form.get("introduction")
        db.session.commit()
        # flash('更新成功')
        return redirect(url_for('popular_science'))
    return render_template('popular_science_change.html', popular_science=popular_science)


@app.route("/popular_science_add", methods=["GET", "POST"])
@login_required
def popular_science_add():
    if request.method == 'POST':
        name = request.form.get("name")
        classification = request.form.get("classification")
        introduction = request.form.get("introduction")
        popular_science = Popular_science(username=current_user.username, name=name, classification=classification,
                                          introduction=introduction)
        db.session.add(popular_science)
        db.session.commit()
        return redirect(url_for('popular_science'))
    return render_template('popular_science_add.html')


@app.route('/popular_science_del/<int:id>', methods=['POST'])
@login_required  # 登录保护
def popular_science_del(id):
    popular_science = Popular_science.query.filter_by(id=id).first()
    db.session.delete(popular_science)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('popular_science'))


@app.route('/recycling', methods=['GET', 'POST'])
@login_required
def recycling():
    if current_user.has_role('Admin') or current_user.has_role('Root'):
        recyclings = Recycling.query.filter_by().all()
        return render_template('recycling.html', recyclings=recyclings)
    elif current_user.has_role('User'):
        recyclings = Recycling.query.filter_by(username=current_user.username).all()
        return render_template('recycling.html', recyclings=recyclings)


@app.route('/recycling_huishou', methods=['POST'])
@login_required
def recycling_huishou():
    data = request.json
    quantity = data.get('quantity')
    id = data.get('id')
    recycling = Recycling.query.filter_by(id=id).first()
    if int(quantity) == int(recycling.pickup_code):
        recycling.recycling = 1
        db.session.commit()
        return jsonify({'message': '回收成功'}), 200
    else:
        return jsonify({'message': '回收验证码错误'}), 400


@app.route('/recycling_instance/<int:id>')
@login_required
def recycling_instance(id):
    recycling = Recycling.query.filter_by(id=id).first()
    return render_template('recycling_instance.html', recycling=recycling)


@app.route("/recycling_add", methods=["GET", "POST"])
@login_required
def recycling_add():
    if request.method == 'POST':
        image = request.files.get('file')
        name = request.form.get("name")
        classification = request.form.get("classification")

        # 2、选择保存图片的路径
        basepath = "/static/image/recycling/"
        path = os.path.dirname(__file__)
        suffix = image.filename.split(".")[1]  # 获取.jpg
        # 获取当前时间
        current_time = datetime.datetime.now()
        name_path = current_time.strftime("%Y-%m-%d-%H-%M")
        o_img_path = basepath + name_path + "." + suffix  # 这是/static/images/xxx.jpg
        # 这个可以传参给前端拿到相对路径然后展示图片

        image.save(path + o_img_path)  # 这是绝对路径，因为.save()貌似只能保存绝对路径，但保存的地址也是项目下的/static/images/xxx.jpg
        print(path + o_img_path)
        image_path = name_path + "." + suffix
        pickup_code = generate_random_number()
        recycling = Recycling(username=current_user.username, name=name, image_path=image_path,
                              classification=classification, pickup_code=pickup_code)
        db.session.add(recycling)
        db.session.commit()
        return redirect(url_for('recycling'))
    return render_template('recycling_add.html')


@app.route('/recycling_del/<int:id>', methods=['POST'])
@login_required  # 登录保护
def recycling_del(id):
    recycling = Recycling.query.filter_by(id=id).first()
    db.session.delete(recycling)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('recycling'))
