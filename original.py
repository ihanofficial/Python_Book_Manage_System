import tkinter as tk  # 图形界面库
import tkinter.messagebox as msg  # 消息框
import sqlite3 as sql  # 数据库连接
import hashlib  # 哈希加密库
import os
from tkinter import ttk
import datetime  # 日期时间库

# 初始化数据库
database_path = r"D:\GitRepo\Python_Book_Manage_System\data.db"
database_connection = sql.connect(database_path)
database_cursor = database_connection.cursor()


root = tk.Tk()
root.iconphoto(True, tk.PhotoImage(file='ico.png'))
print(os.curdir)
root.title("图书管理系统")
root.geometry("400x450")
root.resizable(False, False)

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
    password_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

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


# 定义功能函数
def sign_in():
    global UserID
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
    UserID = username
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

    tk.Label(input_frame, text="用户名：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=0, column=0, padx=5, pady=10,
                                                                                    sticky="e")
    username_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    username_entry.grid(row=0, column=1, padx=5, pady=10, sticky="we")

    tk.Label(input_frame, text="密码：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=1, column=0, padx=5, pady=10,
                                                                                  sticky="e")
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

    tk.Label(input_frame, text="用户名：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=0, column=0, padx=5, pady=8,
                                                                                    sticky="e")
    username_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    username_entry.grid(row=0, column=1, padx=5, pady=8, sticky="we", columnspan=2)

    tk.Label(input_frame, text="密码：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=1, column=0, padx=5, pady=8,
                                                                                  sticky="e")
    password_entry = tk.Entry(input_frame, show="*", font=("微软雅黑", 12))
    password_entry.grid(row=1, column=1, padx=5, pady=8, sticky="we", columnspan=2)

    tk.Label(input_frame, text="确认密码：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=2, column=0, padx=5, pady=8,
                                                                                      sticky="e")
    confirm_password_entry = tk.Entry(input_frame, show="*", font=("微软雅黑", 12))
    confirm_password_entry.grid(row=2, column=1, padx=5, pady=8, sticky="we", columnspan=2)

    tk.Label(input_frame, text="用户类型：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=3, column=0, padx=5, pady=8,
                                                                                      sticky="e")
    user_type_var = tk.IntVar(value=0)
    user_cate_radiobtn1 = tk.Radiobutton(input_frame, text="普通用户", variable=user_type_var, value=1, bg="#f5f6fa",
                                         font=("微软雅黑", 11))
    user_cate_radiobtn2 = tk.Radiobutton(input_frame, text="管理员", variable=user_type_var, value=2, bg="#f5f6fa",
                                         font=("微软雅黑", 11))
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





# 图书信息表字段
# ["barcode", "title", "author", "publisher", "year", "isbn", "clc_code", "call_number", "avaliable_copies", "total_copies", "lend_times"] 


def add_book():
    add_book_window = tk.Toplevel(root)
    add_book_window.title("添加书籍")
    add_book_window.geometry("420x520")
    add_book_window.configure(bg="#f5f6fa")

    tk.Label(
        add_book_window, text="添加书籍", font=("微软雅黑", 18, "bold"),
        bg="#f5f6fa", fg="#273c75"
    ).pack(pady=(18, 10))

    input_frame = tk.Frame(add_book_window, bg="#f5f6fa")
    input_frame.pack(pady=10, padx=30, fill="x")

    labels = [
        "条形码(barcode)：", "书名：", "作者：", "出版社：", "出版年份：",
        "ISBN：", "分类号：", "索书号：", "可借阅数量：", "总数量："
    ]
    entries = []
    for i, label_text in enumerate(labels):
        tk.Label(
            input_frame, text=label_text, font=("微软雅黑", 12), bg="#f5f6fa"
        ).grid(row=i, column=0, padx=5, pady=8, sticky="e")
        entry = tk.Entry(input_frame, font=("微软雅黑", 12))
        entry.grid(row=i, column=1, padx=5, pady=8, sticky="we")
        entries.append(entry)

    input_frame.grid_columnconfigure(1, weight=1)

    (
        barcode_entry, title_entry, author_entry, publisher_entry, year_entry,
        isbn_entry, clc_code_entry, call_number_entry,
        available_copies_entry, total_copies_entry
    ) = entries

    btn_frame = tk.Frame(add_book_window, bg="#f5f6fa")
    btn_frame.pack(pady=24)
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
            barcode_entry, title_entry, author_entry, publisher_entry, year_entry,
            isbn_entry, clc_code_entry, call_number_entry,
            available_copies_entry, total_copies_entry
        ),
        **btn_style
    ).pack(side="left", padx=18)
    tk.Button(
        btn_frame, text="取消", command=add_book_window.destroy, **btn_style
    ).pack(side="left", padx=18)


