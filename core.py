from spider import *
from post import *
from writer import *
import GUI
import webbrowser
import threading
import os


PATH = os.getcwd()


def set_info(post):
    assert isinstance(post, Post)
    get_info(post)


def set_type(post):
    assert isinstance(post, Post)
    if post.title.find("漫画") != -1:
        post.type = PostType.CARTOON
    elif post.title.find("章") != -1:
        post.type = PostType.FICTION
    else:
        post.type = PostType.OTHER
    return post.type


def open_url(url):
    assert isinstance(url, str)
    webbrowser.open(url)


def save(post, suffix, path):
    assert isinstance(post, Post)
    if post.type == PostType.CARTOON:
        write_image(name=post.title, images=get_images(post.url), path=path, suffix='jpg')
    else:
        write_text(text=post.title + '\n\n' + get_text(post.url), name=post.title, path=path, suffix=suffix)
    os.chdir(PATH)


# 爬虫线程类
class SpiderThread(threading.Thread):
    sleeping_time = 0

    def __init__(self, n, app):
        super(SpiderThread, self).__init__()
        self.sleeping_time = n
        self.app = app
        self.running = True

    def run(self):
        while self.running:
            # 获得现在及以前的置顶帖
            now_top_posts = get_top_posts()
            last_top_posts = []
            with open("LASTED_TOP_POSTS", 'r') as f:
                last_top_posts = f.read().split('\n')
            if len(last_top_posts) == 0:
                with open("LASTED_TOP_POSTS", 'w') as f:
                    for each in now_top_posts:
                        f.write(str(each.id) + '\n')
                continue
            # 比较id是否相等
            different_posts = []
            for now in now_top_posts:
                if str(now.tid) not in last_top_posts:
                    different_posts.append(now)
            """if len(different_posts) == 0:
                self.have_update = False
                continue"""
            # 若更新，发送给主线程
            for post in different_posts:
                set_info(post)
                set_type(post)
                """if post_type == PostType.CARTOON and self.see_cartoon:
                    self.have_update = True
                if post_type == PostType.FICTION and self.see_fiction:
                    self.have_update = True
                if post_type == PostType.OTHER and self.see_others:
                   self.have_update = True
                else:
                    continue"""
                self.app.posts.append(post)
                self.app.update_post()
            # 更新文件
            while os.getcwd() != PATH:
                pass
            with open("LASTED_TOP_POSTS", 'w') as f:
                for each in now_top_posts:
                    f.write(str(each.tid) + '\n')
            sleep(self.sleeping_time * 60)
