# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui


pluginhandle = int(sys.argv[1])

baseurl = 'http://www.dorkly.com'


def MAIN():
	list_main(baseurl+'/originals')


def MAIN_NEXT(url):#1
	list_main(url)


def PLAY(url,name):#2
	match_id=re.compile('www.dorkly.com/video/(.+?)/', re.DOTALL).findall(url)
	response=getUrl('http://www.dorkly.com/moogaloop/video/'+match_id[0])
	match_video=re.compile('<file><!\[CDATA\[(.+?)\]\]></file>', re.DOTALL).findall(response)
        listitem = xbmcgui.ListItem(path=match_video[0])
        return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

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
        MAIN_NEXT(url)

elif mode==2:
        print ""+url
        PLAY(url,name)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
