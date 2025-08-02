from requests_html import HTMLSession
import socket
import subprocess
import platform
from base64 import b64encode
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Router(object):
	 
	def __init__(self,ip=None,username="telecomadmin",password="admintelecom",port=80,scheme="https"):
		
		self.scheme = scheme
		self.session=HTMLSession()
		self.ip = ip
		self.port = port
		self.username = username
		self.username = password
		self.headers={
	        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0",
	        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	        "Accept-Language": "en-US,en;q=0.5",
	        "Content-Type": "application/x-www-form-urlencoded",
	        "Upgrade-Insecure-Requests": "1",
	        "Sec-Fetch-Dest": "document",
	        "Sec-Fetch-Mode": "navigate",
	        "Sec-Fetch-Site": "same-origin",
	        "Sec-Fetch-User": "?1",
	        "Priority": "u=0, i",
	        "Cookie": "Cookie=body:Language:english:id=-1",
	    }
		self.data={
			"UserName": username,
			"PassWord": b64encode(password.encode("utf8")).decode("utf8"),
			"x.X_HW_Token": ""
		}


	def login(self):

		if self.is_host_up(self.ip):

			if self.is_port_open(self.ip,self.port)==True:
				
				self.set_token()
				 
				respone = self.session.post(f"{self.scheme}://{self.ip}:{self.port}/login.cgi",headers=self.headers,data=self.data,verify=False)
				

				if "var pageName = 'index.asp';" in respone.html.html:
					return True,"We Have Loged in"
				else:
					return False,f"Some Thing Worng html respone is {respone.html.html}"


			else:
				return False,"the port is not open"
		else:
			return False,"the host is not up"



	def set_token(self):

		respone = self.session.get(f"{self.scheme}://{self.ip}:{self.port}",headers=self.headers,verify=False)
		 
		self.data['x.X_HW_Token']=respone.html.search("function GetRandCnt() { return '{}'; }")[0]

	def is_port_open(self,host,port,timeout=2):
	     
	    try:
	        with socket.create_connection((host, port), timeout=timeout):
	            return True
	    except (socket.timeout, socket.error):
	        return False


	def is_host_up(self,host, timeout_ms=500):
	    
	    system = platform.system().lower()
	    is_windows = system == "windows"

	    count_flag = "-n" if is_windows else "-c"
	    timeout_flag = "-w" if is_windows else "-W"
	    timeout_value = str(timeout_ms if is_windows else int(timeout_ms / 1000))

	    cmd = ["ping", count_flag, "1", timeout_flag, timeout_value, host]

	    kwargs = {
	        "stdout": subprocess.DEVNULL,
	        "stderr": subprocess.DEVNULL
	    }

	    if is_windows:
	        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

	    try:
	        return subprocess.run(cmd, **kwargs).returncode == 0
	    except Exception:
	        return False
 