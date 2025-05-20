# 导入包
import tkinter as tk # 图形界面库
import tkinter.messagebox as msg #消息框
import sqlite3 as sql # 数据库连接
import hashlib # 哈希加密库

# 定义调试用户
default_username = "admin"
default_password = "123456"

class MyApp(tk.Frame):
    '''主窗口类
    继承自tk.Frame类
    类方法：

    '''
    def __init__(self, master=None):
        '''初始化方法
        参数：
            master: 主窗口
        '''
        self.master = master
        self.master.title("应用程序模板")
        self.create_widgets()

    def create_widgets(self):
        """主界面控件及布局"""
        self.title_label = tk.Label(self.master, 
                                    text="图书管理系统",
                                    font=("", 24))
        self.log_btn = tk.Button(self.master, 
                                 text="登录", 
                                 font=("", 14),
                                 command=self.login_window)
        self.reg_btn = tk.Button(self.master, 
                                 text="注册", 
                                 font=("", 14),
                                 command=self.register_window)
        self.quit_btn = tk.Button(self.master, 
                                 text="退出", 
                                 font=("", 14),
                                 command=self.master.quit)

        # 控件布局
        self.title_label.pack()
        self.log_btn.pack()
        self.reg_btn.pack()
        self.quit_btn.pack()

    def login_window(self):
        log_window = tk.Toplevel(self.master)
        log_window.title("登录")
        log_window.geometry("300x200")
        tk.Label(log_window, text="用户名：").grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.username_entry = tk.Entry(log_window)
        self.username_entry.grid(row=1, column=2, padx=10, pady=10)
        tk.Label(log_window, text="密码：").grid(row=2, column=1, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(log_window, show="*")
        self.password_entry.grid(row=2, column=2, padx=10, pady=10)
        tk.Button(log_window, text="登录", command=self.signin).grid(row=3, column=1, padx=10, pady=20)
        tk.Button(log_window, text="取消", command=log_window.destroy).grid(row=3, column=2, padx=10, pady=20)
        log_window.protocol("WM_DELETE_WINDOW", log_window.destroy)
        log_window.transient(self.master)

    def signin(self):
        """登录验证"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == default_username and password == default_password:
            msg.showinfo("登录成功", "欢迎使用图书管理系统！")
            self.master.destroy()
        else:
            msg.showerror("登录失败", "用户名或密码错误，请重试。")


    def register_window(self):
        reg_window = tk.Toplevel(self.master)
        reg_window.title("注册")
        reg_window.geometry("300x200")
        tk.Label(reg_window, text="用户名：").grid(row=1, column=1, padx=10, pady=10, sticky="e")
        username_entry = tk.Entry(reg_window)
        username_entry.grid(row=1, column=2, padx=10, pady=10)
        tk.Label(reg_window, text="密码：").grid(row=2, column=1, padx=10, pady=10, sticky="e")
        password_entry = tk.Entry(reg_window, show="*")
        password_entry.grid(row=2, column=2, padx=10, pady=10)
        tk.Button(reg_window, text="注册", command=lambda: self.register(username_entry.get(), password_entry.get())).grid(row=3, column=1, padx=10, pady=20)
        tk.Button(reg_window, text="取消", command=reg_window.destroy).grid(row=3, column=2, padx=10, pady=20)
        reg_window.protocol("WM_DELETE_WINDOW", reg_window.destroy)

# 初始化数据库
database_path = r"database.db"
database_connection = sql.connect(database_path)
database_cursor = database_connection.cursor()

# 创建应用程序实例
root = tk.Tk()
app = MyApp(root)
root.geometry("400x200")
root.title("智能图书管理系统")
root.mainloop()
