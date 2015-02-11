# -*- coding: utf-8 -*-
import urllib,urllib2,re,random,xbmcplugin,xbmcgui,xbmcaddon,cookielib,HTMLParser,datetime
from time import gmtime, strftime

__settings__ = xbmcaddon.Addon(id='plugin.video.nhlvideocenter')
__language__ = __settings__.getLocalizedString

if __settings__.getSetting("firstrun") == 'true':
	__settings__.setSetting(id="firstrun",value='false')

import resources.lib.utils as utils
import resources.lib.webcache as webcache
#try:
#	import StorageServer
#except:
#	import storageserverdummy as StorageServer
#cache = StorageServer.StorageServer("nhlvideocenter", 24)

html_parser = HTMLParser.HTMLParser()

month = strftime("%m", gmtime())
year = strftime("%Y", gmtime())




COOKIEFILE = xbmc.translatePath(__settings__.getAddonInfo('profile')+"cookies.lwp")


pluginhandle = int(sys.argv[1])

mainurl = 'http://video.nhl.com/videocenter/'



def MAIN():
	addDir(__language__(30002).encode("utf-8"),'Search',9,'')
	LIST_VIDEOCENTER(mainurl)
	addDir(__language__(30003),mainurl,4,'',__language__(30004))

	
def LIST_VIDEOCENTER(url):#5
	response = webcache.request(url,ttl=86400)
	match=re.compile('<table id="tblMenu".+?>(.+?)</div>', re.DOTALL).findall(response)
	#print match[0]
	match_topics=re.compile('<tr>(.+?)</table>', re.DOTALL).findall(match[0])
	#match_topics=match[0].split('</table>')
	for topic in match_topics:
		#print topic
		match_name=re.compile('<td style.+?>(.+?)/td>', re.DOTALL).findall(topic)
		#match_name=re.compile('<td.+?>(.+?)</td>', re.DOTALL).findall(topic)
		name_a = match_name[0].replace('\n','').replace('<','')
		name_b = match_name[1].replace('\n','').replace('<','')
		#log('name_a: '+name_a)
		#log('name_b: '+name_b)
		
		match_id=re.compile('id="(.+?)"').findall(topic)
		id = match_id[0]
		#log('id: '+id)
		
		match_menuindex=re.compile('menuindex="(.+?)"').findall(topic)
		menuindex = match_menuindex[0]
		#log('menuindex: '+menuindex)
		
		match_menuid=re.compile('menuid="(.+?)"').findall(topic)
		menuid = match_menuid[0]
		#log('menuid: '+menuid)
		
		match_menutype=re.compile('menutype="(.+?)"').findall(topic)
		menutype = match_menutype[0]
		#log('menutype: '+menutype)
		
		name = name_a+' - '+name_b
		
		if menutype == '1':
			newurl = mainurl+'servlets/guide?channeldays=7&cid='+menuid+'&ispaging=false&large=true&menuChannelId='+menuid+'&menuChannelIndex='+menuindex+'&pn=1&ps=7&ptrs=3'
			addDir(fix_name(name_a),newurl,10,'',name_b)
			
		elif menutype == '0':
			newurl = mainurl+'servlets/browse?cid='+menuid+'&component=_browse&ispaging=false&large=true&menuChannelId='+menuid+'&menuChannelIndex='+menuindex+'&pm=0&pn=1&ps=12&ptrs=3'
			addDir(fix_name(name_a),newurl,10,'',name_b)
		
		elif menutype == '4':
			newurl = mainurl+'servlets/guide?channeldays=7&cid='+menuid+'&ispaging=false&large=true&menuChannelId='+menuid+'&menuChannelIndex='+menuindex+'&pn=1&ps=7&ptrs=3'
			addDir(fix_name(name_a),newurl,10,'',name_b)
			#log('Menutype not used: '+menutype)
			#log('Livestreams not working')
			
		elif menutype == '5':
			log('Menutype not used: '+menutype)
			log('Podcasts not working')
			
		elif menutype == '100':
			if url[-1] == '/':
				newurl = url 
			else:
				newurl = url + '/'
			addDir(fix_name(name_a),newurl,1,'',fix_name(name_b))
			

		else:
			log('Menutype not used: '+menutype)
			log('Name: '+fix_name(name))
	
			
