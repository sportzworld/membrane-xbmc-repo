import resources.lib.utils as utils
"""
enables the caching of web requests. this will:
- save some time wasted by web requests
- make fever web requests
this results in a performance gain, most dominant on low power platforms
""" 

def request(url,method='get',data='',ttl=3600):#returns a cached version if we have a fresh one
	if ttl == 0:
		return utils.GET(url)#todo post
	hash = utils.hash(url)
	print 'hash for '+url+' is '+ hash
	file = utils.f_translate_path(utils.f_basepath() + '/webcache/' + hash)
	path = utils.f_translate_path(utils.f_basepath() + '/webcache/')
	epoch = utils.epoch()
	if not utils.f_check_existance(path):
		utils.f_mkdir(path)
		
	if utils.f_check_existance(file):
		f = utils.f_open(file)
		abs_ttl = int(f[:10])
		print abs_ttl
		print epoch
		f = f[11:]
	if not utils.f_check_existance(file) or abs_ttl < epoch:#checks if the milk is sour
		f = utils.GET(url)#todo post
		utils.f_write(file,str(epoch+ttl)+f)
		print 'request new file'
	else:
		print 'use cached copy'
	return f

def clear_cache():
	utils.f_rmdir(utils.f_translate_path(utils.f_basepath() + '/webcache/'))
	utils.f_mkdir(utils.f_translate_path(utils.f_basepath() + '/webcache/'))
	return True
"""
def remove_expired():
	__epoch = utils.epoch()
	index = open(indexfile)
	new_index = ''
	for line in index:
		if abs_ttl > epoch:
			new_index = line + abs_ttl + '\n'
		else:
			remove(fileofmd5)
	if new_index != index:
		write(indexfile,new_index)
def remove_old(i=100):
	print 'todo'
"""