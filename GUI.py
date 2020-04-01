from tkinter import *
from tkinter import messagebox, filedialog
from os import getcwd
import core
from post import *


def main():
    root = Tk()
    root.title("终极斗罗更新查看器")
    app = App(root)
    spider = core.SpiderThread(1, app)
    app.spider = spider
    spider.start()
    mainloop()
    spider.running = False


class App:
    root: Tk
    posts = []
    post: Post
    spider = None

    def __init__(self, root: Tk):
        assert isinstance(root, Tk)
        # 窗口初始化
        self.root = root

        # 变量初始化
        self.post = None
        self.str_info = StringVar()
        self.str_info.set("状态：未更新\n标题：----\n发帖者：----")
        self.see_cartoon = IntVar()
        self.see_cartoon.set(0)
        self.see_fiction = IntVar()
        self.see_fiction.set(1)
        self.path = StringVar()
        self.path.set(getcwd())
        self.type = IntVar()
        self.type.set(1)
        self.suffix = StringVar()
        self.suffix.set("docx")

        self.info_frame = self.create_info_frame()
        self.info_frame.pack()

        self.get_frame = self.create_get_frame()
        self.get_frame.pack()

        self.save_frame = self.create_save_frame()
        self.save_frame.pack()

    def update_post(self):
        for post in self.posts:
            if post.type == PostType.FICTION and self.see_fiction.get() == 1:
                self.post = post
                messagebox.showinfo("提示", "终极斗罗 %s 更新了！" % post.title)
                break
            if post.type == PostType.CARTOON and self.see_cartoon.get() == 1:
                self.post = post
                messagebox.showinfo("提示", "终极斗罗 %s 更新了！" % post.title)
                break
            del self.posts[0]
        else:
            self.str_info.set("状态：未更新\n标题：----\n发帖者：----\n")
            self.post = None
            return False
        self.str_info.set("状态：已更新\n标题：%s\n发帖者：%s\n" % (self.post.title, self.post.lz))
        return True

    def create_info_frame(self) -> Frame:
        frame = Frame(self.root)

        info_label = Label(frame, textvariable=self.str_info, justify=LEFT, font=('微软雅黑', 10))
        info_label.pack(pady=10)

        def log(func):
            def wrapper():
                if self.post is None:
                    messagebox.showerror("警告", "未更新！")
                    return
                func()
                self.posts.remove(self.post)
                self.update_post()
            return wrapper

        @log
        def go_to_url():
            core.open_url(self.post.url)

        open_button = Button(frame, text="前往链接", command=go_to_url)
        open_button.pack(side=LEFT, padx=10)

        @log
        def save_post():
            core.save(self.post, self.suffix, self.path.get())

        save_button = Button(frame, text="保存", command=save_post)
        save_button.pack(side=LEFT, padx=10)

        return frame

    def create_get_frame(self) -> Frame:
        frame = Frame(self.root)

        get_label_frame = LabelFrame(frame, text="获取帖子类型")

        get_checkbutton = Checkbutton(get_label_frame, text="小说", variable=self.see_fiction)
        get_checkbutton.pack()
        get_checkbutton = Checkbutton(get_label_frame, text="漫画", variable=self.see_cartoon)
        get_checkbutton.pack()

        get_label_frame.pack(pady=10)

        check_frame = Frame(frame)

        Label(check_frame, text="每过").pack(side=LEFT, padx=10)

        def check(event):
            try:
                sleeping_time = check_spinbox.get()
                if len(sleeping_time) == 0:
                    return
                sleeping_time = int(sleeping_time)
            except ValueError:
                messagebox.showerror("警告", "无效输入")
                check_spinbox.delete(0, END)
                check_spinbox.insert(0, '1')
                return

            if sleeping_time > 60:
                sleeping_time = 60
                check_spinbox.delete(0, END)
                check_spinbox.insert(0, '60')
            if sleeping_time < 1:
                sleeping_time = 1
                check_spinbox.delete(0, END)
                check_spinbox.insert(0, '1')
            self.spider.sleeping_time = sleeping_time

        check_spinbox = Spinbox(check_frame, from_=1, to=60)
        check_spinbox.pack(side=LEFT, pady=10)
        check_spinbox.bind("<KeyRelease>", check)

        Label(check_frame, text="分钟检查是否更新").pack(side=LEFT, padx=10)

        check_frame.pack(anchor=S)

        return frame

    def create_save_frame(self) -> Frame:
        frame = Frame(self.root)

        path_frame = Frame(frame)

        Label(frame, text="保存至：").pack()
        path_entry = Entry(path_frame, width=60, textvariable=self.path)
        path_entry.pack(side=LEFT)
        path_button = Button(path_frame, text="......", command=lambda: self.path.set(filedialog.askdirectory()))
        path_button.pack(side=LEFT)

        path_frame.pack(padx=10)

        type_label_frame = LabelFrame(frame, text="文件类型:")

        def update_suffix(event: Event):
            if self.type.get() == 1:
                self.suffix.set("docx")
            elif self.type.get() == 2:
                self.suffix.set("txt")

        types = [
            ("word文档(.docx文件)", 1),
            ("文本文档(.txt文件)", 2),
            ("其他(请注明后缀)", 3)
        ]
        for t in types:
            b = Radiobutton(type_label_frame, text=t[0], variable=self.type, value=t[1])
            b.pack(anchor=W)
            b.bind("<Motion>", update_suffix)

        type_entry = Entry(type_label_frame, textvariable=self.suffix)
        type_entry.pack()

        type_label_frame.pack(pady=10)

        return frame


if __name__ == '__main__':
    main()