def add_book_confirm(barcode_entry, title_entry, author_entry, publisher_entry, year_entry,
                     isbn_entry, clc_code_entry, call_number_entry,
                     available_copies_entry, total_copies_entry):
    # 获取输入框的值
    barcode = barcode_entry.get().strip()
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
            "INSERT INTO book_info (barcode, title, author, publisher, year, isbn, clc_code, call_number, avaliable_copies, total_copies) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (barcode, title, author, publisher, year, isbn, clc_code, call_number, int(available_copies),
             int(total_copies))
        )
        database_connection.commit()
        msg.showinfo("添加成功", "书籍添加成功！")
    except Exception as e:
        msg.showerror("错误", f"添加书籍失败: {e}")


def delete_book():
    delete_book_window = tk.Toplevel(root)
    delete_book_window.title("删除书籍")
    delete_book_window.geometry("400x200")
    delete_book_window.configure(bg="#f5f6fa")
    tk.Label(delete_book_window, text="删除书籍", font=("微软雅黑", 18, "bold"), bg="#f5f6fa", fg="#273c75").pack(
        pady=(18, 10))
    # 输入区
    input_frame = tk.Frame(delete_book_window, bg="#f5f6fa")
    input_frame.pack(pady=10, padx=20, fill="x")
    tk.Label(input_frame, text="条形码(barcode)：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=0, column=0, padx=5,
                                                                                             pady=8, sticky="e")
    barcode_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    barcode_entry.grid(row=0, column=1, padx=5, pady=8, sticky="we", columnspan=2)
    # 按钮区
    btn_frame = tk.Frame(delete_book_window, bg="#f5f6fa")
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
        text="删除",
        command=lambda: delete_book_confirm(barcode_entry),
        **btn_style
    ).pack(side="left", padx=14)
    tk.Button(btn_frame, text="取消", command=delete_book_window.destroy, **btn_style).pack(side="left", padx=14)


def delete_book_confirm(barcode_entry):
    # 获取输入框的值
    barcode = barcode_entry.get().strip()

    # 检查是否为空
    if not barcode:
        msg.showwarning("警告", "请输入条形码")
        return

    # 删除数据到数据库
    try:
        database_cursor.execute(
            "DELETE FROM book_info WHERE barcode=?",
            (barcode,)
        )
        database_connection.commit()
        msg.showinfo("删除成功", "书籍删除成功！")
    except Exception as e:
        msg.showerror("错误", f"删除书籍失败: {e}")


