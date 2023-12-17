# cstnetdown/bypop.py

import os
import re
import zmail

def get_time(mail):
	datetime = mail["date"]
	if datetime is None:
		return "00000000-000000"
	else:
		return datetime.strftime("%Y%m%d_%H%M%S")

def get_title(mail):
	title_raw = mail["subject"]
	if title_raw is None:
		return ""
	title_1 = re.sub(r'[<>:"/\\|?*]', '_', title_raw)
	title_2 = re.sub(r"[\r\n\t]", ' ', title_1)
	title_3 = re.sub(r"  +", ' ', title_2)
	return title_3.strip()

def summarize(mail):
	return f"[{get_time(mail)}] {get_title(mail)}.eml"

def save_mail(mail, directory):
	file_name = summarize(mail)
	file_path = os.path.join(directory, file_name)
	if os.path.isfile(file_path):
		j = 1
		while True:
			file_path_new = f"{file_path[:-4]}_{j}.eml"
			if not os.path.isfile(file_path_new):
				break
			j += 1
		file_path = file_path_new
	zmail.save(mail, file_path)
	return file_path

def bypop(account, password, directory, begin=1, end=-1):
	server = zmail.server(account, password, 
		smtp_host="mail.cstnet.cn", smtp_port=994, 
		pop_host="mail.cstnet.cn", pop_port=995, pop_ssl=True)
	count, _ = server.stat()
	if end < 0 or end > count:
		end = count
	failed_indices = []
	for i in range(begin, end+1):
		try:
			mail = server.get_mail(i)
			file_path = save_mail(mail, directory)
			print(i, file_path)
		except Exception as e:
			print(i, e)
			failed_indices.append(i)
	print("Failed:", failed_indices)
