# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,string,random,xbmcaddon,threading,base64,cookielib


pluginhandle = int(sys.argv[1])

baseurl = 'http://sport.puls4.com/'

xip = '80.152.42.240'

addon = xbmcaddon.Addon(id='plugin.video.puls4sport')
akamaiProxyServer = xbmc.translatePath(addon.getAddonInfo('path')+"/akamaiSecureHD.py")
akamaiProxyServerLive = xbmc.translatePath(addon.getAddonInfo('path')+"/akamaiSecureHDLive.py")
#testfile = xbmc.translatePath(addon.getAddonInfo('path')+"/test.flv")

COOKIEFILE = xbmc.translatePath(addon.getAddonInfo('path')+"cookies.lwp")
#USERFILE = xbmc.translatePath(addon.getAddonInfo('path')+"userfile.js")
URL_AKAMAI_PROXY = 'http://127.0.0.1:64653/laola/%s'

def log(message):
	#if xbmcplugin.getSetting(pluginhandle,"debug") == 'true':
	print "#####Laola1 Debug: "+message
	return
	
class LivePlayer(xbmc.Player):
	def __init__(self):
		xbmc.Player.__init__(self)
		log('LivePlayer init')
		self._playbackLock = threading.Event()
		self._playbackLock.set()

	def onPlayBackStarted(self):
		log('LivePlayer onplayback')
		
	def PlayStream(self,fullUrl,thumb,name):
		
		try:
			getUrl('http://127.0.0.1:64653/version')
			getUrl('http://127.0.0.1:64653/stop')
		except:
			pass
		xbmc.sleep(500)
		#xbmc.executebuiltin('RunScript('+akamaiProxyServerLive+')')
		xbmc.executebuiltin('RunScript('+akamaiProxyServer+')')
		xbmc.sleep(500)

		VIDb64 = base64.encodestring(fullUrl).replace('\n', '')
		fullUrl = URL_AKAMAI_PROXY % VIDb64

		item=xbmcgui.ListItem(name, thumbnailImage=thumb, path=fullUrl)
		item.setProperty('mimetype', 'video/x-flv')
		#xbmc.Player(playercore).play(fullUrl,item)
		xbmcplugin.setResolvedUrl(pluginhandle, True, item)


	def onPlayBackStopped(self):
		log('LivePlayer stop')
		getUrl('http://127.0.0.1:64653/stop')
		self._playbackLock.clear()

	def onPlayBackPaused(self):
		log('Paused')

def MAIN():
	addDir('Live','http://sport.puls4.com/live',3,'')
	"""
	response=getUrl(baseurl+'video')
	match_cats=re.compile('<div class="tabnavi">(.+?)</div>', re.DOTALL).findall(response)
	match_cat=re.compile('<li(.+?)</li>', re.DOTALL).findall(match_cats[0])
	for cat in match_cat:
		match_thumb=re.compile('src="(.+?)"', re.DOTALL).findall(cat)
		match_url=re.compile('href="/(.+?)"', re.DOTALL).findall(cat)
		match_name=re.compile('alt="(.+?)"', re.DOTALL).findall(cat)
		addDir(match_name[0],baseurl+match_url[0]+'/video',1,baseurl+match_thumb[0])
	"""
	
liveplayer = LivePlayer()

def LIST_VOD(url):#1
	response=getUrl(url)
	match_videos=re.compile('<div class="video_uebersicht_paging">(.+?)<div class="pages">', re.DOTALL).findall(response)
	match_video=re.compile('<div class="teaser">(.+?)/p>', re.DOTALL).findall(match_videos[0])
	
	for video in match_video:
		match_thumb=re.compile('src="(.+?)"', re.DOTALL).findall(video)
		match_url=re.compile('href="/(.+?)"', re.DOTALL).findall(video)
		match_name=re.compile('<h3>(.+?)</h3>', re.DOTALL).findall(video)
		match_desc=re.compile('<p class="description">(.+?)<', re.DOTALL).findall(video)
		addLink(match_name[0],baseurl+match_url[0],2,baseurl+match_thumb[0],match_desc[0])
		
	#match_next #TODO!!
	#<li class="pageing" data-val="2" style="color:#999;font-weight:bold; font-size:14px; cursor:pointer"> > </li>