def modify_book():
    # 创建窗口
    modify_book_window = tk.Toplevel(root)
    modify_book_window.title("修改书籍信息")
    modify_book_window.geometry("950x350")
    modify_book_window.configure(bg="#f5f6fa")

    tk.Label(modify_book_window, text="修改书籍信息", font=("微软雅黑", 18, "bold"),
             bg="#f5f6fa", fg="#273c75").pack(pady=(18, 10))

    # 查找栏
    search_frame = tk.Frame(modify_book_window, bg="#f5f6fa")
    search_frame.pack(pady=5, padx=10, fill="x")
    tk.Label(search_frame, text="书名：", font=("微软雅黑", 12), bg="#f5f6fa").pack(side="left")
    search_entry = tk.Entry(search_frame, font=("微软雅黑", 12), width=30)
    search_entry.pack(side="left", padx=5)
    # Treeview显示区
    columns = [
        "barcode", "title", "author", "publisher", "year", "isbn",
        "clc_code", "call_number", "avaliable_copies", "total_copies", "lend_times"
    ]
    col_names = [
        "条形码", "书名", "作者", "出版社", "年份", "ISBN",
        "分类号", "索书号", "可借阅数量", "总数量", "借阅次数"
    ]
    tree = ttk.Treeview(modify_book_window, columns=columns, show="headings", height=5)
    for col, name in zip(columns, col_names):
        tree.heading(col, text=name)
        tree.column(col, width=80, anchor="center")
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # 可编辑Treeview：双击单元格弹出Entry进行编辑
    edit_widgets = {}

    def on_tree_double_click(event):
        item = tree.identify_row(event.y)
        column = tree.identify_column(event.x)
        if not item or not column:
            return
        col_idx = int(column.replace("#", "")) - 1
        if col_idx < 0 or col_idx >= len(columns):
            return
        col = columns[col_idx]
        if col == "lend_times":
            msg.showerror("错误", "系统不允许直接修改借阅次数")
            return
        x, y, width, height = tree.bbox(item, column)
        value = tree.set(item, col)
        entry = tk.Entry(tree, font=("微软雅黑", 12))
        entry.insert(0, value)
        entry.place(x=x, y=y, width=width, height=height)
        entry.focus()

        def save_edit(event=None):
            new_value = entry.get()
            tree.set(item, col, new_value)
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: entry.destroy())
        edit_widgets[(item, col)] = entry

    tree.bind("<Double-1>", on_tree_double_click)

    # 查找按钮
    def search_and_show():
        for row in tree.get_children():
            tree.delete(row)
        title = search_entry.get().strip()
        if not title:
            msg.showwarning("警告", "请输入书名")
            return
        try:
            database_cursor.execute("SELECT * FROM book_info WHERE title=?", (title,))
            result = database_cursor.fetchone()
            if result:
                tree.insert("", "end", values=result)
            else:
                msg.showwarning("未找到", "未找到该书籍")
        except Exception as e:
            msg.showerror("错误", f"查询失败: {e}")

    tk.Button(search_frame, text="查找", font=("微软雅黑", 12), bg="#40739e", fg="white",
              activebackground="#718093", activeforeground="white", bd=0, relief="flat",
              cursor="hand2", command=search_and_show).pack(side="left", padx=8)

    # 保存更改按钮
    def save_changes():
        items = tree.get_children()
        if not items:
            msg.showwarning("警告", "没有可保存的数据")
            return
        item = items[0]
        values = tree.item(item, "values")
        # 字段顺序: barcode, title, author, publisher, year, isbn, clc_code, call_number, avaliable_copies, total_copies, lend_times
        try:
            database_cursor.execute(
                """UPDATE book_info SET
                    title=?, author=?, publisher=?, year=?, isbn=?, clc_code=?, call_number=?, avaliable_copies=?, total_copies=?
                   WHERE barcode=?""",
                (
                    values[1], values[2], values[3], values[4], values[5], values[6], values[7],
                    int(values[8]), int(values[9]), values[0]
                )
            )
            database_connection.commit()
            msg.showinfo("成功", "更改已保存到数据库")
        except Exception as e:
            msg.showerror("错误", f"保存更改失败: {e}")

    btn_frame = tk.Frame(modify_book_window, bg="#f5f6fa")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="保存更改", font=("微软雅黑", 12), bg="#40739e", fg="white",
              activebackground="#718093", activeforeground="white", bd=0, relief="flat",
              cursor="hand2", command=save_changes).pack(side="left", padx=14)
    tk.Button(btn_frame, text="关闭", font=("微软雅黑", 12), bg="#40739e", fg="white",
              activebackground="#718093", activeforeground="white", bd=0, relief="flat",
              cursor="hand2", command=modify_book_window.destroy).pack(side="left", padx=14)


def modify_book_confirm(title_entry):
    # 获取输入框的值
    title = title_entry.get().strip()

    # 检查是否为空
    if not title:
        msg.showwarning("警告", "请输入书名")
        return

    # 修改数据到数据库
    try:
        database_cursor.execute(
            "UPDATE book_info SET title=? WHERE title=?",
            (title, title)
        )
        database_connection.commit()
        msg.showinfo("修改成功", "书籍信息修改成功！")
    except Exception as e:
        msg.showerror("错误", f"修改书籍信息失败: {e}")


