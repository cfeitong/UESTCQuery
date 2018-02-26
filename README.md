# 郫县男子职业技术学校查询工具
在命令行中实现包括但不限于对信息门户、图书馆等学生生活相关信息的查询

## 具体功能
### 查询信息门户
- 查询指定学期的考试时间
- 查询指定学期的考试成绩
- 查询指定学期、指定周的课表

## 更新日志
> 2018-01-09 添加查询成绩功能  
> 2018-02-26 添加查询课表功能

## TODO
- [x] 查询课表
- [ ] 查询全校的考试安排
- [ ] 查询空闲教室

## 使用方法
1. 安装相关依赖（安装方法在下方）
2. 运行**build.py**构建exe文件，文件保存在bin文件夹下 
3. 打开cmd或powershell，将目录切换到bin文件夹
4. 使用相关命令

### 命令示例
查询当前学期考试信息
```cmd
./uestc_query.exe -e uesrname password # username为学号，password为信息门户密码 
```
查询指定学期成绩信息
```cmd
./uestc_query.exe -g username password --semester 2015-2016-2 #查询2015-2016年第二学期的成绩
```

### 命令格式
```cmd
./uestc_query.exe params username password other_params 
```
params列表  
"-e", "--exam" : 查询考试安排  
"-g", "--grade": 查询成绩  
"-c", "--curriculum": 查询课表

other_params列表  
"-s", "--semester" : 查询某个学期相关信息 如"-s 2015-2016-1"表示查询2015-2016第一个学期的相关信息
"-w", "--week": 指定第几周，仅在查询课表时有用
 
 ## 开发方法
 - clone工程
 - 使用pip安装requirements.txt中的依赖项
 ```cmd
 pip install -r requirements.txt
 ```
 
 ### 目录结构 
 \-UESTCQuery/  
 \-\-\-constant/        存放常用的一些常量  
 \-\-\-model/  
 \-\-\-query/           存放各种查询py文件    
 \-\-\-config.py        配置文件  
 \-\-\-login.py         登录信息门户代码文件  
 \-\-\-uestc_query.py   主程序文件  
 \-\-\-utils.py         常用的一些工具函数  
 \-\-build.py           构建程序，运行可以自动编译成exe文件到bin/目录（需提前安装依赖  
 \-requirements.txt     pip依赖文件
 
 ## 联系方式
 邮箱：kangyan62406@126.com
 
 欢迎提issue，欢迎star和fork！