def fix_name(name):#make 'STRING' to 'String'
	fixed_name = ''
	firstchar = True
	words = name.split(' ')
	for name in words:
		m = ''
		#if len(name) > 1:
		if len(name) > 3:
			
			for i in range(0, len(name)):
				if not firstchar == True:
					n = name[i].lower()
				else:
					n = name[i]
					
				m = m + n
				
				if n == ' ':
					firstchar = True
				else:
					firstchar = False
		else:
			m = name
		if fixed_name == '':
			fixed_name = m
		else:
			fixed_name = fixed_name + ' ' + m
	fixed_name = fixed_name.replace('Nhl','NHL')
	fixed_name = fixed_name.replace('nhl','NHL')
	fixed_name = fixed_name.replace('Sd ','SD ')
	fixed_name = fixed_name.replace('Pp','PP')
	fixed_name = fixed_name.replace('&#039;',"'")
	return fixed_name
			
		
		
		
def INDEX_HIGHLIGHTS(url):#1
	
	#addDir(__language__(30100).encode("utf-8"),mainurl+'highlights?xml=0&year='+year+'&month='+month,3,'')
	addDir(__language__(30100).encode("utf-8"),url+'highlights?xml=0',4,'')
	end_year = 2010
	count_year = int(year)
	while count_year >= end_year:
		addDir(str(count_year),url+'highlights?xml=0&year='+str(count_year),2,'')
		count_year -= 1
	
def MONTH(url):#2
	count_month = 1
	
	if '2010' in url:
		count_month = 9

	if year in url:
		active_year = True
		if month == '10':
			end_month = 10#TODO: make pretty
		else:
			end_month = int(month.replace('0',''))
	else:
		active_year = False
		end_month = 12


	while count_month <= end_month:
		name = str(count_month)
		name = name.replace('12',__language__(30112))#December
		name = name.replace('11',__language__(30111))#November
		name = name.replace('10',__language__(30110))#October
		name = name.replace('1',__language__(30101))#January
		name = name.replace('2',__language__(30102))#February
		name = name.replace('3',__language__(30103))#March
		name = name.replace('4',__language__(30104))#April
		name = name.replace('5',__language__(30105))#May
		name = name.replace('6',__language__(30106))#June
		name = name.replace('7',__language__(30107))#July
		name = name.replace('8',__language__(30108))#August
		name = name.replace('9',__language__(30109))#September
		if not active_year or count_month < end_month-1:
			addDir(name.encode("utf-8"),url+'&month='+str(count_month),3,'')
		else:
			addDir(name.encode("utf-8"),url+'&month='+str(count_month),4,'')
		count_month += 1


