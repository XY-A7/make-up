import os  # 确保已导入
import ssl
from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

# 使用绝对路径定义文件位置
USER_DATA_FILE = os.path.join(os.path.dirname(__file__), "userdata.csv")

# 调试输出文件路径（步骤1的代码）
print(f"用户数据文件绝对路径：{os.path.abspath(USER_DATA_FILE)}")  # 确保这里不再报错

# 检查用户是否存在
def user_exists(username):
    try:
        with open(USER_DATA_FILE, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if row and row[0] == username:
                    return True
    except FileNotFoundError:
        pass
    return False

# 获取用户密码
def add_user(username, password):
    try:
        with open(USER_DATA_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([username, password])
            print(f"已写入用户：{username}")  # 调试信息
    except Exception as e:
        print(f"写入用户数据失败：{str(e)}")  # 关键错误日志
        raise  # 抛出异常让上层捕获


# 检查文件是否存在，如果不存在则创建并写入标题行
def initialize_user_file():
    try:
        with open(USER_DATA_FILE, 'r', newline='', encoding='utf-8') as csvfile:
            print("用户文件已存在")
    except FileNotFoundError:
        print("正在创建新用户文件...")
        with open(USER_DATA_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['username', 'password'])
            print("用户文件创建成功")
# 获取用户密码（新增函数）
def get_user_password(username):
    try:
        with open(USER_DATA_FILE, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                # 跳过标题行（如果存在）
                if row and row[0] == 'username' and row[1] == 'password':
                    continue
                if row and row[0] == username:
                    return row[1]  # 返回第二列的密码
            return None  # 如果遍历完所有行都没找到
    except FileNotFoundError:
        print(f"错误：用户数据文件 {USER_DATA_FILE} 不存在")
        return None
    except Exception as e:
        print(f"读取用户密码时发生异常：{str(e)}")
        return None
    
@app.route("/login")
def index_login():
    return render_template("login.html")

@app.route("/register")
def index_register():
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("username")
    pwd = request.form.get("password")
    
    if not user_exists(name):
        return "用户不存在"  # 返回纯文本错误信息
    
    stored_password = get_user_password(name)
    if pwd == stored_password:
        # 跳转到商品界面
        return redirect(url_for('shopping'))
    else:
        return "密码错误"  # 返回纯文本错误信息

@app.route("/register", methods=["POST"])
def register():
    try:
        name = request.form.get("username")
        pwd = request.form.get("password")
        
        if not name or not pwd:
            return "用户名和密码不能为空", 400
        
        if user_exists(name):
            return "用户已存在", 409
        
        add_user(name, pwd)
        print(f"新用户注册成功：{name}")  # 调试信息
        return '注册成功 <a href="/login">前往登录</a>'
        
    except Exception as e:
        print(f"注册时发生异常：{str(e)}")  # 关键错误日志
        return "注册遇到问题，请稍后重试", 500

@app.route("/shopping")
def shopping():
    return render_template("疏影_商品界面.html")

if __name__ == "__main__":
    initialize_user_file()
    app.run(debug=True)


