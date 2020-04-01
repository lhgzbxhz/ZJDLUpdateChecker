from enum import IntEnum
import threading
from time import sleep


# 帖子类型
class PostType(IntEnum):
    UNKNOWN = 0
    FICTION = 1
    CARTOON = 2
    OTHER = 3


# 帖子类
class Post:
    url = ''
    title = ''
    tid = 0
    lz = ''
    type = PostType.UNKNOWN
    see_lz = False

    def __init__(self, tid, see_lz):
        self.tid = tid
        self.see_lz = see_lz
        self.url = "https://tieba.baidu.com/p/%d?see_lz=%d" % (tid, int(see_lz))

    def __str__(self):
        return str(self.tid)

    __repr__ = __str__
