# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui


pluginhandle = int(sys.argv[1])

baseurl = 'http://www.bundestag.de'


def MAIN():
	addDir('Live',baseurl+'/Mediathek/index.jsp?action=tv',1,'')
	#addDir('Neuste Videos',baseurl+match_next[0],1,'')

	response=getUrl(baseurl+'/Mediathek/')
	match_auswahl=re.compile('<div class="mediathekVL">(.+?)<div class="mediathekBorder">', re.DOTALL).findall(response)
	match_themen=re.compile('<div class="mediathekVLBlock(.+?)Videos', re.DOTALL).findall(match_auswahl[0])
	for thema in match_themen:
		match_thumb=re.compile('<img src="(.+?)"', re.DOTALL).findall(thema)
		match_name=re.compile('<h2>(.+?)</h2>', re.DOTALL).findall(thema)
		match_desc=re.compile('<p>(.+?)</p>', re.DOTALL).findall(thema)
		match_url=re.compile('<a href="(.+?)"', re.DOTALL).findall(thema)
		url = baseurl+'/Mediathek/index.jsp'+match_url[0].replace('&amp;','&')

		if match_name[0] == 'Plenarsitzungen':#wechselt, beobachten!
			addDir(match_name[0],url,4,baseurl+match_thumb[-1])
		else:
			addDir(match_name[0],url,3,baseurl+match_thumb[-1])


def LIVE(url):#1
	addLink('Kanal 1','http://webtv.bundestag.de/player/_x_/xasx_live.xml',2,'')
	addLink('Kanal 2','http://webtv.bundestag.de/player/_x_/xasx_live_ch2.xml',2,'')
	"""


	response=getUrl(baseurl+'/Mediathek/index.jsp?action=tv')
	match_chan=re.compile('<div class="mediathekVideoText liveTvText">(.+?)</div>', re.DOTALL).findall(response)
	n='1'

	for channel in match_chan:
		match_name=re.compile('<br />(.+?)</h2>', re.DOTALL).findall(thema)
		match_desc=re.compile('<p>(.+?)</p>', re.DOTALL).findall(thema)

		addLink('Kanal '+n+': '+match_name[0]+' - '+match_desc[0],baseurl+match_next[0],2,baseurl+'/includes/datasources/stream_0'+n+'.jpg')

		n='2'
	"""

def PLAY_LIVE(url,name):#2
	response=getUrl(url)
	match_video=re.compile('<video width="512" height="288" href="(.+?)" bandwidth=".+?"/>').findall(response)
	video = match_video[-1]
	bananasplit = video.split('/')#rtmp://x3777parlac13014.f.l.f.lb.core-cdn.net/13014bundestag/live/3777parlamentsfernsehen/live_1000.flv

	playpath = bananasplit[-3]+'/'+bananasplit[-2]+'/'+bananasplit[-1].replace('.flv','')
	app = bananasplit[-4]

	#video=match_video[0]+' swfurl=http://webtv.bundestag.de/iptv/swf/xflv/showIt3_10.swf' + ' swfvfy=true app=13014bundestag/live'
	video=match_video[0]+' swfurl=http://webtv.bundestag.de/iptv/swf/xflv/showIt3_10.swf' + ' swfvfy=true pageUrl=http://www.bundestag.de live=true'+' app='+app+' playpath='+playpath
	#' app=13014bundestag playpath=live/3777parlamentsfernsehen/live_1000'
        listitem = xbmcgui.ListItem(path=video)
        return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)


def THEMEN(url):#3
	response=getUrl(url)
	match_list=re.compile('<ul class="mediathekUebersichtListe">(.+?)</ul>', re.DOTALL).findall(response)
	match_entry=re.compile('<li>(.+?)</li>', re.DOTALL).findall(match_list[0])

	for entry in match_entry:
		match_thumb=re.compile('<img src="(.+?)"', re.DOTALL).findall(entry)
		match_name=re.compile('<div class="mediathekSETitel"><p>(.+?)</p>', re.DOTALL).findall(entry)
		match_desc=re.compile('<div class="mediathekSEText"><p>(.+?)</p>', re.DOTALL).findall(entry)
		match_url=re.compile('<div class="mediathekSELink"><a href="(.+?)"', re.DOTALL).findall(entry)
		url = baseurl+'/Mediathek/index.jsp'+match_url[0].replace('&amp;','&')
		name = replace(match_name[0])

		if baseurl in match_thumb[0]:
			thumb = match_thumb[0]
		else:
			thumb = baseurl+match_thumb[0]

		addLink(name,url,5,thumb)

	match_next=re.compile('<a href="(.+?)" title="Ergebnisliste weiter">').findall(response)

	for next in match_next:
		url = baseurl+'/Mediathek/index.jsp'+next.replace('&amp;','&')
		addDir('Nächste Seite',url,3,'')



def THEMEN_PLENAR(url):#4
	try:
		response=getUrl(url)
		match_list=re.compile('<div class="mediathekPlenarErgebnisse">(.+?)<div class="mediathekBorder">', re.DOTALL).findall(response)
		match_entry=re.compile('<div class=.+?mediathekPlenarItem">(.+?)<br class="clear" />', re.DOTALL).findall(match_list[0])

		for entry in match_entry:
			match_thumb=re.compile('<img src="(.+?)"', re.DOTALL).findall(entry)
			match_name=re.compile('<h2><a href=".+?">(.+?)</a>', re.DOTALL).findall(entry)
			match_desc=re.compile('<strong> (.+?) </strong>', re.DOTALL).findall(entry)
			match_url=re.compile('<a href="(.+?)"', re.DOTALL).findall(entry)
			url = baseurl+'/Mediathek/index.jsp'+match_url[0].replace('&amp;','&')
			name = replace(match_name[0]+' - '+match_desc[0])
			addLink(name,url,5,baseurl+match_thumb[0])

		match_next=re.compile('<a href="(.+?)" title="Ergebnisliste weiter">').findall(response)

		for next in match_next:
			url = baseurl+'/Mediathek/index.jsp'+next.replace('&amp;','&')
			addDir('Nächste Seite',url,4,'')
	except:
		THEMEN(url)


def PLAY_THEMEN(url,name):#5
	response=getUrl(url)
	match_video=re.compile('data-downloadurl="(.+?)"', re.DOTALL).findall(response)
        listitem = xbmcgui.ListItem(path=match_video[0])
        return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def replace(name):
	name = name.replace('&quot;','"')
	name = name.replace('&uuml;','ü')
	name = name.replace('&auml;','ä')
	name = name.replace('&ouml;','ö')
	name = name.replace('&ndash;','-')
	return name

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
#		req.add_header('X-Forwarded-For', xip)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	return link


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
        LIVE(url)

elif mode==2:
        print ""+url
        PLAY_LIVE(url,name)

elif mode==3:
        print ""+url
        THEMEN(url)

elif mode==4:
        print ""+url
        THEMEN_PLENAR(url)

elif mode==5:
        print ""+url
        PLAY_THEMEN(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
