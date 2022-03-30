# Markdown2VX Press Guide：vx公众号排版tool

## 直接使用

下载后运行md2vx.exe即可。

## 运行环境

Python 3.9.6

[mistune](https://github.com/lepture/mistune)，
[premailer](https://github.com/peterbe/premailer)，
PyQt5

运行以下命令安装：

``pip install -r requirements.txt``

## 使用方法

1. 使用Markdown写作，并保存为 `.md`文件；
2. 运行UI.py；
3. 点击 `Choose a Markdown File`，选择写好的 `.md`文件，该 `.md`文件此时自动保存在 `Source `文件夹下；
4. 点击 `Execute File Conversion` 执行转换；
5. 在 `html_output`目录中得到同文件名的 `.html`文件，同时原始 `.md`文件被移动到 `history`目录中备份；
6. 用浏览器打开生成的 `.html`文件，全选复制，粘贴到微信编辑器中。
7. 检查，预览，调整。

## 注意事项

1. 推送前请务必发送到手机预览仔细检查，作者不保证最终样式的绝对正确。
2. 如须引用图片，请先传到公众号后台，复制微信提供的链接。
3. 可通过订制style.css更改排版样式。

## 示例文档：

你可以使用此文档进行测试：

[example.md](https://github.com/insula1701/maxpress/blob/master/temp/example.md)
