import requests  #pip install requests
import parsel    #pip install parsel
import re
import pdfkit    #pip install pdfkit

#wkhtmltopdf下载地址：https://wkhtmltopdf.org/downloads.html

url="https://blog.csdn.net/qdpython/article/details/115627055"
html_str="""
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
	</head>
	<body>
		{article}
	</body>
</html>
"""
headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}
response=requests.get(url=url,headers=headers)

selector=parsel.Selector(response.text)
# content=selector.css("#content_views > div.toc > ul > li > ul > li > ul > li:nth-child(1) > a::attr(href)").get()
content=selector.xpath('//*[@id="content_views"]/div[1]/ul/li/ul/li/ul/li[1]/a/text()').get()
print(content)
#title=re.sub(r'[\\/:*?"<>|]',title) #文件名去特殊字符
content_html=html_str.format(article=content)
html_path='html\\1.html'
pdf_path='pdf\\1.pdf'
with open(html_path,mode='w',encoding='utf-8') as f:
    f.write(content_html)
print("正在保存")
config=pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
pdfkit.from_file(html_path,pdf_path,configuration=config)