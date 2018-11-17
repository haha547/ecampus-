# ecampus-

## 前言 
為了解決教學平台無法自動適屏各個裝置，我們決定重新改良教學平台的種種缺點！
<br>
但因為我們是以爬蟲方式爬取教學平台的資訊，也就是說我們的產品還是基於**教學平台**。  
我們主要想實現快速、直覺的操作，拒絕繁瑣以及煩人的跳出視窗！

使用工具、語言
------------
#### 後端
* Python 3
  * BeautifulSoup
  * requests
* Django
* Sqlite 3
#### 前端
* Bootstrap 4
* Javascript
* Html + Css

已實現功能
---------
可以用學號登入到教學平台，並且列出所有課程。

11/13新增 點進課程可顯示公告。

預期實現目標
-----------
1. 在課程表顯示作業公告

2. 爬取課程中所需資訊(諸如: 作業、文件...等)

#### Course List
<pre>
├── Slidebar  
|  ├── Home  
|  |   ├──All HW
|  |   ├──All BBS   
|  |   └──All DOC
|  |
|  ├── Course
|  |   ├── #course1  
|  |       ├──HW
|  |       ├──BBS
|  |       └──DOC
|  |   ├── #course2  
|  |       ├──HW
|  |       ├──BBS
|  |       └──DOC
|  |   ├── #course3  
|  |       ├──HW
|  |       ├──BBS
|  |       └──DOC
|  |   └── #course4  
|  |       ├──HW
|  |       ├──BBS
|  |       └──DOC
|  ├── User  
|  |   ├──Profile
|  |   └──Sign out 
|  | 
|  ├── FAQ  
|  | 
|  └── Contact us / Issue Report 
</pre>

產品特色
-----------

* 響應式設計 

* 移除不常用元件

* 更加直覺的介面

* 更安全的加密法

徵求小夥伴
---------
歡迎各位與我們做中學，我們不是很厲害，但是有一些想法想實現。  
您只要有一顆熱誠的心，我們可以一步一步建立這個專案！






