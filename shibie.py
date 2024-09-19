
from detect import run

classes = ['书籍纸张', '金属厨具', '砧板', '污损塑料', '筷子',
           '陶瓷器皿', '插头电线', '洗护用品', '塑料玩具', '鞋',
           '果皮果肉', '玻璃器皿', '毛绒玩具', '污损用纸', '塑料器皿',
           '纸盒纸箱', '花盆', '包', '金属器皿', '干电池', '调料瓶',
           '菜帮菜叶', '锅', '食用油桶', '饮料瓶', '充电宝', '易拉罐',
           '牙签', '剩饭剩菜', '大骨头', '鱼骨', '垃圾桶', '酒瓶',
           '金属食品罐', '一次性快餐盒', '烟蒂', '旧衣服', '塑料衣架',
           '枕头', '过期药物', '茶叶渣', '软膏', '蛋壳', '快递纸袋']

classes_4 = {'可回收': ['书籍纸张', '金属厨具', '易拉罐', '饮料瓶', '食用油桶',
                        '快递纸袋', '金属食品罐', '酒瓶', '调料瓶', '包', '塑料衣架',
                        '旧衣服', '锅', '金属器皿', '纸盒纸箱', '毛绒玩具', '玻璃器皿',
                        '塑料器皿', '插头电线', '塑料玩具', '鞋', '垃圾桶', '枕头'],
             '不可回收': ['污损塑料', '一次性快餐盒', '花盆', '牙签', '污损用纸', '筷子',
                          '陶瓷器皿', '洗护用品', '软膏'],
             '有害垃圾': ['烟蒂', '过期药物', '干电池', '充电宝'],
             '厨余垃圾': ['大骨头', '鱼骨', '蛋壳', '菜帮菜叶', '剩饭剩菜', '茶叶渣', '果皮果肉', '砧板']}

def get_detection(image_path):
    shibie_path,cls,cls_num = run(weights="static/weight/best.pt",
                source='static/image/up/'+image_path,
                imgsz=(640, 640),
                project='static/image/out',
                name=image_path.split('.')[0]
                )

    # 根据索引获取对应的类别名
    cls_names = [classes[i] for i in cls]

    # 根据类别名获取对应的类别
    cls_4 = []
    for cls_name in cls_names:
        for key, value in classes_4.items():
            if cls_name in value:
                cls_4.append(key)
                break

    # 计算四个类别的数量
    cls_4_counts = {}
    for category in cls_4:
        cls_4_counts[category] = sum(cls_num[i] for i, c in enumerate(cls_4) if c == category)

    return '/'+str(shibie_path)+'/'+image_path, cls_names, cls_num, cls_4, cls_4_counts

# get_detection('test/1.jpg')