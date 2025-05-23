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


# 定义功能函数
def sign_in():
    msg.showinfo("标题","你点击了登录按钮")

def sign_up():
    msg.showinfo("标题","你点击了注册按钮")

def log_window_launch():
    log_window = tk.Toplevel(root)
    log_window.title("登录")
    log_window.geometry("300x200")

    tk.Label(log_window, text="用户名：").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    username_entry = tk.Entry(log_window)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(log_window, text="密码：").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    password_entry = tk.Entry(log_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(log_window, text="登录", command=sign_in).grid(row=2, column=0, padx=10, pady=20)
    tk.Button(log_window, text="取消", command=log_window.destroy).grid(row=2, column=1, padx=10, pady=20)
    log_window.protocol("WM_DELETE_WINDOW", log_window.destroy)
    log_window.transient(root)


def reg_window_launch():
    reg_window = tk.Toplevel(root)
    reg_window.title("注册")
    reg_window.geometry("350x250")

    # 用户名
    tk.Label(reg_window, text="用户名：").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    username_entry = tk.Entry(reg_window)
    username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="we", columnspan=2)

    # 密码
    tk.Label(reg_window, text="密码：").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    password_entry = tk.Entry(reg_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we", columnspan=2)

    # 确认密码
    tk.Label(reg_window, text="确认密码：").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    confirm_password_entry = tk.Entry(reg_window, show="*")
    confirm_password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="we", columnspan=2)

    # 用户类型
    tk.Label(reg_window, text="用户类型：").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    user_type_var = tk.IntVar(value=0)
    user_cate_radiobtn1 = tk.Radiobutton(reg_window, text="普通用户", variable=user_type_var, value=1)
    user_cate_radiobtn2 = tk.Radiobutton(reg_window, text="管理员", variable=user_type_var, value=2)
    user_cate_radiobtn1.grid(row=3, column=1, sticky="w")
    user_cate_radiobtn2.grid(row=3, column=2, sticky="w")

    # 按钮
    btn_frame = tk.Frame(reg_window)
    btn_frame.grid(row=4, column=0, columnspan=3, pady=20)
    tk.Button(btn_frame, text="注册", width=10, command=sign_up).pack(side="left", padx=10)
    tk.Button(btn_frame, text="取消", width=10, command=reg_window.destroy).pack(side="left", padx=10)

    # 使输入框和按钮自适应窗口宽度
    reg_window.grid_columnconfigure(1, weight=1)
    reg_window.grid_columnconfigure(2, weight=1)

    reg_window.protocol("WM_DELETE_WINDOW", reg_window.destroy)


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
        ("查看借阅记录", view_borrow_history),
        ("查看书籍列表", view_book_list),
        ("查看个人信息", view_user_info),
        ("查看借阅书籍", view_borrowed_books),
        ("查看用户信息", view_user_info),
        ("查看借阅历史", view_borrow_history),
        ("退出", main_window.destroy)
    ]
    btn_frame = tk.Frame(main_window)
    btn_frame.pack(pady=10)
    for text, cmd in btn_texts_cmds:
        tk.Button(btn_frame, text=text, width=18, command=cmd).pack(pady=3)


def reader_window():
    pass

root = tk.Tk()
title_label = tk.Label(root, text="图书管理系统",font=("", 24))
log_btn = tk.Button(root,text="登录",font=("", 14), command=log_window_launch)
reg_btn = tk.Button(root,text="注册", font=("", 14), command=reg_window_launch)
test_btn = tk.Button(root,text="管理员测试", font=("", 14), command=admin_window)
quit_btn = tk.Button(root, text="退出", font=("", 14), command=root.quit)

# 布局
title_label.pack()
log_btn.pack()
reg_btn.pack()
test_btn.pack()
quit_btn.pack()
root.mainloop()