def search_book():
    search_book_window = tk.Toplevel(root)
    search_book_window.title("查询书籍")
    search_book_window.geometry("400x200")
    search_book_window.configure(bg="#f5f6fa")
    tk.Label(search_book_window, text="查询书籍", font=("微软雅黑", 18, "bold"), bg="#f5f6fa", fg="#273c75").pack(
        pady=(18, 10))
    # 输入区
    input_frame = tk.Frame(search_book_window, bg="#f5f6fa")
    input_frame.pack(pady=10, padx=20, fill="x")
    tk.Label(input_frame, text="书名：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=0, column=0, padx=5, pady=8,
                                                                                  sticky="e")
    title_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    title_entry.grid(row=0, column=1, padx=5, pady=8, sticky="we", columnspan=2)
    # 按钮区
    btn_frame = tk.Frame(search_book_window, bg="#f5f6fa")
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
        text="查询",
        command=lambda: search_book_confirm(title_entry),
        **btn_style
    ).pack(side="left", padx=14)
    tk.Button(btn_frame, text="取消", command=search_book_window.destroy, **btn_style).pack(side="left", padx=14)


def search_book_confirm(title_entry):
    # 获取输入框的值
    title = title_entry.get().strip()

    # 检查是否为空
    if not title:
        msg.showwarning("警告", "请输入书名")
        return

    # 查询数据到数据库
    try:
        database_cursor.execute(
            "SELECT * FROM book_info WHERE title=?",
            (title,)
        )
        result = database_cursor.fetchone()
        if result:
            # 用Treeview显示查找到的书籍信息
            info_window = tk.Toplevel(root)
            info_window.title("书籍信息")
            info_window.geometry("900x120")
            info_window.configure(bg="#f5f6fa")

            columns = [
                "barcode", "title", "author", "publisher", "year", "isbn",
                "clc_code", "call_number", "avaliable_copies", "total_copies", "lend_times"
            ]
            col_names = [
                "条形码", "书名", "作者", "出版社", "年份", "ISBN",
                "分类号", "索书号", "可借阅数量", "总数量", "借阅次数"
            ]

            tree = ttk.Treeview(info_window, columns=columns, show="headings", height=1)
            for col, name in zip(columns, col_names):
                tree.heading(col, text=name)
                tree.column(col, width=80, anchor="center")
            tree.pack(expand=True, fill="both", padx=10, pady=10)

            tree.insert("", "end", values=result)
        else:
            msg.showwarning("查询失败", "未找到该书籍")
    except Exception as e:
        msg.showerror("错误", f"查询书籍失败: {e}")


def borrow_book():
    # 借阅书籍窗口
    borrow_book_window = tk.Toplevel(root)
    borrow_book_window.title("借阅书籍")
    borrow_book_window.geometry("400x200")
    borrow_book_window.configure(bg="#f5f6fa")
    tk.Label(borrow_book_window, text="借阅书籍", font=("微软雅黑", 18, "bold"), bg="#f5f6fa", fg="#273c75").pack(
        pady=(18, 10))
    input_frame = tk.Frame(borrow_book_window, bg="#f5f6fa")
    input_frame.pack(pady=10, padx=20, fill="x")
    tk.Label(input_frame, text="条形码(barcode)：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=0, column=0, padx=5,
                                                                                             pady=8, sticky="e")
    barcode_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    barcode_entry.grid(row=0, column=1, padx=5, pady=8, sticky="we", columnspan=2)

    btn_frame = tk.Frame(borrow_book_window, bg="#f5f6fa")
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

    def borrow_book_confirm():
        barcode = barcode_entry.get().strip()
        if not barcode:
            msg.showwarning("警告", "请输入条形码")
            return
        try:
            # 查询书籍是否存在且可借阅
            database_cursor.execute("SELECT avaliable_copies, rowid, isbn FROM book_info WHERE barcode=?", (barcode,))
            result = database_cursor.fetchone()
            if not result:
                msg.showwarning("警告", "未找到该书籍")
                return
            available, book_rowid, book_isbn = result
            if available <= 0:
                msg.showwarning("警告", "该书籍已无可借阅数量")
                return
            # 借阅操作
            database_cursor.execute(
                "UPDATE book_info SET avaliable_copies=avaliable_copies-1, lend_times=lend_times+1 WHERE rowid=?",
                (book_rowid,)
            )
            database_connection.commit()
            msg.showinfo("借阅成功", "借阅成功！")
            # 写入日志
            op = 1  # 1代表借阅
            out_time = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            current_user = UserID  # 这里应替换为实际登录用户名
            bookID = book_isbn
            log_string = "{" + f'"type_op":{op}, "out_time":{out_time}, "user":"{current_user}","book":"{bookID}"' + "}"
            with open("log.jsonl", "a", encoding="utf-8") as f:
                f.write(log_string + "\n")
            borrow_book_window.destroy()
        except Exception as e:
            msg.showerror("错误", f"借阅书籍失败: {e}")

    tk.Button(btn_frame, text="借阅", command=borrow_book_confirm, **btn_style).pack(side="left", padx=14)
    tk.Button(btn_frame, text="取消", command=borrow_book_window.destroy, **btn_style).pack(side="left", padx=14)