def PLAY_VOD(url,name):#2
	response=getUrl(url)
	match_videopfad=re.compile('&videopfad=(.+?)&', re.DOTALL).findall(response)

	req = urllib2.Request(match_videopfad[0])
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	#if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
	print 'Try to use X-Forwarded-For trick'
	req.add_header('X-Forwarded-For', xip)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	print 'link'
	print link
	match_httpBase=re.compile('<meta name="httpBase" content="(.+?)"', re.DOTALL).findall(link)
	match_video=re.compile('<video src="(.+?)"', re.DOTALL).findall(link)
	video = match_httpBase[0]+match_video[-1].replace('&amp;','&')+'&v=2.11.3&fp=WIN%2011,6,602,171&r='+char_gen(5)+'&g='+char_gen(12)
	
	#listitem = xbmcgui.ListItem(path=video)
	#return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	
	thumb = ''
	
	item=xbmcgui.ListItem(name, thumbnailImage=thumb, path=video+" live=true")
	item.setProperty('mimetype', 'video/x-flv')
	LivePlayer().PlayStream(video,thumb,name)
	
def LIST_LIVE(url):
	response=getUrl(url)
	match_livestreams=re.compile('<!--LIVE PROGRAMM ANFANG -->(.+?)<!-- LIVE PROGRAMM ENDE -->', re.DOTALL).findall(response)
	match_livestream=re.compile('<div class="time">(.+?)<.+?<div class="category">(.+?)</div>.+?href="(.+?)".+?>(.+?)<', re.DOTALL).findall(match_livestreams[0])
	for time,cat,url,name in match_livestream:
		addLink(time+' - '+cat+' - '+name,url,4,'')
		
def PLAY_LIVE(url):
	response=getUrl(baseurl+url)
	match_videopfad=re.compile('&videopfad=(.+?)&', re.DOTALL).findall(response)
	print match_videopfad
	PLAY_LIVE_1B(match_videopfad[0])


def PLAY_LIVE_1B(url,name='LIVE',thumb='',streamid='',offset='0'):#11

	"""
	link,etag=getUrlCookie(url,get_etag=True)
	xbmc.sleep(500)
	"""
	link=getUrl(url)
	#xbmc.sleep(5000)

	if 'This stream is not available in your region' in link:
		log('Geolocked stream called')
		#xbmc.executebuiltin("Notification("+__language__(30009)+","+__language__(30010)+", 7000)")
		return
	
	print link
	match_rtmp=re.compile('<meta name="rtmpPlaybackBase" content="(.+?)" />').findall(link)
	match_http=re.compile('<meta name="httpBase" content="(.+?)" />').findall(link)
	match_quality=re.compile('<video src="(.+?)" system-bitrate=".+?"/>').findall(link)
	http = match_http[0]
	log('Base video url: '+http)
	#http = http.replace("&l=","&l=&v=2.4.5&fp=LNX%2010,3,162,29&r="+char_gen(5)+"&g="+char_gen(12))

	#if livequality == '0':
	#	video = match_quality[0]
	#if livequality == '1':
	#	try:
	#		video = match_quality[1]
	#	except:
	#		video = match_quality[0]
	#if livequality == '2':
	video = match_quality[-1]
		
	video = video + "&v=2.11.3&fp=WIN%2011,6,602,180&r="+char_gen(5)+"&g="+char_gen(12)
	video = video.replace('&amp;','&')
	#if '&e=&' in video:
	#	video = video.replace('&e=','&e='+streamid)
	if not '&p=1' in video:
		video = video.replace('&p=','&p=1')
		
	
	log("playing: "+http+video)

	if '1' == '2':#xbmcplugin.getSetting(pluginhandle,"replay"):
		log('using replay')
		#name = urllib.quote_plus(params["name"])
		print name
		offset = 0
		
		if '1' == '2':#xbmcplugin.getSetting(pluginhandle,"ads"):#disabled
			print 'todo: remove ad'
			
		
		#xbmc.sleep(2000)
		pl=xbmc.PlayList(1)
		pl.clear()
		#xbmc.sleep(2000)
		#item.setProperty('mimetype', 'video/x-flv')
		item = xbmcgui.ListItem('Dummy entry',thumbnailImage='')
		xbmc.PlayList(1).add('', item)
		#xbmc.PlayList(1).add('', item)
	
		item=xbmcgui.ListItem(name+'replay', thumbnailImage=thumb)

		log('1')
		xbmc.PlayList(1).add('plugin://plugin.video.laola1live/?url='+enc_url(http+video)+'&mode=12&thumb='+enc_url(thumb)+'&offset=0&name='+urllib.quote_plus(name), item)
		log('2')
		item=xbmcgui.ListItem(name, thumbnailImage=thumb)

		xbmc.PlayList(1).add(http+video+" live=true", item)
		#xbmc.Player().play(pl)

		
	else:
		log('Replay disabled')
		item=xbmcgui.ListItem(name, thumbnailImage=thumb, path=http+video+" live=true")
		item.setProperty('mimetype', 'video/x-flv')
		#xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(http+video+" live=true", item)
		#liveplayer.play(http+video+" live=true",item,False)
		#while liveplayer._playbackLock.isSet():
		#	xbmc.sleep(250)
		LivePlayer().PlayStream(http+video,thumb,name)
	