def RESULTS(url,cache=True):#3
	#link = getUrl(mainurl+'highlights'+url)
	if cache:
		link = webcache.request(url,ttl=2592000)#cache it for a month if it is not an active month
	else:
		link = webcache.request(url,ttl=1800)#cache it for 30min else
	match=re.compile('<game>(.+?)</game>', re.DOTALL).findall(link)
	
	for game in match:
		"""
		date = 'DATE'
		guestname = 'GUESTNAME'
		guestcity = 'GUESTCITY'
		guestgoals = 'GUESTGOALS'
		homename = 'HOMENAME'
		homecity = 'MOMECITY'
		homegoals = 'HOMEGOALS'
		url = 'URL'
		possiblethumb = 'POSSIBLETHUMB'
		"""

		match_date=re.compile('<game-date>(.+?)</game-date>', re.DOTALL).findall(game)

		match_guest=re.compile('<away-team>(.+?)</away-team>', re.DOTALL).findall(game)
		match_guest_name=re.compile('<name>(.+?)</name>', re.DOTALL).findall(match_guest[0])
		match_guest_city=re.compile('<city>(.+?)</city>', re.DOTALL).findall(match_guest[0])
		match_guest_goals=re.compile('<goals>(.+?)</goals>', re.DOTALL).findall(match_guest[0])
		match_guest_logo=re.compile('<logo-40px>(.+?)</logo-40px>', re.DOTALL).findall(match_guest[0])

		match_home=re.compile('<home-team>(.+?)</home-team>', re.DOTALL).findall(game)
		match_home_name=re.compile('<name>(.+?)</name>', re.DOTALL).findall(match_home[0])
		match_home_city=re.compile('<city>(.+?)</city>', re.DOTALL).findall(match_home[0])
		match_home_goals=re.compile('<goals>(.+?)</goals>', re.DOTALL).findall(match_home[0])
		match_home_logo=re.compile('<logo-40px>(.+?)</logo-40px>', re.DOTALL).findall(match_home[0])
		
		match_url=re.compile('<alt-video-clip>(.+?)</alt-video-clip>', re.DOTALL).findall(game)
		match_duration=re.compile('<video-duration>(.+?)</video-duration>', re.DOTALL).findall(game)
		match_possiblethumb=re.compile('<video-clip-thumbnail>(.+?)</video-clip-thumbnail>', re.DOTALL).findall(game)

		date = match_date[0]
		MM,DD,YYYY=date.split('/')
		guestname = match_guest_name[0]

		try:
			guestcity =  match_guest_city[0]+' '
		except:
			guestcity =  ''

		guestgoals =  match_guest_goals[0]

		homename = match_home_name[0]

		try:
			homecity =  match_home_city[0]+' '
		except:
			homecity =  ''
		homegoals = match_home_goals[0]

		try:
			duration = match_duration[0]
		except:
	   		duration = False
			
		try:
			url = match_url[0]
		except:
	   		match_rtmp=re.compile('<video-clip>(.+?)</video-clip>', re.DOTALL).findall(game)
			url = match_rtmp[0]+' swfurl=http://nhl.cdn.neulion.net/u/videocenter/console.swf swfvfy=true'


		possiblethumb = match_possiblethumb[0]

		date_thumb = date.split('/')
		thumb = ''
		if int(date_thumb[2]) > 2010:
			thumb = possiblethumb
		if int(date_thumb[2]) == 2010 and int(date_thumb[0].replace('0','')) > 8:
			thumb = possiblethumb
		name = date+' '+homecity+homename+' vs. '+guestcity+guestname
		if xbmcplugin.getSetting(pluginhandle,"show_score") == 'true':
			name += ' - '+homegoals+':'+guestgoals
		name = name.replace('&#233;','é')
		url = url.replace('<![CDATA[','')
		url = url.replace(']]>','')
		thumb = thumb.replace('<![CDATA[','')
		thumb = thumb.replace(']]>','')
		thumb = thumb.replace('_es','_eb')
		#addLinkOld(name,url,thumb,duration)
		addLinkOld(name,url,thumb,duration,True,match_home_city[0],match_guest_city[0],match_home_name[0],match_guest_name[0],largethumb(match_home_logo[0]),largethumb(match_guest_logo[0]),match_home_goals[0],match_guest_goals[0],DD,MM,YYYY)

def RESULTS_UNCACHED(url):
	RESULTS(url,cache=False)
def TEAMS(url):#4 not in use at the moment
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match_all_teams=re.compile('<div id="teamMenu">(.+?)<div id="identityBanner">', re.DOTALL).findall(link)
	match=re.compile('title="(.+?)" href="(.+?)"', re.DOTALL).findall(match_all_teams[0])
	for name,url in match:
		urlsplit = url.split('?')
		url = urlsplit[0].replace('http://','http://video.')+'/videocenter'
		if name != "NHL.com":
			addDir(name,url,5,'')

