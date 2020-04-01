import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from post import Post

# 驱动程序路径
CHROME_DRIVER_PATH = ".\\driver\\chromedriver"


# 获取置顶帖
def get_top_posts():
    # 设置隐藏
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # 获取网页
    driver = webdriver.Chrome(chrome_options=options, executable_path=CHROME_DRIVER_PATH)
    driver.get('https://tieba.baidu.com/f?kw=%E7%BB%88%E6%9E%81%E6%96%97%E7%BD%97&fr=index')
    # 将其转化为BeautifulSoup对象
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # 获取置顶帖并将其转换为Post类
    top_posts_tag = soup.find('li', class_="thread_top_list_folder")
    top_posts_tags = top_posts_tag.find_all('li', class_="j_thread_list thread_top j_thread_list clearfix")
    top_posts = []
    for each in top_posts_tags:
        top_posts.append(Post(int(each['data-tid']), True))
    return top_posts


# 获取信息
def get_info(post):
    assert isinstance(post, Post)
    # 设置隐藏
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # 获取网页
    driver = webdriver.Chrome(chrome_options=options, executable_path=CHROME_DRIVER_PATH)
    driver.get(post.url)
    # 转化为BeautifulSoup对象
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # 获取楼主昵称
    name_div_tag = soup.find('div', class_="d_author")
    name_a_tag = name_div_tag.find('a', attrs={"alog-group": "p_author"})
    name = name_a_tag.get_text()
    # 获取标题
    title_div_tag = soup.find('div', class_="core_title_wrap_bright clearfix", id="j_core_title_wrap")
    title = title_div_tag.h3["title"]
    post.lz = name
    post.title = title
    return title, name


# 获取文章
def get_text(url):
    # 设置隐藏
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # 获取网页
    driver = webdriver.Chrome(chrome_options=options, executable_path=CHROME_DRIVER_PATH)
    driver.get(url)
    # 转化为BeautifulSoup对象
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # 寻找标签
    text_tags = soup.find_all('div', class_="d_post_content j_d_post_content")
    text = ""
    for each in text_tags:
        text += ('\n'.join(each.get_text().split('　')))
    return text


# 获取图片
def get_images(url):
    # 设置隐藏
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # 获取网页
    driver = webdriver.Chrome(chrome_options=options, executable_path=CHROME_DRIVER_PATH)
    driver.get(url)
    # 转化为BeautifulSoup对象
    soup = BeautifulSoup(driver.page_source, "html.parser")
    image_tags = soup.find_all('img', class_="BDE_Image")
    image_urls = []
    for each in image_tags:
        image_urls.append(each["src"])
    images = []
    for each in image_urls:
        images.append(requests.get(each).content)
    return images
