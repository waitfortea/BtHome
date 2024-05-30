@echo off
::获取当前文件所在的目录的绝对路径
set "thispath=%~dp0"
::删除之后的路径分隔符号“\”
set "thispath=%thispath:~0,-1%"
echo 当前文件所在的目录的绝对路径:%thispath%
::读取path环境变量到自定义变量中
set mypath=%path%
::把path环境变量写入临时文件中,以备后续使用findstr命令进行查找
echo %mypath% > temp.txt
::在临时文件中查找有没有当前路径
find "%thispath%" temp.txt
::如果查找到则fin命令返回0,如果没有找到find命令返回1
if %errorlevel% == 0 (
	echo path环境变量中 已经包含了 当前路径%thispath%
	echo 程序返回码:%errorlevel%
) else (
	echo path环境变量中 没有包含   当前路径%thispath%
	echo 程序返回码:%errorlevel%
	::追加当前文件所在目录的路径到path环境变量中
	setx /m "path" "%thispath%;%path%"
)	
::删除临时文件
del temp.txt
pause