def LIST_TEAMS(url):#5 not in use at the moment
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match_css=re.compile('<link rel="stylesheet" type="text/css" href="(.+?)" />').findall(link)
	match_catid=re.compile('catid=(.+?)">(.+?)</a>', re.DOTALL).findall(link)
	req = urllib2.Request(match_css[-1])
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match_bg=re.compile('background-image:url\((.+?)\)').findall(link)

	for catid,name in match_catid:
		if catid != '0':
			name = name.replace('\n','')
			name = name.replace('	','')
			url2 = url+'/servlets/browse?cid='+catid+'&component=_browse&ispaging=true&large=true&menuChannelId='+catid+'&menuChannelIndex='+'2'+'&pm=0&pn=1&ps=12&ptrs=3'
			#		   /servlets/browse?cid=647	  &component=_browse&ispaging=true&large=true&menuChannelId=647	  &menuChannelIndex=2	  &pm=0&pn=1&ps=12&ptrs=3
			addDirFan(name,url2,5,'',match_bg[0])

def VIDEOS(url,name,fanart):#6 not in use at the moment
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile("<table title=\"(.+?)\".+?_console.playVideo\('.+?','.+?','(.+?)'.+?src=\"(.+?)\"", re.DOTALL).findall(link)

	for name,url,thumb in match:
		url = url.replace(':','%3A')
		url = url.replace('/','%2F')
		url = url.replace('.','%2E')
		url = url.replace('_','%5F')
		url = url.replace('?','%3F')
		url = url.replace('=','%3D')
		url = url.replace('&','%26')
		url = 'http://video.bruins.nhl.com/videocenter/servlets/encryptvideopath?path=' + url + '&isFlex=true&type=fvod'

		addLink(name,url,6,thumb)

def PLAY(url,name):#7 not in use at the moment
	req = urllib2.Request('http://video.ducks.nhl.com/videocenter/servlets/browse?cid=647&component=_browse&ispaging=false&large=true&menuChannelId=647&menuChannelIndex=2&pm=0&pn=1&ps=12&ptrs=3')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()


	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('\[CDATA\[(.+?)\]').findall(link)


	item = xbmcgui.ListItem(path=match[0])
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)

def SEARCH(url):
	sword = searchbox()
	url = mainurl+'servlets/search?cid=&menuChannelId=&menuChannelIndex=&param='+sword+'&pm=0&pn=1&ps=24&ptrs=3&type=0'
	log('Search url is: '+url)
	MENUTYPE_1(url)

	
def MENUTYPE_1_START(url):#10 
	#cache_clear()
	MENUTYPE_1(url,firstpage=True)
	
def MENUTYPE_1(url,firstpage=False):#11 
	#i = cache_list_stored()
	#stuff = ''
	response = webcache.request(url,ttl=1800)#cache it for 30min
	response = response.decode('utf-8')
	response = response.encode('ascii','ignore')
	#print excepttion
	match=re.compile(u'<td valign="top">(.+?)</table>', re.DOTALL).findall(response)
	for entry in match:
		match_name_a=re.compile('<div divType="prog_name".+?>(.+?)</div>').findall(entry)
		name_a = match_name_a[0]
		log('name_a: '+name_a)

		match_name_b=re.compile('title="(.+?)"').findall(entry)
		name_b = match_name_b[0]
		print name_b
		print name_b.encode('ascii','ignore')
		log('name_b: '+name_b)
		
		match_onclick=re.compile('onclick="(.+?)"').findall(entry)
		onclick = match_onclick[0]
		log('onclick: '+onclick)
		match_video=re.compile("'(.+?)'").findall(onclick)
		video = match_video[2]
		log('video: '+video)
		
		sd = match_video[4]
		log('sd: '+sd)
		
		
		

		match_thumb=re.compile('src="(.+?)"').findall(entry)
		thumb = match_thumb[0]
		replacement=re.compile('/s/(.+?)/').findall(video)
		if len(replacement) != 0 and replacement[0] != 'nhl':
			thumb = thumb.replace('/u/www/','/u/'+replacement[0]+'/')#for the team specific urls, idk why they do that
		log('thumb: '+thumb)
		
		name = name_a+' - '+name_b
		#name = name.replace('&#039;',"'")
		#name_a = name_a.replace('&#039;',"'")
		
		if sd == '1':
			video = video.replace('.mp4',u'_sd.mp4')
		#stuff = stuff + '<vid>'+name_a+'|'+video+'|'+'11'+'|'+thumb+'|'+name_b+'</vid>'

		addLink(html_parser.unescape(fix_name(name_a)),video,12,thumb,html_parser.unescape(fix_name(name_b)))
	
	#cache_store(stuff)
	
	if 'NÄCHSTE</a>' in response or 'NEXT</a>' in response:
		match_onclick=re.compile('onclick="(.+?)"').findall(response)
		if not '_search.searchMoviesByPage' in response:
			match_next=re.compile('\(\'(.+?)\',(.+?)\)').findall(match_onclick[-2])
			menuid,page = match_next[0]
		else:
			match_next=re.compile('\((.+?)\)').findall(match_onclick[-2])
			page = match_next[0]
		currentpage=re.compile('&pn=(.+?)&').findall(url)
		url = url.replace('&pn='+currentpage[0],'&pn='+page)
			
		addDir(__language__(30001).encode("utf-8"),url,11,'')
	
	if firstpage == False:
		if __settings__.getSetting('back_hidden') != 'true':
			i = i + 1
		try:
			wnd = xbmcgui.Window(xbmcgui.getCurrentWindowId())
			wnd.getControl(wnd.getFocusId()).selectItem(i)
			

		except:
			log('focusing not possible')
		
		xbmcplugin.endOfDirectory(int(sys.argv[1]), updateListing=True)

