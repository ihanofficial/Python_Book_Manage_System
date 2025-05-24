import tkinter as tk # 图形界面库
import tkinter.messagebox as msg #消息框
import sqlite3 as sql # 数据库连接
import hashlib # 哈希加密库
import os



# 定义日志字段
# log_string = 
# type_op out_time user book
op = 1
out_time = 202505232035
userID ="admin"
bookID="23413424"
log_string = "{"+f'"type_op":{op}, "out_time":{out_time}, "user"{userID},"book":{bookID}'+"}"
print(log_string)
# 定义功能函数
def sign_in():
    # 获取登录窗口的用户名和密码输入框
    log_window = None
    username_entry = None
    password_entry = None
    # 查找当前所有Toplevel窗口，找到标题为"登录"的窗口
    for widget in tk._default_root.winfo_children():
        if isinstance(widget, tk.Toplevel) and widget.title() == "登录":
            log_window = widget
            # 获取输入框
            for child in widget.winfo_children():
                if isinstance(child, tk.Frame):
                    entries = child.winfo_children()
                    for entry in entries:
                        if isinstance(entry, tk.Entry):
                            if not username_entry:
                                username_entry = entry
                            else:
                                password_entry = entry
            break

    if not log_window or not username_entry or not password_entry:
        msg.showerror("错误", "无法获取登录窗口控件")
        return

    username = username_entry.get().strip()
    password = password_entry.get()

    if not username or not password:
        msg.showwarning("警告", "请输入用户名和密码")
        return

    # 查询数据库，获取加密密码和盐及用户类型
    database_cursor.execute("SELECT user_passwd_e, salt, user_cate FROM user_info WHERE user_name=?", (username,))
    result = database_cursor.fetchone()
    if not result:
        msg.showerror("登录失败", "用户名不存在")
        return

    password_hash_db, salt, user_type = result
    password_hash_input = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    if password_hash_input != password_hash_db:
        msg.showerror("登录失败", "密码错误")
        return

    msg.showinfo("登录成功", f"欢迎，{username}！")
    log_window.destroy()
    print(user_type)
    print(type(user_type))

    if user_type == "2":
        admin_window()
    else:
        reader_window()



