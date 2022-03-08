# wx_press_guide：vx公众号排版tool

## 运行环境
Python 3.5.2

[mistune](https://github.com/lepture/mistune)，
[premailer](https://github.com/peterbe/premailer)

运行以下命令安装：

```pip install -r requirements.txt```

## 使用方法
1. 使用Markdown写作，并保存为`.md`文件。
2. 将要转化的`.md`文件放入`source`目录中，运行main.py，
在`html_output`目录中得到同文件名的`.html`文件，
同时原始`.md`文件被移动到`history`目录中备份。
3. 用浏览器打开生成的`.html`文件，全选复制，粘贴到微信编辑器中。
4. 检查，预览，调整。

## 注意事项
1. 推送前请务必发送到手机预览仔细检查，作者不保证最终样式的绝对正确。
2. 如须引用图片，请先传到公众号后台，复制微信提供的链接。
3. 可通过订制style.css更改排版样式。

## 示例文档：
你可以使用此文档进行测试：

[example.md](https://github.com/insula1701/maxpress/blob/master/temp/example.md)