def PLAY_1(url,name,thumb):#12
	response = getUrl(mainurl+'servlets/encryptvideopath?type=fvod&isFlex=true&path='+urllib.quote_plus(url))
	match_video=re.compile('<path>(.+?)</path>').findall(response)
	video = match_video[0]
	video = video.replace('<![CDATA[','')
	video = video.replace(']]>','')

	
	item=xbmcgui.ListItem(name, thumbnailImage='', path=video)
	item.setProperty('mimetype', 'video/x-flv')
	xbmcplugin.setResolvedUrl(pluginhandle, True, item)
	

"""	
def cache_store(stuff,name=''):
	stuff = stuff.decode('utf-8')
	#"#""
	stuff = stuff.replace('ä','&auml;')
	stuff = stuff.replace('Ä','&Auml;')
	stuff = stuff.replace('ö','&ouml;')
	stuff = stuff.replace('Ö','&Ouml;')
	stuff = stuff.replace('ü','&uuml;')
	stuff = stuff.replace('Ü','&Uuml;')
	stuff = stuff.replace('ß','&szlig;')
	stuff = stuff.replace('\n','&newline')
	#"#""
	cache.table_name = "nhltable"
	log('store: '+stuff)
	#cache.set('test', urllib.quote_plus(stuff))
	cache.set('cache', stuff)
	return True
	
def cache_recall(name=''):
	cache.table_name = "nhltable"
	stuff = cache.get('cache')
	stuff = stuff.encode("utf-8")
	#"#""
	stuff = stuff.replace('&auml;','ä')
	stuff = stuff.replace('&Auml;','Ä')
	stuff = stuff.replace('&ouml;','ö')
	stuff = stuff.replace('&Ouml;','Ö')
	stuff = stuff.replace('&uuml;','ü')
	stuff = stuff.replace('&Uuml;','Ü')
	stuff = stuff.replace('&szlig;','ß')
	stuff = stuff.replace('&newline','\n')
	#"#""
	log('recall: '+stuff)
	return stuff
	
	
def cache_list_stored():
	i = 0
	match_stored_vids=re.compile('<vid>(.+?)</vid>', re.DOTALL).findall(cache_recall())
	for vid in match_stored_vids:

		i = i + 1
		name,url,mode,thumb,plot=vid.split('|')
		addLink(name,url,mode,thumb,plot)
	return i
	
def cache_clear():
	cache.table_name = "nhltable"
	cache.delete("cache")
"""	
def searchbox():
	searchStr = ''
	keyboard = xbmc.Keyboard(searchStr,'Search')
	keyboard.doModal()
	if (keyboard.isConfirmed() == 'false'):
		return
	searchStr = keyboard.getText().replace(' ','%20')
	if len(searchStr) == 0:
		return
	else:
		return searchStr
		

