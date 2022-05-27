# coding=utf-8
import os
import shutil

import pdfkit
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileMerger
from PyPDF4 import PdfFileReader,PdfFileWriter


base_url = 'http://python3-cookbook.readthedocs.io/zh_CN/latest/'
book_name = ''
chapter_info = []

#获取目录及对应网址
def parse_title_and_url(html):
    """
    解析全部章节的标题和url
    :param html: 需要解析的网页内容
    :return None
    """
    soup = BeautifulSoup(html, 'html.parser')

    # 获取书名
    book_name = soup.find('div', class_='wy-side-nav-search').a.text
    menu = soup.find_all('div', class_='section')
    chapters = menu[0].div.ul.find_all('li', class_='toctree-l1')
    for chapter in chapters:
        info = {}
        # 获取一级标题和url
        # 标题中含有'/'和'*'会保存失败
        info['title'] = chapter.a.text.replace('/', '').replace('*', '')
        info['url'] = base_url + chapter.a.get('href')
        info['child_chapters'] = []

        # 获取二级标题和url
        if chapter.ul is not None:
            child_chapters = chapter.ul.find_all('li')
            for child in child_chapters:
                url = child.a.get('href')
                # 如果在url中存在'#'，则此url为页面内链接，不会跳转到其他页面
                # 所以不需要保存
                if '#' not in url:
                    info['child_chapters'].append({
                        'title': child.a.text.replace('/', '').replace('*', ''),
                        'url': base_url + child.a.get('href'),
                    })
        # print(info)

        chapter_info.append(info)



#获取章节内容
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""
def get_one_page(url):
    return requests.get(url).content.decode()

def get_content(url):
    """
    解析URL，获取需要的html内容
    :param url: 目标网址
    :return: html
    """
    html = get_one_page(url)

    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', attrs={'itemprop': 'articleBody'})
    html = html_template.format(content=content)
    return html

#保存PDF
def save_pdf(html, filename):
    """
    把所有html文件保存到pdf文件
    :param html:  html内容
    :param file_name: pdf文件名
    :return:
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(html, filename, options=options,configuration=config)

def parse_html_to_pdf():
    """
    解析URL，获取html，保存成pdf文件
    :return: None
    """
    try:
        for chapter in chapter_info:
            ctitle = chapter['title']
            url = chapter['url']
            # 文件夹不存在则创建（多级目录）
            dir_name = os.path.join(os.path.dirname(__file__), 'gen', ctitle)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            html = get_content(url)

            pdf_path = os.path.join(dir_name, ctitle + '.pdf')
            save_pdf(html, os.path.join(dir_name, ctitle + '.pdf'))

            children = chapter['child_chapters']
            if children:
                for child in children:
                    html = get_content(child['url'])
                    pdf_path = os.path.join(dir_name, child['title'] + '.pdf')
                    save_pdf(html, pdf_path)


    except Exception as e:
        print(e)

#合并PDF
from PyPDF2 import PdfFileReader, PdfFileWriter


def merge_pdf(infnList, outfn):
    """
    合并pdf
    :param infnList: 要合并的PDF文件路径列表
    :param outfn: 保存的PDF文件名
    :return: None
    """
    pagenum = 0
    pdf_output = PdfFileWriter()


    for pdf in infnList:
        # 先合并一级目录的内容
        first_level_title = pdf['title']
        dir_name = os.path.join(os.path.dirname(
            __file__), 'gen', first_level_title)
        padf_path = os.path.join(dir_name, first_level_title + '.pdf')

        pdf_input = PdfFileReader(open(padf_path, 'rb'))
        # 获取 pdf 共用多少页
        page_count = pdf_input.getNumPages()
        for i in range(page_count):
            pdf_output.addPage(pdf_input.getPage(i))

        # 添加书签
        parent_bookmark = pdf_output.addBookmark(
            first_level_title, pagenum=pagenum)

        # 页数增加
        pagenum += page_count

        # 存在子章节
        if pdf['child_chapters']:
            for child in pdf['child_chapters']:
                second_level_title = child['title']
                padf_path = os.path.join(dir_name, second_level_title + '.pdf')

                pdf_input = PdfFileReader(open(padf_path, 'rb'))
                # 获取 pdf 共用多少页
                page_count = pdf_input.getNumPages()
                for i in range(page_count):
                    pdf_output.addPage(pdf_input.getPage(i))

                # 添加书签
                pdf_output.addBookmark(
                    second_level_title, pagenum=pagenum, parent=parent_bookmark)
                # 增加页数
                pagenum += page_count

    # 合并
    pdf_output.write(open(outfn, 'wb'))
    # 删除所有章节文件
    shutil.rmtree(os.path.join(os.path.dirname(__file__), 'gen'))



if __name__=="__main__":
    # html=requests.get(base_url).content.decode()
    # parse_title_and_url(html)
    # parse_html_to_pdf()

    DIR = "gen/"
    OUTPUT = "output.pdf"
    merger = PdfFileMerger(strict=False)
    file_list = filter(lambda f: f.endswith('.pdf'),merger)


    for f_name in file_list:
        f = open(os.path.join(DIR, f_name), "rb")
    merger.append(f)

    output = open(OUTPUT, "wb")
    merger.write(output)



