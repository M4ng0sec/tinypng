#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import os.path
import click
import tinify
from concurrent.futures import ThreadPoolExecutor
tinify.key = "LpQYXSLJE6r5ruBJZ288cLiOunZNcPVj"		# API KEY
version = "1.0.2"				# 版本
tinyPath="tinypng"				# 要保存的文件夹
pool = ThreadPoolExecutor(max_workers=10) # 创建一个线程池
count=[0]
# 压缩的核心
def compress_core(inputFile, outputFile, img_width):
	count[0]+=1	
	print "开始压缩第"+str(count[0])+"个 "+inputFile.encode("utf8")
	source = tinify.from_file(inputFile)
	if img_width is not -1:
		resized = source.resize(method = "scale", width  = img_width)
		resized.to_file(outputFile)
	else:
		source.to_file(outputFile)
	print "成功压缩第"+str(count[0])+"个 "+outputFile.encode("utf8")+"\n"
	
	
# 压缩一个文件夹下的图片
def compress_path(path, width):
	#print "compress_path-------------------------------------"
	# myroot=path
	# if len(myroot)==0:
	# 	myroot =path
	# print myroot
	if not os.path.isdir(path):
		print "这不是一个文件夹，请输入文件夹的正确路径!"
		return
	else:
		fromFilePath = path 			# 源路径
		toFilePath = path;#+"/tiny" 		# 输出路径
		for root, dirs, files in os.walk(fromFilePath):
			# print "root = %s" %root
			# print "dirs = %s" %dirs
			# print "files= %s" %files
			if len(dirs)>0:
				for f in dirs:
					if(os.path.isdir(root+"/"+f)):
						compress_path(root+"/"+f,width)				   	
			for name in files:
				#print name
				   fileName, fileSuffix = os.path.splitext(name)
				   if fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg':
						toFullPath = toFilePath + root[len(fromFilePath):]
						toFullName = toFullPath + '/' + name
						outputFileDir= os.getcwd()+"/"+tinyPath+(root+"/"+name).replace(os.getcwd(),"").replace(name,"")
						if os.path.exists(outputFileDir):
							pass
						else:
							os.makedirs(outputFileDir)
						future = pool.submit(compress_core(root + '/' + name,(outputFileDir+name).encode('utf8'),width))
			break									# 仅遍历当前目录

# 仅压缩指定文件
def compress_file(inputFile, width):
	print "compress_file-------------------------------------"
	if not os.path.isfile(inputFile):
		print "这不是一个文件，请输入文件的正确路径!"
		return
	print "file = %s" %inputFile
	dirname  = os.path.dirname(inputFile)
	basename = os.path.basename(inputFile)
	outputFileDir=os.path.abspath(inputFile).replace(basename,"")+tinyPath
	print outputFileDir
	fileName, fileSuffix = os.path.splitext(basename)
	if fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg':
		if os.path.exists(outputFileDir):
			pass
		else:
			os.makedirs(outputFileDir)
		compress_core(inputFile, outputFileDir+"/"+basename, width)
	else:
		print "不支持该文件类型!"

@click.command()
@click.option('-f', "--file",  type=str,  default=None,  help="单个文件压缩")
@click.option('-d', "--dir",   type=str,  default=None,  help="被压缩的文件夹")
@click.option('-w', "--width", type=int,  default=-1,    help="图片宽度，默认不变")
def run(file, dir, width):
	print ("GcsSloop TinyPng V%s" %(version))
	if file is not None:
		compress_file(file, width)				# 仅压缩一个文件
		pass
	elif dir is not None:
		compress_path(dir, width)				# 压缩指定目录下的文件
		pass
	else:
		compress_path(os.getcwd(), width)		# 压缩当前目录下的文件
	print "结束!"

if __name__ == "__main__":
    run()

