cachedir = 

class listcache:
	def start(new=True,page_list_size=0,ttl=-1,confirmed_cache_matches=3):
		if new:
			clear_cache()#todo: even smarter caching
		else:
			list_cache()
	def add_entry(self,name,url,mode,thumb='',fanart='',plot='',folder=False,addmore=False,loadinbackground=False,ttl=0):
		if not addmore:
			if folder:
				addDir(name,url,mode,thumb,fanart,plot)
			else:
				addLink(name,url,mode,thumb,fanart,plot)
		else:
			addDir(name,url,mode,thumb,fanart,plot)


class requestcache:
	def request(url,method,data='',ttl=3600):#returns a cached version if we have a fresh one
		if ttl == 0:
			return utils.GET(url)#todo post
		
		path = utils.f_translate_path(utils.f_basepath() + '/webcache/' + utils.hash(url))
		if utils.f_check_existance(path):
			f = utils.f_open(path)
			abs_ttl = f[:9]
			f = f[10:]
		if not utils.f_check_existance(path) or abs_ttl < epoch:#checks if the milk is sour
			f = utils.GET(url)#todo post
			utils.f_write(str(utils.epoch()+ttl)+f)
			print 'request new file'
		else:
			print 'use cached copy'
		return f
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

#def end_list():