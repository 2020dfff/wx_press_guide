from mistune import Markdown
import premailer
import os


def pack_html(html, style='default_style.css'):
    head = """<!DOCTYPE html><html lang="zh-cn">
          <head>
          <meta charset="UTF-8">
          <title>output</title>
          <link rel="stylesheet" type="text/css" href="{style}">
          </head>
          <body>\n""".format(style=style)

    bottom = """\n</body>\n</html>"""
    return head + html + bottom


def convert_all(src='source', dst='html_output', style='default_style.css'):
    for file in os.listdir(src):

        if file.endswith('.md'):
            with open('{src}/{fn}'.format(src=src, fn=file), 'r', encoding='utf-8') as mdfile:
                mdstr = mdfile.read()

            md = Markdown()
            raw_html = md(mdstr)
            result = premailer.transform(pack_html(raw_html, style))

            with open('{dst}/{fn}.html'.format(dst=dst, fn=file[:-3]),
                      'w', encoding='utf-8') as htmlfile:
                htmlfile.write(result)
            os.rename('{src}/{fn}'.format(src=src, fn=file), 'history/{fn}'.format(fn=file))
            print('成功：转换后的.html文件保存在html_output文件夹中')
            print('在history文件中查看转换完毕的.md源文件')


if __name__ == '__main__':
    try:
        convert_all(src='source', dst='html_output', style='default_style.css')
    except:
        input('错误：运行前请将所有要转换的.md文件放入source文件夹中'
              '按回车键结束程序：')