def list_main(url):
	response=getUrl(url)
	match_videos=re.compile('<div class="browse_video browse cfx">(.+?)</div>', re.DOTALL).findall(response)
	for video in match_videos:
		print video
		match_thumb=re.compile('src="(.+?)"', re.DOTALL).findall(video)
		match_url=re.compile('<a href="(.+?)" class="video_thumb">', re.DOTALL).findall(video)
		match_desc=re.compile('<p class="description">(.+?)</p>', re.DOTALL).findall(video)
		match_name=re.compile('data-json=".+?">(.+?)</a></h3>', re.DOTALL).findall(video)
		name = match_name[0].replace('Dorkly Bits: ','')
		addLink(name,baseurl+match_url[0],2,match_thumb[-1])

	match_next=re.compile('<a class="next" href="(.+?)">', re.DOTALL).findall(response)
	addDir('Next Page',baseurl+match_next[0],1,'')
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



def getUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#	if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#		print 'Try to use X-Forwarded-For trick'
	req.add_header('X-Forwarded-For', xip)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	return link

def getUrlCookie( url , extraheader=True,referer=None,host=None,if_none_match=None,get_etag=False):
	url = url.replace('&amp;','&')
	log('Getting url with cookie: '+url)

	cj = cookielib.LWPCookieJar()
	if os.path.isfile(COOKIEFILE):
		cj.load(COOKIEFILE, ignore_discard=True)

	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:19.0) Gecko/20100101 Firefox/19.0')]
	opener.addheaders = [('X-Forwarded-For', xip)]
	#opener.addheaders = [('Host', 'ad.smartclip.net')]
	if host != None:
		log('host')
		opener.addheaders = [('Host', host)]
	if referer != None:
		opener.addheaders = [('Referer', referer)]
	if if_none_match != None:
		opener.addheaders = [('If-None-Match', if_none_match)]
	opener.addheaders = [('Host', 'streamaccess.unas.tv')]
	opener.addheaders = [('Referer', 'http://www.laola1.tv/swf/hdplayer.13032013.swf')]
	#opener.addheaders = [('If-None-Match', '7930dbc81a35eff70ab82a8ae226a082:1363609713')]
		
	"""
	opener.addheaders = [('Referer', 'http://www.vevo.com'),
			 ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;)')]

	if extraheader:
	opener.addheaders = [('X-Requested-With', 'XMLHttpRequest')]
	if addoncompat.get_setting('location')==1:
	opener.addheaders = [('X-Forwarded-For', '12.13.14.15')]
	"""
	usock=opener.open(url)
	response=usock.read()
	try:
		etag = usock.info().getheader('Etag')
		etag = etag.replace('"','')
	except:
		pass
	usock.close()
	#if os.path.isfile(COOKIEFILE):
	cj.save(COOKIEFILE, ignore_discard=True)
	"""
	if get_etag == True:
		log('Etag is'+etag)
		return response,etag
	"""
	print response
	return response

def char_gen(size=1, chars=string.ascii_uppercase):
	return ''.join(random.choice(chars) for x in range(size))

def addLinkOld(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addLink(name,url,mode,iconimage,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name , "Plot": plot , "Plotoutline": plot } )
	liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	return ok
	
def addLinkFan(name,url,mode,iconimage,fanart):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('IsPlayable', 'true')
	liz.setProperty('fanart_image',fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
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
        LIST_VOD(url)

elif mode==2:
        print ""+url
        PLAY_VOD(url,name)
		
elif mode==3:
        print ""+url
        LIST_LIVE(url)
		
elif mode==4:
        print ""+url
        PLAY_LIVE(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
