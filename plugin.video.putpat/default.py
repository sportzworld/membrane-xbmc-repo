# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,cookielib


pluginhandle = int(sys.argv[1])
__settings__ = xbmcaddon.Addon(id='plugin.video.putpat')
addon = xbmcaddon.Addon(id='plugin.video.putpat')
COOKIEFILE = xbmc.translatePath(addon.getAddonInfo('path')+"/cookies.lwp")

baseurl = 'http://www.putpat.tv'

mainreq = urllib2.Request(baseurl+'/ws.xml?method=Initializer.putpatPlayer&client=putpatplayer&streamingMethod=rtmp&partnerId=1')
mainreq.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
mainresponse = urllib2.urlopen(mainreq)
mainlink=mainresponse.read()
mainresponse.close()

match_channels=re.compile('<channel>(.+?)</channel>', re.DOTALL).findall(mainlink)
channels = match_channels


def MAIN():
	for channel in match_channels:
	
		try:
			match_info=re.compile('<channel-info>(.+?)</channel-info>').findall(channel)
			info = match_info[0]
		except:
			info = 'Scraping Fehler, bitte melden ;)'	
			
		try:
			match_message=re.compile('<channel-message>(.+?)</channel-message>').findall(channel)
			message = match_message[0]
		except:
			message = 'Scraping Fehler, bitte melden ;)'	
			
		try:
			match_artists=re.compile('<played-artists>(.+?)</played-artists>', re.DOTALL).findall(channel)
			artists = match_artists[0]
		except:
			artists = 'Scraping Fehler, bitte melden ;)'	
			
		try:
			match_integer=re.compile('<id type="integer">(.+?)</id>', re.DOTALL).findall(channel)
			integer = match_integer[0]
		except:
			integer = 'Scraping Fehler, bitte melden ;)'				
			
		try:
			match_tags=re.compile('<tags>(.+?)</tags>').findall(channel)
			tags = match_tags[0]
		except:
			tags = 'Scraping Fehler, bitte melden ;)'	
			
		try:
			match_title=re.compile('<title>(.+?)</title>').findall(channel)
			title = match_title[0]
		except:
			title = 'Scraping Fehler, bitte melden ;)'
			
		try:
			match_urlchannel=re.compile('<url-channel-name>(.+?)</url-channel-name>').findall(channel)
			urlchannel = match_urlchannel[0]
		except:
			urlchannel = 'Scraping Fehler, bitte melden ;)'

		try:
			match_channelid=re.compile('<id type="integer">(.+?)</id>').findall(channel)
			channelid = match_channelid[0]
		except:
			channelid = 'Scraping Fehler, bitte melden ;)'

		
		name = fix_name(title + ' - ' + message)
		thumb = 'http://files.putpat.tv/artwork/channelgraphics/'+integer+'/channellogo_invert_500.png'
		url = 'http://www.putpat.tv/ws.xml?method=Channel.clips&client=putpatplayer&streamingMethod=http&streamingId=tvrl&channelId='+channelid+'&maxClips=5&partnerId=1'
		addLinkFan(name,url,1,thumb,'http://files.putpat.tv/putpat_player/231/assets/putpat_splashscreen.jpg')

		

