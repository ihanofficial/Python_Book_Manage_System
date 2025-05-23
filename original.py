import tkinter as tk # 图形界面库
import tkinter.messagebox as msg #消息框
import sqlite3 as sql # 数据库连接
import hashlib # 哈希加密库

# 初始化数据库
database_path = r""
database_connection = sql.connect(database_path)
database_cursor = database_connection.cursor()

# 定义调试用户
default_username = "admin"
default_password = "123456"

# 定义日志字段
# rating = 5.0
# log_string = "{"+f'"rating":{rating}  '+"}"

# 定义功能函数
def sign_in():
    msg.showinfo("标题","你点击了登录按钮")

def sign_up():
    msg.showinfo("标题","你点击了注册按钮")

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
    user_type_var = tk.IntVar(value=1)
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
    tk.Button(btn_frame, text="注册", command=sign_up, **btn_style).pack(side="left", padx=14)
    tk.Button(btn_frame, text="取消", command=reg_window.destroy, **btn_style).pack(side="left", padx=14)

    reg_window.protocol("WM_DELETE_WINDOW", reg_window.destroy)
    reg_window.transient(root)


def add_book():
    pass
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