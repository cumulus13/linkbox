#!/usr/bin/env python

from __future__ import print_function

import os, sys

import requests

from bs4 import BeautifulSoup as bs
from make_colors import make_colors
from pydebugger.debug import debug
from configset import configset
import progressbar
import traceback
import time
import re
import inspect
try:
	from pause import pause
except:
	def pause(*args, **kwargs):
		return None
from pprint import pprint
import clipboard
from unidecode import unidecode
import bitmath
from datetime import datetime
import argparse
try:
	from . import get_version
except:
	try:
		import get_version
	except:
		class get_version(object):

			def __init__(self): pass

			@classmethod
			def get(self):
				return "0.1"

if sys.version_info.major == 3:
	raw_input = input
	from urllib.parse import unquote, quote, urlparse
else:
	from urllib import unquote, quote
	from urlparse import urlparse


class LinkToBox(object):

	CONFIG = configset()

	URL = CONFIG.get_config('setting', 'url', "https://www.linkbox.to/")
	SESS = requests.Session()
	prefix = {'{variables.task} >> {variables.subtask}'}
	variables = {'task': '---', 'subtask': '---'}
	BAR = progressbar.ProgressBar(prefix = prefix, variables = variables, max_value = 100, max_error = False)
	MAX_ERROR = CONFIG.get_config('error', 'max_try', '10')

	HEADERS = {
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Linux"',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'sec-fetch-site': 'cross-site',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-user': '?1',
		'sec-fetch-dest': 'document',
		'accept-encoding': 'gzip, deflate',
		'accept-language': 'en-US,en;q=0.9,id;q=0.8',

	}


	SESS.headers.update(HEADERS)

	def __init__(self, url = None):
		self.URL = url or self.URL

	@classmethod
	def valid(self, soup, func, args):
		debug(args = args)
		if isinstance(args, str):
			args = (args, {})
		else:
			if len(args) == 1:
				args = (args[0], {})

		n_try = 0
		debug(args = args)
		try:
			data = getattr(soup, func)(*args)
			if not data:
				print(make_colors("error:", 'lw', 'r') + " " + make_colors("Failed to get:", 'lr') + " " + make_colors("`" + " ".join([str(i) for i in args]) + "`", 'ly'))
				if __name__ == '__main__': sys.exit(0)
				else: return False
			return data
		except Exception as e:
			debug(inspect_stack = inspect.stack())
			print(make_colors("error:", 'lw', 'r') + " " + make_colors(e, 'ly'))

			if __name__ == '__main__': sys.exit()
			else: return False

	@classmethod
	def connect(self, url = None, method='get', n_try = 10, **kwargs):
		url = url or self.URL
		debug(url = url)
		req = False
		while 1:
			try:
				# content = self.SESS.get(self.URL).content
				req = getattr(self.SESS, method)(url, **kwargs)
				break
			except Exception as e:
				task = make_colors("error", 'lw', 'r')
				subtask = make_colors(e, 'ly') + " "
				if not n_try == self.MAX_ERROR:
					n+=1
					self.BAR.update(n, task = task, subtask = subtask)
					time.sleep(0.3)
				else:
					self.BAR.finish()
					print(make_colors("error:", 'lw', 'r') + " " + make_colors(e, 'ly'))
					# sys.exit(make_colors(traceback.format_exc(), 'r', 'lw'))
					if __name__ == '__main__': sys.exit(make_colors(traceback.format_exc(), 'r', 'lw'))
					else: return False
		return req

	@classmethod
	def download_linux(self, url, download_path=os.getcwd(), saveas=None, cookies = {}, downloader = 'wget', check_file = True):
		'''
			downloader: aria2c, wget, uget, persepolis
		'''

		if saveas:
			saveas = re.sub("\.\.", ".", saveas)
		if not download_path or not os.path.isdir(download_path):
			if self.CONFIG.get_config('DOWNLOAD', 'path', os.getcwd()):
				download_path = self.CONFIG.get_config('DOWNLOAD', 'path')
		if not download_path:
			download_path = os.getcwd()
		print(make_colors("DOWNLOAD_PATH (linux):", 'lw', 'bl') + " " + make_colors(download_path, 'b', 'ly'))
		print(make_colors("DOWNLOAD LINK [direct]:", 'b', 'lc') + " " + make_colors(url, 'b', 'ly'))
		if sys.version_info.major == 3:
			aria2c = os.popen("aria2c")
			wget = os.popen("wget")
			persepolis = os.popen("persepolis --help")
		else:
			aria2c = os.popen3("aria2c")
			wget = os.popen3("wget")
			persepolis = os.popen3("persepolis --help")

		if downloader == 'aria2c' and not re.findall("not found\n", aria2c[2].readlines()[0]):
			if saveas:
				saveas = '-o "{0}"'.format(saveas.encode('utf-8', errors = 'ignore'))
			cmd = 'aria2c -c -d "{0}" "{1}" {2} --file-allocation=none'.format(os.path.abspath(download_path), url, saveas)
			os.system(cmd)
			self.logger(cmd)
		elif downloader == 'wget':
			if sys.version_info.major == 2:
				if re.findall("not found\n", wget[2].readlines()[0]):
					print(make_colors("Download Failed !", 'lw', 'r'))
					return False
			filename = ''
			if saveas:
				if sys.version_info.major == 3:
					filename = os.path.join(os.path.abspath(download_path), saveas)
					saveas = ' -O "{}"'.format(os.path.join(os.path.abspath(download_path), saveas))
				else:
					filename = os.path.join(os.path.abspath(download_path), saveas.decode('utf-8', errors = 'ignore'))
					saveas = ' -O "{}"'.format(os.path.join(os.path.abspath(download_path), saveas.decode('utf-8', errors = 'ignore')))
			else:
				saveas = '-P "{0}"'.format(os.path.abspath(download_path))
				filename = os.path.join(os.path.abspath(download_path), os.path.basename(url))
			headers = ''
			header = ""
			if cookies:
				for i in cookies: header +=str(i) + "= " + cookies.get(i) + "; "
				headers = ' --header="Cookie: ' + header[:-2] + '"' + ' --header="User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36" ' + '--header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" --header="Sec-Fetch-Site: same-origin" --header="Accept-Encoding: gzip, deflate, br" --header="Connection: keep-alive" --header="Upgrade-Insecure-Requests: 1" --header="Sec-Fetch-Mode: navigate" --header="Sec-Fetch-User: ?1" --header="Sec-Fetch-Dest: document"'
			cmd = 'wget -c "' + url + '" {}'.format(unidecode(saveas)) + headers
			if 'racaty' in url:
				cmd+= ' --no-check-certificate'
			print(make_colors("CMD:", 'lw', 'lr') + " " + make_colors(cmd, 'lw', 'r'))
			os.system(cmd)
			self.logger(cmd)
			if self.CONFIG.get_config('policy', 'size'):
				size = ''
				try:
					size = bitmath.parse_string_unsafe(self.CONFIG.get_config('policy', 'size'))
				except ValueError:
					pass
				if check_file:
					if size and not bitmath.getsize(filename).MB.value > size.value:
						print(make_colors("REMOVE FILE", 'lw', 'r') + " [" + make_colors(bitmath.getsize(filename).kB) + "]: " + make_colors(filename, 'y') + " ...")
						os.remove(filename)

		elif downloader == 'persepolis'  and not re.findall("not found\n", persepolis[2].readlines()[0]):
			cmd = 'persepolis --link "{0}"'.format(url)
			os.system(cmd)
			self.logger(cmd)
		else:
			try:
				from pywget import wget as d
				d.download(url, download_path, saveas.decode('utf-8', errors = 'ignore'))
				self.logger("download: {} --> {}".format(url, os.path.join(download_path, saveas.decode('utf-8', errors = 'ignore'))))
			except:
				print(make_colors("Can't Download this file !, no Downloader supported !", 'lw', 'lr', ['blink']))
				clipboard.copy(url)
				self.logger("download: copy '{}' --> clipboard".format(url), "ERROR")

	@classmethod
	def logger(self, message, status="INFO"):
	    logfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.splitext(os.path.basename(os.path.realpath(__file__)))[0] + ".log")
	    if not os.path.isfile(logfile):
	        lf = open(logfile, 'wb')
	        lf.close()
	    real_size = bitmath.getsize(logfile).kB.value
	    max_size = self.CONFIG.get_config("LOG", 'max_size')
	    debug(max_size = max_size)
	    if max_size:
	        debug(is_max_size = True)
	        try:
	            max_size = bitmath.parse_string_unsafe(max_size).kB.value
	        except:
	            max_size = 0
	        if real_size > max_size:
	            try:
	                os.remove(logfile)
	            except:
	                print("ERROR: [remove logfile]:", traceback.format_exc())
	            try:
	                lf = open(logfile, 'wb')
	                lf.close()
	            except:
	                print("ERROR: [renew logfile]:", traceback.format_exc())


	    str_format = datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S.%f") + " - [{}] {}".format(status, message) + "\n"
	    with open(logfile, 'ab') as ff:
	        if sys.version_info.major == 3:
	            ff.write(bytes(str_format, encoding='utf-8'))
	        else:
	            ff.write(str_format)

	@classmethod
	def home(self, url = None):

		if url:
			if not 'linkbox.to' in url:
				url = self.URL + url.replace("/", '')

		data = []
		debug(self_URL = self.URL)
		debug(url = url)
		content = self.connect(url, timeout=10, headers = self.HEADERS).content
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'result.html'), 'w') as cf:
			cf.write(content)

		if not content:
			print(make_colors("Failed to get data !", 'lw', 'r'))
			if __name__ == '__main__': sys.exit()
			else: return False

		#"lxml", "lxml-xml", "html.parser", or "html5lib" or it may be the type of markup to be used ("html", "html5", "xml")
		b = bs(content, features='lxml-xml')
		plyr__video_wrapper = self.valid(b, 'find', ('div', {'class':'plyr__video-wrapper'}))

		debug(plyr__video_wrapper = plyr__video_wrapper)
		pause()

		for i in left_cards:
			add = {}
			title = self.valid(i, 'find', ('h1', {'class':'movies'}))
			# _title = title.find('img')
			_title = self.valid(title, 'find', ('img')).get('alt').replace(' icon', '')
			debug(title = _title)
			title_url = self.valid(title, 'find', ('a')).get('href')
			debug(title_url = title_url)
			title_rss = self.valid(title, 'find', ('a', {'title':re.compile('RSS')})).get('href')
			debug(title_rss = title_rss)

			grey_bar3 = self.valid(i, 'find_all', ('div', {'class':('grey_bar3')}))
			debug(grey_bar3 = grey_bar3)
	
	@classmethod
	def generator(self, id, download_path = None, saveas = None):
		# https://www.linkbox.to/api/file/detail?itemId=fp3btk0000gz&needUser=1&needTpInfo=1&token=
		params = {}
		if not 'linkbox' in id:
			params = {
				'itemId':id,
				'needUser':'1',
				'needTpInfo':'1',
				'token':''
			}
			url = self.URL + 'api/file/detail'
		else:
			if len(list(filter(lambda k: k in ('api', 'file', 'detail', 'linkbox', 'itemId', 'needUser', 'needTpInfo', 'token'), id))) == 8:
				url = id
			else:
				print(make_colors("URL NOT valid !", 'lw', 'r'))
				return False
		debug(url = url)
		debug(params = params)
		content = self.connect(url, params = params, headers = {'accept': 'application/json, text/plain, */*', 'content-type': 'application/json'})
		debug(content_url = content.url)
		content = content.json()
		# content = content.content
		debug(content = content)
		# pprint(content)
		urlparsed = urlparse(content.get('data').get('itemInfo').get('resolutionList')[0].get('url'))
		debug(urlparsed = urlparsed)
		response = urlparsed.scheme + "://" + "wdl.nuplink.net" + urlparsed.path + "?" + urlparsed.query + "&filename=" + quote(content.get('data').get('itemInfo').get('name'))
		debug(response = response)
		clipboard.copy(response)
		saveas = saveas or content.get('data').get('itemInfo').get('name')
		if download_path:
			self.download_linux(response, download_path, cookies = self.HEADERS, saveas = saveas)
		return response, os.path.join(download_path, saveas), headers

	@classmethod
	def usage(self):
		parser = argparse.ArgumentParser(formatter_class= argparse.RawTextHelpFormatter)#, version = get_version.get())
		parser.add_argument('URL', action = 'store', help = 'linktobox.to url or id, example: "https://www.linkbox.to/file/fp3btk0000gz" or "fp3btk0000gz", type "c" for get url from clipboard')
		parser.add_argument('-p', '--download-path', action = 'store', help = 'Download path to save file')
		parser.add_argument('-n', '--name', action = 'store', help = 'Alternative Save as name')
		parser.add_argument('-d', '--debug', action = 'store_true', help = 'Debugger process')
		parser.add_argument('-c', '--clipboard', action = 'store_true', help = 'Copy generated link to clipboard')
		parser.add_argument('-v', '--version', action = 'store_true', help = 'get version number')

		if len(sys.argv) == 1:
			parser.print_help()
		elif len(sys.argv) == 2:
			if sys.argv[1] == '-v' or sys.argv[1] == '--version':
				print(make_colors("VERSION:", 'lc') + " " + make_colors(get_version.get() or "0.1", 'ly'))
				sys.exit()
		else:
			args = parser.parse_args()
			if args.version:
				print(make_colors("VERSION:", 'lc') + " " + make_colors(get_version.get() or "0.1", 'ly'))
				sys.exit()
			debug(debugger = args.debug)
			if self.config.read_config('debug', 'debug', value= False):
				self.debug = eval(self.config.read_config('debug', 'debug', value= False))
				debug(self_debug = self.debug)
			self.debug = args.debug
			debug(self_debug = self.debug)
			if args.URL == 'c':
				args.URL = clipboard.paste()

			url_download, name, cookies = self.generate(args.URL, args.download_path, args.name)

			if not args.download_path:
				print(make_colors("GENERATED:", 'w', 'r') + " " + make_colors(url_download, 'b', 'ly', attrs= ['blink']))
				if args.clipboard:
					clipboard.copy(url_download)

def usage():
	return LinkToBox.usage()

if __name__ == '__main__':
	# LinkToBox.generator("fp3btk0000gz")
	LinkToBox.usage()