def return_book():
    # 归还书籍窗口
    return_book_window = tk.Toplevel(root)
    return_book_window.title("归还书籍")
    return_book_window.geometry("400x200")
    return_book_window.configure(bg="#f5f6fa")
    tk.Label(return_book_window, text="归还书籍", font=("微软雅黑", 18, "bold"), bg="#f5f6fa", fg="#273c75").pack(
        pady=(18, 10))
    input_frame = tk.Frame(return_book_window, bg="#f5f6fa")
    input_frame.pack(pady=10, padx=20, fill="x")
    tk.Label(input_frame, text="条形码(barcode)：", font=("微软雅黑", 12), bg="#f5f6fa").grid(row=0, column=0, padx=5,
                                                                                             pady=8, sticky="e")
    barcode_entry = tk.Entry(input_frame, font=("微软雅黑", 12))
    barcode_entry.grid(row=0, column=1, padx=5, pady=8, sticky="we", columnspan=2)

    btn_frame = tk.Frame(return_book_window, bg="#f5f6fa")
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

    def return_book_confirm():
        barcode = barcode_entry.get().strip()
        if not barcode:
            msg.showwarning("警告", "请输入条形码")
            return
        try:
            # 查询书籍是否存在
            database_cursor.execute("SELECT avaliable_copies, rowid, isbn FROM book_info WHERE barcode=?", (barcode,))
            result = database_cursor.fetchone()
            if not result:
                msg.showwarning("警告", "未找到该书籍")
                return
            available, book_rowid, book_isbn = result
            # 归还操作
            database_cursor.execute(
                "UPDATE book_info SET avaliable_copies=avaliable_copies+1 WHERE rowid=?",
                (book_rowid,)
            )
            database_connection.commit()
            msg.showinfo("归还成功", "归还成功！")
            # 写入日志
            op = 2  # 2代表归还
            out_time = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            current_user = UserID  # 这里应替换为实际登录用户名
            bookID = book_isbn
            log_string = "{" + f'"type_op":{op}, "out_time":{out_time}, "user":"{current_user}","book":"{bookID}"' + "}"
            with open("log.jsonl", "a", encoding="utf-8") as f:
                f.write(log_string + "\n")
            return_book_window.destroy()
        except Exception as e:
            msg.showerror("错误", f"归还书籍失败: {e}")

    tk.Button(btn_frame, text="归还", command=return_book_confirm, **btn_style).pack(side="left", padx=14)
    tk.Button(btn_frame, text="取消", command=return_book_window.destroy, **btn_style).pack(side="left", padx=14)


