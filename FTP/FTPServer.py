#coding:utf-8

import SocketServer
import os

class FTPServer(SocketServer.BaseRequestHandler):
	def handle(self):
		base_path = '/root'
		conn = self.request
		print 'connected...'

		while True:
			pre_data = conn.recv(1024)
			header,data = pre_data.split('/\\|/\\')
		
			if header == 'exit':
				break

			cmd,file_name,file_size = header.split('|')

			#上传文件路径拼接
			file_dir = os.path.join(base_path,file_name)
			f = file(file_dir,'wb')
			flag = True
			#已经接收文件的大小
			recv_size = 0;
			if len(data)> 0:
				recv_size += len(data)
				f.write(data)

			while flag:
				if int(file_size) > recv_size:#未上传完毕
					#最多接受1024,可能接收的小于1024
					data = conn.recv(1024)
					recv_size += len(data)
				else:#上传完毕则退出循环
					recv_size = 0
					flag = False
					continue

				#写入文件
				f.write(data)

			print 'upload successed.'
			f.close()

instance = SocketServer.ThreadingTCPServer(('127.0.0.1',8888),FTPServer)
instance.serve_forever()