def getUrl( url , extraheader=True):
	print url
	cj = cookielib.LWPCookieJar()
	if os.path.isfile(COOKIEFILE):
		cj.load(COOKIEFILE, ignore_discard=True)

	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;)')]
	usock=opener.open(url)
	response=usock.read()
	usock.close()
	cj.save(COOKIEFILE, ignore_discard=True)
	return response
	

def log(message):
	if xbmcplugin.getSetting(pluginhandle,"debug") == 'true':
		try:
			print "#####NHL Videocenter Debug: "+unicode(message)
		except:
			print "#####NHL Videocenter Debug: unicode from HELL"
	return


def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
								
	return param


def largethumb(thumb):
	thumb = thumb.replace('_es.jpg','_eb.jpg')
	thumb = thumb.replace('110x62','640x360')
	thumb = thumb.replace('small','extralarge')
	return thumb


def addLinkOld(name,url,iconimage,duration,extrainfo=False,home_city='',guest_city='',home_name='',guest_name='',home_logo='',guest_logo='',home_score='',guest_score='',game_dd='',game_mm='',game_yyyy=''):
	iconimage = largethumb(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	if extrainfo:
		liz.setInfo( type="Video", infoLabels={ "Title": name , "home_city": home_city , "guest_city": guest_city , "home_name": home_name , "guest_name": guest_name , "home_logo": home_logo , "guest_logo": guest_logo , "home_score": home_score , "guest_score": guest_score , "game_dd": game_dd , "game_mm": game_mm , "game_yyyy": game_yyyy } )
	else:
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.addStreamInfo('video', { 'codec': 'h264', 'width':960 ,'height' : 540 ,'duration' : int(duration) })
	liz.setProperty('fanart_image',iconimage)

	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addLink(name,url,mode,iconimage,plot='',duration=False):
	name = html_parser.unescape(fix_name(name))
	plot = html_parser.unescape(fix_name(plot))
	iconimage = largethumb(iconimage)
	if xbmcplugin.getSetting(pluginhandle,"description") == 'true' and not plot == '':
		name = name + ' - ' + plot
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	#liz.setInfo( type="Video", infoLabels={ "Title": name , "Plot": plot , "Plotoutline": plot , "Duration": duration } )
	liz.setInfo( type="Video", infoLabels={ "Title": name , "Plot": plot , "Plotoutline": plot} )
	liz.setProperty('IsPlayable', 'true')
	liz.setProperty('fanart_image',iconimage)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,plot=''):
	iconimage = largethumb(iconimage)

	if xbmcplugin.getSetting(pluginhandle,"description") == 'true' and not plot == '':
		name = name + ' - ' + plot
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name , "Plot": plot , "Plotoutline": plot } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
		
def addDirFan(name,url,mode,iconimage,fanart):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('fanart_image',fanart)

	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
			  
params=get_params()
url=None
name=None
thumb=None
mode=None
fanart=None

try:
		url=urllib.unquote_plus(params["url"])
except:
		pass
try:
		name=urllib.unquote_plus(params["name"])
except:
		pass
try:
		thumb=urllib.unquote_plus(params["thumb"])
except:
		pass
try:
		mode=int(params["mode"])
except:
		pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
		print ""
		MAIN()

elif mode==1:
		print ""+url
		INDEX_HIGHLIGHTS(url)
		
elif mode==2:
		print ""+url
		MONTH(url)
		
elif mode==3:
		print ""+url
		RESULTS(url)	
		
elif mode==4:
		print ""+url
		RESULTS_UNCACHED(url)

elif mode==9:
		print ""+url
		SEARCH(url)
		
elif mode==10:
		print ""+url
		MENUTYPE_1_START(url)
		
elif mode==11:
		print ""+url
		MENUTYPE_1(url)
		
elif mode==12:
		print ""+url
		PLAY_1(url,name,thumb)


elif mode==4:
		print ""+url
		TEAMS(url)

elif mode==5:
		print ""+url
		LIST_VIDEOCENTER(url)
"""
elif mode==6:
		print ""+url
		VIDEOS(url,name,fanart)

elif mode==7:
		print ""+url
		PLAY(url,name)
"""

xbmcplugin.endOfDirectory(int(sys.argv[1]))