def view_borrowed_books():
    # 读取所有未归还书籍（即当前用户已借但未归还的书籍）
    borrowed_books = set()
    try:
        with open("log.jsonl", "r", encoding="utf-8") as f:
            logs = [eval(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        msg.showwarning("提示", "日志文件不存在")
        return

    user_logs = [log for log in logs if log.get("user") == UserID]
    borrow_count = {}
    for log in user_logs:
        book = log.get("book")
        if log.get("type_op") == 1:  # 借阅
            borrow_count[book] = borrow_count.get(book, 0) + 1
        elif log.get("type_op") == 2:  # 归还
            borrow_count[book] = borrow_count.get(book, 0) - 1

    for book, count in borrow_count.items():
        if count > 0:
            borrowed_books.add(book)

    if not borrowed_books:
        msg.showinfo("提示", "当前没有未归还的书籍")
        return

    # 查询书籍详细信息
    books_info = []
    for isbn in borrowed_books:
        database_cursor.execute("SELECT * FROM book_info WHERE isbn=?", (isbn,))
        result = database_cursor.fetchone()
        if result:
            books_info.append(result)

    if not books_info:
        msg.showinfo("提示", "未找到未归还书籍的详细信息")
        return

    # 显示在窗口
    window = tk.Toplevel(root)
    window.title("未归还书籍列表")
    window.geometry("900x300")
    window.configure(bg="#f5f6fa")
    tk.Label(window, text="未归还书籍列表", font=("微软雅黑", 18, "bold"), bg="#f5f6fa", fg="#273c75").pack(
        pady=(18, 10))

    columns = [
        "barcode", "title", "author", "publisher", "year", "isbn",
        "clc_code", "call_number", "avaliable_copies", "total_copies", "lend_times"
    ]
    col_names = [
        "条形码", "书名", "作者", "出版社", "年份", "ISBN",
        "分类号", "索书号", "可借阅数量", "总数量", "借阅次数"
    ]

    tree = ttk.Treeview(window, columns=columns, show="headings", height=8)
    for col, name in zip(columns, col_names):
        tree.heading(col, text=name)
        tree.column(col, width=80, anchor="center")
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    for book in books_info:
        tree.insert("", "end", values=book)


def view_book_list():
    # 读取书籍列表并用Treeview控件显示
    book_list_window = tk.Toplevel(root)
    book_list_window.title("书籍列表")
    book_list_window.geometry("900x400")
    book_list_window.configure(bg="#f5f6fa")
    tk.Label(book_list_window, text="书籍列表", font=("微软雅黑", 18, "bold"), bg="#f5f6fa", fg="#273c75").pack(
        pady=(18, 10))

    columns = [
        "barcode", "title", "author", "publisher", "year", "isbn",
        "clc_code", "call_number", "avaliable_copies", "total_copies", "lend_times"
    ]
    col_names = [
        "条形码", "书名", "作者", "出版社", "年份", "ISBN",
        "分类号", "索书号", "可借阅数量", "总数量", "借阅次数"
    ]

    tree = ttk.Treeview(book_list_window, columns=columns, show="headings", height=15)
    for col, name in zip(columns, col_names):
        tree.heading(col, text=name)
        tree.column(col, width=80, anchor="center")
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # 查询所有书籍
    try:
        database_cursor.execute("SELECT * FROM book_info")
        books = database_cursor.fetchall()
        if not books:
            msg.showinfo("提示", "没有书籍信息")
            book_list_window.destroy()
            return
        for book in books:
            tree.insert("", "end", values=book)
    except Exception as e:
        msg.showerror("错误", f"查询书籍列表失败: {e}")
        book_list_window.destroy()


def view_user_info():
    username = UserID
    # 查询数据库
    try:
        database_cursor.execute("SELECT user_name, user_cate FROM user_info WHERE user_name=?", (username,))
        result = database_cursor.fetchone()
        if not result:
            msg.showwarning("提示", "未找到该用户")
            return
        user_name, user_cate = result
        user_type_str = "管理员" if str(user_cate) == "2" else "普通用户"
        info = f"用户名: {user_name}\n用户类型: {user_type_str}"
        msg.showinfo("用户信息", info)
    except Exception as e:
        msg.showerror("错误", f"查询用户信息失败: {e}")


def view_borrow_history():
    # 读者用户查看自己的借阅记录
    import tkinter.simpledialog
    username = UserID

    # 读取log.jsonl并筛选
    logs = []
    try:
        with open("log.jsonl", "r", encoding="utf-8") as f:
            for line in f:
                try:
                    log = eval(line.strip())
                    if str(log.get("user")) == username:
                        logs.append(log)
                except Exception:
                    continue
    except FileNotFoundError:
        msg.showwarning("提示", "日志文件不存在")
        return

    if not logs:
        msg.showinfo("结果", f"未找到用户 {username} 的借阅记录")
        return

    # 显示结果
    result_str = "\n".join(
        [f'操作:{("借阅" if l["type_op"] == 1 else "归还")}, 时间:{l["out_time"]}, 书籍:{l["book"]}' for l in logs])
    result_window = tk.Toplevel(root)
    result_window.title(f"{username} 的借阅记录")
    result_window.geometry("500x400")
    text = tk.Text(result_window, font=("微软雅黑", 12))
    text.pack(expand=True, fill="both")
    text.insert("end", result_str)
    text.config(state="disabled")


def view_borrow_history_total():
    # 管理员查看总借阅记录（Treeview显示）
    logs = []
    try:
        with open("log.jsonl", "r", encoding="utf-8") as f:
            for line in f:
                try:
                    log = eval(line.strip())
                    logs.append(log)
                except Exception:
                    continue
    except FileNotFoundError:
        msg.showwarning("提示", "日志文件不存在")
        return

    if not logs:
        msg.showinfo("结果", "没有借阅记录")
        return

    # 创建窗口和Treeview
    result_window = tk.Toplevel(root)
    result_window.title("总借阅记录")
    result_window.geometry("700x400")
    columns = ("type_op", "out_time", "user", "book")
    col_names = ("操作", "时间", "用户", "书籍")
    tree = ttk.Treeview(result_window, columns=columns, show="headings", height=18)
    for col, name in zip(columns, col_names):
        tree.heading(col, text=name)
        tree.column(col, width=150 if col != "type_op" else 80, anchor="center")
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # 插入数据
    for l in logs:
        op_str = "借阅" if l.get("type_op") == 1 else "归还"
        out_time = l.get("out_time", "")
        user = l.get("user", "")
        book = l.get("book", "")
        tree.insert("", "end", values=(op_str, out_time, user, book))


def admin_window():
    main_window = tk.Toplevel(root)
    main_window.title("管理员主界面")
    main_window.geometry("600x540")
    main_window.configure(bg="#f5f6fa")
    tk.Label(
        main_window, text=f"你好管理员{UserID}！", font=("微软雅黑", 20, "bold"),
        bg="#f5f6fa", fg="#273c75"
    ).pack(pady=(28, 18))
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
    btn_frame = tk.Frame(main_window, bg="#f5f6fa")
    btn_frame.pack(pady=10)
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
    # 两列布局
    for idx, (text, cmd) in enumerate(btn_texts_cmds):
        row, col = divmod(idx, 2)
        tk.Button(btn_frame, text=text, command=cmd, **btn_style).grid(row=row, column=col, padx=12, pady=7,
                                                                       sticky="we")
    btn_frame.grid_columnconfigure(0, weight=1)
    btn_frame.grid_columnconfigure(1, weight=1)


def reader_window():
    reader_win = tk.Toplevel(root)
    reader_win.title("读者主界面")
    reader_win.geometry("600x420")
    reader_win.configure(bg="#f5f6fa")
    tk.Label(
        reader_win, text=f"你好读者{UserID}！", font=("微软雅黑", 20, "bold"),
        bg="#f5f6fa", fg="#273c75"
    ).pack(pady=(28, 18))
    btn_texts_cmds = [
        ("查询书籍", search_book),
        ("借阅书籍", borrow_book),
        ("归还书籍", return_book),
        ("查看个人借阅记录", view_borrow_history),
        ("查看个人信息", view_user_info),
        ("查看借阅历史", view_borrow_history),
        ("退出", reader_win.destroy)
    ]
    btn_frame = tk.Frame(reader_win, bg="#f5f6fa")
    btn_frame.pack(pady=10)
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
    # 两列布局
    for idx, (text, cmd) in enumerate(btn_texts_cmds):
        row, col = divmod(idx, 2)
        tk.Button(btn_frame, text=text, command=cmd, **btn_style).grid(row=row, column=col, padx=12, pady=7,
                                                                       sticky="we")
    btn_frame.grid_columnconfigure(0, weight=1)
    btn_frame.grid_columnconfigure(1, weight=1)


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
quit_btn = tk.Button(btn_frame, text="退出", command=root.quit, **btn_style)

# 按钮布局
log_btn.pack(pady=5)
reg_btn.pack(pady=5)
quit_btn.pack(pady=(20, 5))

root.mainloop()
