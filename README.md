# <p align = "center">Backup-Douban-Broadcast</P>
## <p align = "center">备份豆瓣广播</P>
------------------------------------------------------------------------------

**备份的文件为txt格式，如果打开文件内容为乱码，请把文件编码改为utf-8**
---------------------------------------------------------------------------

### <p align = "center">效果展示</P>
![douban](/rd/douban2.png)  


## 一、使用前提<br>

1、请下载 Backup Douban Broadcast.py 文件<br>
2、请确保电脑已安装[python3](https://www.python.org/downloads/release/python-365/)<br>
3、该脚本依赖两个python库，一是`LXML`，二是`requests`,（三是`BeautifuSoup`，如果用的是`Backup_Douban_Broadcast2.py`）  
请安装完python3后分别安装。<br>

		*目前只能这样用，后期有时间会打包成.exe*  

	
---------------------------------------------------------------------------
## 二、使用说明<br>

1.豆瓣处于登陆状态<br>
2.复制豆瓣下的`Uesr-Agent`和`Cookie`，请用火狐或chrome等浏览器用**F12**打开**开发者模式** 
![获取cookie,Uesr-Agent](/rd/text.png)  
3.更替脚本中的`Uesr-Agent`和`Cookie`  ![image](https://github.com/yekingyan/Backup-Douban-Broadcast/blob/master/rd/replace.png)   
4.运行并输入要备份的页数



---------------------------------------------------------------------------
### 备注
	**Backup Douban Broadcast.py**的功能  
	~~目前只能备份时间与文字，~~  
	~~没有广播的电影和书籍，~~  
	没有点赞和评论内容。  


	**Backup_Douban_Broadcast2.py**的功能
	~~目前只能备份时间与文字，~~
	~~没有广播的电影和书籍，~~ 只技电影、音乐、豆列、广播内容了
	还是没有点赞和评论内容。（主要是作者豆瓣没人点赞、评论😅:see_no_evil:）


Backup Douban Broadcast.py`与`Backup_Douban_Broadcast2.py`的主要具别是前者是用xlml解析的，后者用的是BeautifulSoup加上正则表达式，理论上前者会快一点，但快是没有用的，因为太快豆瓣会锁号（不是封号），因些两个脚本我都加了每页2秒暂停时间。
`Backup_Douban_Broadcast2.py`太长写的得不好，看起来乱，后期会加入类的方法作简化，让思路看起来清晰一点。但单纯使用的话不影响，`Backup_Douban_Broadcast2.py`的教程和`Backup Douban Broadcast.py`基本一样（需加多一个BeautifuSoup库），只是操作上少了一步：输入页码，默认备份全部广播（除非广播超出1000页）。  
   
   GitHub有时会读取不出图片，我在CSDN上有较为详细一点的教程，但是更新的代码还是需要在GitHub下载。[下载、备份豆瓣广播 ](https://blog.csdn.net/weixin_42105977/article/details/80384101)