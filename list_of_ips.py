import sys,os,re, pygeoip, webbrowser

def list_of_ips(files):
	''' path to log file with ip numbers, find ips and save to list '''
	files = files.split(',')
	ips = []
	for file in files:
		with open(file, "r") as file:
			for text in file.readlines():
				text = text.rstrip()
				regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', text)
				if regex is not None:
					ips.extend(regex)
	return ips

def remove_duplicates(list_of_ips):
	''' func to remove duplicates '''
	list_of_ips = list(set(list_of_ips))
	return list_of_ips

def count_list(ips):
	''' len function '''
	count = 0
	for ip in ips:
		count +=1
	return count

def make_dict():
	''' Make a list from an auth.log file, from what country, how many tries, from what ip '''
	file = input('FilePath: ')
	ip_list = list_of_ips(file)
	places = dict()
	ips_dict = {}
	gip = pygeoip.GeoIP('GeoLiteCity.dat')
	for addr in ip_list:
		rec = gip.record_by_addr(addr)
		try:
			country = rec['country_name']
		except:
			country = ''
		if rec is not None:
			country = rec['country_name']

			if country not in ips_dict:
				ips_dict.setdefault(country, []).append(0)
			if addr not in ips_dict[country]:
				ips_dict.setdefault(country, []).append(addr)
			ips_dict[country][0] += 1
	new_dict = []
	for key, value in ips_dict.items():
		new_dict.append({'country':key, 'count':value[0], 'ips':value[1:]})
	return new_dict