def PLAY(url):#1
	#dummy entry, workaround

	#pl=xbmc.PlayList(1)
	#pl.clear()

	#item = xbmcgui.ListItem('Dummy entry',thumbnailImage='')
	#xbmc.PlayList(1).add('', item)
	"""
	ad = 'true'
	print '####################################################ad: '
	print ad
	if ad == 'true':
		video = get_ad()
		print video
		item = xbmcgui.ListItem('Werbung',thumbnailImage='')
		item.setProperty('mimetype', 'video/mp4')
		xbmc.PlayList(1).add(video, item)
	"""

	response = getUrl(url)
	match_clips=re.compile('<clip>(.+?)</clip>', re.DOTALL).findall(response)

	

	#xbmc.sleep(500)
	for entry in match_clips:
		try:
			match_title=re.compile('<title>(.+?)</title>').findall(entry)
			title = match_title[-1]	
		except:
			title = 'Scraping Fehler, bitte melden ;)'
			
		try:
			match_author=re.compile('<display-artist-title>(.+?)</display-artist-title>').findall(entry)
			author = match_author[0]
		except:
			author = 'Scraping Fehler, bitte melden ;)'
			
		try:
			if xbmcplugin.getSetting(pluginhandle,"quality") == '2':
				match_video = match_high=re.compile('<medium>(.+?)</medium>').findall(entry)
	
			elif xbmcplugin.getSetting(pluginhandle,"quality") == '1':
				match_video = match_high=re.compile('<low>(.+?)</low>').findall(entry)
				
			elif xbmcplugin.getSetting(pluginhandle,"quality") == '0':
				match_video = match_high=re.compile('<preview>(.+?)</preview>').findall(entry)
				
			video = match_video[0].replace('&amp;','&')
		except:
			video = 'Scraping Fehler, bitte melden ;)'

		try:
			match_thumb=re.compile('http://tv.putpat.tv/(.+?)_').findall(video)
			thumb = 'http://files.putpat.tv/artwork/posterframes/'+match_thumb[0]+'_posterframe_putpat_small.jpg'
		except:
			thumb = 'Scraping Fehler, bitte melden ;)'

		###rtmp stuff, use http for now
		"""
		try:
			match_token=re.compile('<token>(.+?)</token>').findall(entry)
			token = match_token[0]
		except:
			token = 'Scraping Fehler, bitte melden ;)'
			
		try:
			match_duration=re.compile('<duration Value="(.+?)" />').findall(entry)
			duration = match_duration[0]
		except:
			duration = 'Scraping Fehler, bitte melden ;)'
			
			
		match_token=re.compile('token=(.+?)=').findall(video)
		token = '?token='+match_token[0]+'='
		
		match_mp4=re.compile('mp4(.+?)mp4').findall(video)
		mp4 = 'mp4'+match_mp4[0]+'mp4'
		
		url = 'rtmp://tvrlfs.fplive.net/tvrl/ playpath='+mp4+token+' swfurl=http://files.putpat.tv/putpat_player/231/PutpatPlayer.swf swfvfy=true pageUrl=http://www.putpat.tv/'
		"""
		print '######################add video'
		print author
		print title
		print thumb
		print video
		if not 'v&#246; folgt!' in title:
			name = author + ' - ' + title
		else:
			name = author
		item = xbmcgui.ListItem(fix_name(name),thumbnailImage=thumb)
		item.setProperty('mimetype', 'video/mp4')
		xbmc.PlayList(1).add(video, item)

	print 'plugin://plugin.video.putpat/?mode=2&url='+enc_url(url)
	item = xbmcgui.ListItem('Werbung',thumbnailImage='')
	xbmc.PlayList(1).add('plugin://plugin.video.putpat/?mode=2&url='+enc_url(url), item)

	#item = xbmcgui.ListItem('More',thumbnailImage='')
	#xbmc.PlayList(1).add('plugin://plugin.video.putpat/?url='+enc_url(url)+'&mode=1&ad=true', item)
	
	

	
	#xbmc.Player().play(pl)



def PLAY_AD(url):#2

	#pl=xbmc.PlayList(1)
	#pl.clear()

	#item = xbmcgui.ListItem('Dummy entry',thumbnailImage='')
	#xbmc.PlayList(1).add('', item)
	try:
		video = get_ad()
	except:
		video = ''

	item = xbmcgui.ListItem('Werbung',thumbnailImage='')
	item.setProperty('mimetype', 'video/mp4')
	xbmc.PlayList(1).add(video, item)

	item = xbmcgui.ListItem('More',thumbnailImage='')
	xbmc.PlayList(1).add('plugin://plugin.video.putpat/?url='+enc_url(url)+'&mode=1', item)


def get_ad():
	response = getUrl('http://www.putpat.tv/ws.xml?partnerId=1&method=Marketing.urls&client=putpatplayer&type=preroll')
	match=re.compile('<url>(.+?)</url>').findall(response)

	split = match[0].split('nuggl=')
	split = dec_url(split[-1])
	dummyresponse = getUrlCookie(match[0])
	response = getUrlCookie(split)
	match_MediaFiles=re.compile('<MediaFiles>(.+?)</MediaFiles>', re.DOTALL).findall(response)
	print match_MediaFiles[0]
	match_URL=re.compile('<URL>.+?CDATA\[(.+?)\]').findall(match_MediaFiles[0])
	return match_URL[-1]


			

def enc_url(url):
	url = url.replace(':','%3A')
	url = url.replace('/','%2F')
	url = url.replace('?','%3F')
	url = url.replace('=','%3D')
	url = url.replace('&','%26')
	url = url.replace('<','%3C')
	url = url.replace('>','%3E')
	return url

def dec_url(url):
	url = url.replace('%3A',':')
	url = url.replace('%2F','/')
	url = url.replace('%3F','?')
	url = url.replace('%3D','=')
	url = url.replace('%26','&')
	return url

def fix_name(name):
	name = name.replace('&amp;','&')
	name = name.replace('&#252;','ü')
	name = name.replace('&#246;','ö')
	name = name.replace('&#196;','A')
	return name

def getUrl(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link


def getUrlCookie( url , extraheader=True):
    cj = cookielib.LWPCookieJar()
    if os.path.isfile(COOKIEFILE):
        cj.load(COOKIEFILE, ignore_discard=True)

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:20.0) Gecko/20121202 Firefox/20.0')]
    opener.addheaders = [('Host', '71iv.nuggad.net')]
    opener.addheaders = [('Referer', 'http://files.putpat.tv/putpat_player/265/PutpatPlayer.swf')]
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
    usock.close()
    #if os.path.isfile(COOKIEFILE):
    cj.save(COOKIEFILE, ignore_discard=True)
    return response




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




def addLinkOld(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addLink(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
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
        PLAY(url)

elif mode==2:
        print ""+url
        PLAY_AD(url)




xbmcplugin.endOfDirectory(int(sys.argv[1]))
