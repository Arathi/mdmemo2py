# -*- coding: utf-8 -*-
import yaml
from os import mkdir,listdir,makedirs
from os.path import isfile, join, split, realpath, exists
import re
import markdown


pattern = re.compile(r'(\d{4}-\d{2}-\d{2})-(.*?)(\.[^\.]*)')
global_config = dict()


# 读取配置文件 _config.yml
def configure():
    config_file = open("_config.yml")
    global_config = yaml.load(config_file)


def mkdir_if_not_exist(dir_name):
    if exists(dir_name)==False:
        makedirs(dir_name)


# 列出_posts目录下文件名符合规则的文件
# yyyy-mm-dd-post-name.*
def get_articles():
    files = [ f for f in listdir("_posts") if isfile(join("_posts", f)) ]
    article_list = list()
    for f in files:
        # TODO 检查文件名是否符合规则
        m = re.match(pattern, f)
        date_and_name = (m.group(0), m.group(1), m.group(2), m.group(3))
        article_list.append(date_and_name)
    return article_list


def parse_article(date_and_name):
    filename = date_and_name[0]
    post_date = date_and_name[1]
    title = date_and_name[2]
    extname = date_and_name[3]
    print "parsing %s ..." % filename

    # 分离配置项与markdown
    config_content = ''  # 以---开始，以---结束
    markdown_content = ''  # 第二个---后面全是md

    file = open('_posts/'+filename)
    spliter_counter = 0
    reading_config = False
    for line in file:
        line = line.strip()
        if line=='---':
            spliter_counter += 1
            if spliter_counter == 1:
                # 开始读取配置项
                reading_config = True
                continue
            elif spliter_counter == 2:
                # 读取配置项结束
                reading_config = False
                continue
        if reading_config:
            config_content += line + '\n'
        else:
            markdown_content += line + '\n'
    # print len(config_content)
    # print len(markdown_content)

    # 解析yaml与
    # yaml_content = config_content
    config = yaml.load(config_content)
    # print config_content
    # print type(markdown_content)  # isinstance(markdown_content, unicode)
    markdown_content = markdown_content.decode('utf-8')
    html = markdown.markdown(markdown_content)  # 解析markdown_content

    # print type(config['categories'])

    categories = list()
    if isinstance(config['categories'], str):
        categories.append(config['categories'])
    elif isinstance(config['categories'], list):
        categories += config['categories']

    # title = ''  # 从文件名中分离
    # print type(config_content)
    return categories, title, html


def write_article_cache(article_dir, html):
    mkdir_if_not_exist(article_dir)
    filepath = article_dir + "/index.html"
    print 'writing html to %s ...' % filepath
    # 生成index.html文件
    # 将html写入index.html
    with open(filepath, 'w') as f:
        f.write(html.encode('utf-8'))


def create_article_cache(categories, title, html):
    # base_dir = split(realpath(__file__))[0]
    # site_dir = base_dir + "/_site"
    if categories != None and len(categories)>0:
        for category in categories:
            # 生成分类目录
            category_dir = '_site/' + category
            mkdir_if_not_exist(category_dir)
            # 生成文章目录
            article_dir = category_dir + '/' + title
            write_article_cache(article_dir, html)
    else:
        article_dir = '_site/' + title
        write_article_cache(article_dir, html)


if __name__ == "__main__":
    configure()
    mkdir_if_not_exist('_site')
    article_list = get_articles()
    for article in article_list:
        # 分类，标题，解析后的html
        categories, title, html = parse_article(article)
        create_article_cache(categories, title, html)
