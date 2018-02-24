"""
自动构建exe程序
需要实现安装pyinstaller
构建后的程序存放在./bin
"""
import os

os.system("pyinstaller ./UESTCQuery/uestc_query.py -F --hidden-import UESTCQuery --clean --distpath ./bin")