def log_window_launch():
    log_window = tk.Toplevel(root)
    log_window.title("登录")
    log_window.geometry("350x220")
    log_window.configure(bg="#f5f6fa")

    # 标题
    tk.Label(log_window, text="用户登录", font=("微软雅黑", 18, "bold"), bg="#f5f6fa", fg="#273c75").pack(pady=(18, 10))

    # 输入区
    input_frame = tk.Frame(log_window, bg="#f5f6fa")
    input_frame.pack(pady=10, padx=20, fill="x")

    tk.Label(input_frame, text="用户名：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=0, column=0, padx=5, pady=10, sticky="e")
    username_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    username_entry.grid(row=0, column=1, padx=5, pady=10, sticky="we")

    tk.Label(input_frame, text="密码：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=1, column=0, padx=5, pady=10, sticky="e")
    password_entry = tk.Entry(input_frame, show="*", font=("微软雅黑", 12))
    password_entry.grid(row=1, column=1, padx=5, pady=10, sticky="we")

    input_frame.grid_columnconfigure(1, weight=1)

    # 按钮区
    btn_frame = tk.Frame(log_window, bg="#f5f6fa")
    btn_frame.pack(pady=10)
    btn_style = {
        "font": ("微软雅黑", 12),
        "width": 10,
        "bg": "#40739e",
        "fg": "white",
        "activebackground": "#718093",
        "activeforeground": "white",
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2"
    }
    tk.Button(btn_frame, text="登录", command=sign_in, **btn_style).pack(side="left", padx=12)
    tk.Button(btn_frame, text="取消", command=log_window.destroy, **btn_style).pack(side="left", padx=12)

    log_window.protocol("WM_DELETE_WINDOW", log_window.destroy)
    log_window.transient(root)


def reg_window_launch():
    reg_window = tk.Toplevel(root)
    reg_window.title("注册")
    reg_window.geometry("370x320")
    reg_window.configure(bg="#f5f6fa")

    # 标题
    tk.Label(reg_window, text="用户注册", font=("微软雅黑", 18, "bold"), bg="#f5f6fa", fg="#273c75").pack(pady=(18, 10))

    # 输入区
    input_frame = tk.Frame(reg_window, bg="#f5f6fa")
    input_frame.pack(pady=10, padx=20, fill="x")

    tk.Label(input_frame, text="用户名：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=0, column=0, padx=5, pady=8, sticky="e")
    username_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    username_entry.grid(row=0, column=1, padx=5, pady=8, sticky="we", columnspan=2)

    tk.Label(input_frame, text="密码：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=1, column=0, padx=5, pady=8, sticky="e")
    password_entry = tk.Entry(input_frame, show="*", font=("微软雅黑", 12))
    password_entry.grid(row=1, column=1, padx=5, pady=8, sticky="we", columnspan=2)

    tk.Label(input_frame, text="确认密码：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=2, column=0, padx=5, pady=8, sticky="e")
    confirm_password_entry = tk.Entry(input_frame, show="*", font=("微软雅黑", 12))
    confirm_password_entry.grid(row=2, column=1, padx=5, pady=8, sticky="we", columnspan=2)

    tk.Label(input_frame, text="用户类型：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=3, column=0, padx=5, pady=8, sticky="e")
    user_type_var = tk.IntVar(value=0)
    user_cate_radiobtn1 = tk.Radiobutton(input_frame, text="普通用户", variable=user_type_var, value=1, bg="#f5f6fa", font=("微软雅黑", 11))
    user_cate_radiobtn2 = tk.Radiobutton(input_frame, text="管理员", variable=user_type_var, value=2, bg="#f5f6fa", font=("微软雅黑", 11))
    user_cate_radiobtn1.grid(row=3, column=1, sticky="w", padx=2)
    user_cate_radiobtn2.grid(row=3, column=2, sticky="w", padx=2)

    input_frame.grid_columnconfigure(1, weight=1)
    input_frame.grid_columnconfigure(2, weight=1)

    # 按钮区
    btn_frame = tk.Frame(reg_window, bg="#f5f6fa")
    btn_frame.pack(pady=18)
    btn_style = {
        "font": ("微软雅黑", 12),
        "width": 10,
        "bg": "#40739e",
        "fg": "white",
        "activebackground": "#718093",
        "activeforeground": "white",
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2"
    }
    tk.Button(
        btn_frame,
        text="注册",
        command=lambda: sign_up(username_entry, password_entry, confirm_password_entry, user_type_var),
        **btn_style
    ).pack(side="left", padx=14)
    tk.Button(btn_frame, text="取消", command=reg_window.destroy, **btn_style).pack(side="left", padx=14)


def sign_up(username_entry, password_entry, confirm_password_entry, user_type_var):
    username = username_entry.get().strip()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    user_type = user_type_var.get()

    if not username or not password or not confirm_password:
        msg.showwarning("警告", "请填写所有字段")
        return

    if password != confirm_password:
        msg.showwarning("警告", "两次输入的密码不一致")
        return

    # 检查用户名是否已存在
    database_cursor.execute("SELECT * FROM user_info WHERE user_name=?", (username,))
    if database_cursor.fetchone():
        msg.showwarning("警告", "用户名已存在")
        return

    # 密码加密
    salt = os.urandom(16).hex()  # 生成随机盐
    password_hash = hashlib.sha256((password+salt).encode('utf-8')).hexdigest()

    try:
        database_cursor.execute(
            "INSERT INTO user_info (user_name, user_passwd_e, salt ,user_cate) VALUES (?, ?, ?, ?)",
            (username, password_hash, salt, user_type)
        )
        database_connection.commit()
        msg.showinfo("注册成功", "注册成功，请登录！")
        # 关闭注册窗口
        for widget in tk._default_root.winfo_children():
            if isinstance(widget, tk.Toplevel) and widget.title() == "注册":
                widget.destroy()
                break
    except Exception as e:
        msg.showerror("错误", f"注册失败: {e}")

# 图书信息表字段
# ["barcode", "title", "author", "publisher", "year", "isbn", "clc_code", "call_number", "avaliable_copies", "total_copies", "lend_times"] 




def add_book():
    add_book_window = tk.Toplevel(root)
    add_book_window.title("添加书籍")
    add_book_window.geometry("400x500")
    add_book_window.configure(bg="#f5f6fa")
    tk.Label(add_book_window, text="添加书籍", font=("微软雅黑", 18, "bold"), bg="#f5f6fa", fg="#273c75").pack(pady=(18, 10))
    # 输入区
    input_frame = tk.Frame(add_book_window, bg="#f5f6fa")
    input_frame.pack(pady=10, padx=20, fill="x")
    tk.Label(input_frame, text="书名：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=0, column=0, padx=5, pady=8, sticky="e")
    title_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    title_entry.grid(row=0, column=1, padx=5, pady=8, sticky="we", columnspan=2)
    tk.Label(input_frame, text="作者：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=1, column=0, padx=5, pady=8, sticky="e")
    author_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    author_entry.grid(row=1, column=1, padx=5, pady=8, sticky="we", columnspan=2)
    tk.Label(input_frame, text="出版社：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=2, column=0, padx=5, pady=8, sticky="e")
    publisher_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    publisher_entry.grid(row=2, column=1, padx=5, pady=8, sticky="we", columnspan=2)
    tk.Label(input_frame, text="出版年份：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=3, column=0, padx=5, pady=8, sticky="e")
    year_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    year_entry.grid(row=3, column=1, padx=5, pady=8, sticky="we", columnspan=2)
    tk.Label(input_frame, text="ISBN：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=4, column=0, padx=5, pady=8, sticky="e")
    isbn_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    isbn_entry.grid(row=4, column=1, padx=5, pady=8, sticky="we", columnspan=2)
    tk.Label(input_frame, text="分类号：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=5, column=0, padx=5, pady=8, sticky="e")
    clc_code_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    clc_code_entry.grid(row=5, column=1, padx=5, pady=8, sticky="we", columnspan=2)
    tk.Label(input_frame, text="索书号：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=6, column=0, padx=5, pady=8, sticky="e")
    call_number_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    call_number_entry.grid(row=6, column=1, padx=5, pady=8, sticky="we", columnspan=2)
    tk.Label(input_frame, text="可借阅数量：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=7, column=0, padx=5, pady=8, sticky="e")
    available_copies_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    available_copies_entry.grid(row=7, column=1, padx=5, pady=8, sticky="we", columnspan=2)
    tk.Label(input_frame, text="总数量：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=8, column=0, padx=5, pady=8, sticky="e")
    total_copies_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    total_copies_entry.grid(row=8, column=1, padx=5, pady=8, sticky="we", columnspan=2)
    # 按钮区
    btn_frame = tk.Frame(add_book_window, bg="#f5f6fa")
    btn_frame.pack(pady=18)
    btn_style = {
        "font": ("微软雅黑", 12),
        "width": 10,
        "bg": "#40739e",
        "fg": "white",
        "activebackground": "#718093",
        "activeforeground": "white",
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2"
    }
    tk.Button(
        btn_frame,
        text="添加",
        command=lambda: add_book_confirm(
            title_entry, author_entry, publisher_entry, year_entry,
            isbn_entry, clc_code_entry, call_number_entry,
            available_copies_entry, total_copies_entry
        ),
        **btn_style
    ).pack(side="left", padx=14)
    tk.Button(btn_frame, text="取消", command=add_book_window.destroy, **btn_style).pack(side="left", padx=14)

def add_book_confirm(title_entry, author_entry, publisher_entry, year_entry,
            isbn_entry, clc_code_entry, call_number_entry,
            available_copies_entry, total_copies_entry):
    # 获取输入框的值
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    publisher = publisher_entry.get().strip()
    year = year_entry.get().strip()
    isbn = isbn_entry.get().strip()
    clc_code = clc_code_entry.get().strip()
    call_number = call_number_entry.get().strip()
    available_copies = available_copies_entry.get().strip()
    total_copies = total_copies_entry.get().strip()

    # 检查是否为空
    if not all([title, author, publisher, year, isbn, clc_code, call_number, available_copies, total_copies]):
        msg.showwarning("警告", "请填写所有字段")
        return

    # 检查ISBN格式
    if not isbn.isdigit() or len(isbn) != 13:
        msg.showwarning("警告", "ISBN必须是13位数字")
        return

    # 检查数量是否为正整数
    if not (available_copies.isdigit() and total_copies.isdigit()):
        msg.showwarning("警告", "可借阅数量和总数量必须是正整数")
        return

    # 插入数据到数据库
    try:
        database_cursor.execute(
            "INSERT INTO book_info (title, author, publisher, year, isbn, clc_code, call_number, avaliable_copies, total_copies) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (title, author, publisher, year, isbn, clc_code, call_number, int(available_copies), int(total_copies))
        )
        database_connection.commit()
        msg.showinfo("添加成功", "书籍添加成功！")
        add_book_window.destroy()
    except Exception as e:
        msg.showerror("错误", f"添加书籍失败: {e}")



def delete_book():
    pass
def modify_book():
    pass
def search_book():
    pass
def borrow_book():
    pass
def return_book():
    pass
def view_borrowed_books():
    pass
def view_book_list():
    pass
def view_user_info():
    pass
def view_borrow_history():
    # 读者用户查看自己的借阅记录
    pass
def view_borrow_history_total():
    # 管理员查看总借阅记录
    pass

def admin_window():
    print("我是管理员")
    main_window = tk.Toplevel(root)
    main_window.title("主窗口")
    main_window.geometry("600x500")
    tk.Label(main_window, text="欢迎使用图书管理系统！").pack(pady=10)
    btn_texts_cmds = [
        ("添加书籍", add_book),
        ("删除书籍", delete_book),
        ("修改书籍信息", modify_book),
        ("查询书籍", search_book),
        ("借阅书籍", borrow_book),
        ("归还书籍", return_book),
        ("查看借阅记录", view_borrow_history_total),
        ("查看书籍列表", view_book_list),
        ("查看借阅书籍", view_borrowed_books),
        ("退出", main_window.destroy)
    ]
    btn_frame = tk.Frame(main_window)
    btn_frame.pack(pady=10)
    for text, cmd in btn_texts_cmds:
        tk.Button(btn_frame, text=text, width=18, command=cmd).pack(pady=3)


def reader_window():
    print("我是普通用户")
    reader_window = tk.Toplevel(root)
    reader_window.title("主窗口")
    reader_window.geometry("600x500")
    tk.Label(reader_window, text="欢迎使用图书管理系统！").pack(pady=10)
    btn_texts_cmds = [
        ("查询书籍", search_book),
        ("借阅书籍", borrow_book),
        ("归还书籍", return_book),
        ("查看个人借阅记录", view_borrow_history),
        ("查看个人信息", view_user_info),
        ("查看借阅书籍", view_borrowed_books),
        ("查看借阅历史", view_borrow_history),
        ("退出", reader_window.destroy)
    ]
    btn_frame = tk.Frame(reader_window)
    btn_frame.pack(pady=10)
    for text, cmd in btn_texts_cmds:
        tk.Button(btn_frame, text=text, width=18, command=cmd).pack(pady=3)




# 初始化数据库
database_path = r"data.db"
database_connection = sql.connect(database_path)
database_cursor = database_connection.cursor()
root = tk.Tk()
root.title("图书管理系统")
root.geometry("400x550")
root.resizable(False, False)

# 设置整体背景色
root.configure(bg="#f5f6fa")

# 标题
title_label = tk.Label(root, text="图书管理系统", font=("微软雅黑", 26, "bold"), bg="#f5f6fa", fg="#273c75")
title_label.pack(pady=(30, 20))

# 按钮样式
btn_style = {
    "font": ("微软雅黑", 14),
    "width": 18,
    "height": 2,
    "bg": "#40739e",
    "fg": "white",
    "activebackground": "#718093",
    "activeforeground": "white",
    "bd": 0,
    "relief": "flat",
    "cursor": "hand2"
}

# 按钮容器
btn_frame = tk.Frame(root, bg="#f5f6fa")
btn_frame.pack(pady=10)

log_btn = tk.Button(btn_frame, text="登录", command=log_window_launch, **btn_style)
reg_btn = tk.Button(btn_frame, text="注册", command=reg_window_launch, **btn_style)
test_btn = tk.Button(btn_frame, text="管理员测试", command=admin_window, **btn_style)
reader_test_btn = tk.Button(btn_frame, text="读者测试", command=reader_window, **btn_style)
quit_btn = tk.Button(btn_frame, text="退出", command=root.quit, **btn_style)

# 按钮布局
log_btn.pack(pady=5)
reg_btn.pack(pady=5)
test_btn.pack(pady=5)
reader_test_btn.pack(pady=5)
quit_btn.pack(pady=(20, 5))

root.mainloop()