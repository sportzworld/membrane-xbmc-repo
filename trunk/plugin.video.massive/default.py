# -*- coding: latin-1 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,cookielib

pluginhandle = int(sys.argv[1])


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))


#req = urllib2.Request('http://www.massive-mag.tv/user/preferences/set/videoformat/wmv/TV-Channel/Mag')
#req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#response = opener.open(req)
#link=response.read()
#response.close()

#print link
                       
def INDEX():
	req = urllib2.Request('http://www.massive-mag.tv/TV-Channel')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	#opener.addheaders.append(('Cookie', 'cookiename=cookievalue'))
        response = urllib2.urlopen(req)
#        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	match=re.compile('<div class="videothumbnail".+?<a href="(.+?)".+?<img src="(.+?)".+?title="(.+?)"', re.DOTALL).findall(link) 
        for url,thumb,name in match:
                addLink(name+' Channel','http://www.massive-mag.tv/user/preferences/set/videoformat/wmv'+url,2,'http://www.massive-mag.tv'+thumb)

	req = urllib2.Request('http://www.massive-mag.tv/Videos')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	match=re.compile('<div class="videothumbnail".+?<a href="(.+?)".+?<img src="(.+?)".+?title="(.+?)"', re.DOTALL).findall(link) 
        for url,thumb,name in match:
                addDir(name+' Videos','http://www.massive-mag.tv'+url,3,'http://www.massive-mag.tv'+thumb)


def PLAY_LIVE(url,name):#name#1
	print 'TODO'

def PLAY_CHANNEL(url,name):#2
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = opener.open(req)
        link=response.read()
        response.close()
#	print link
        match_streams=re.compile('<center>(.+?)</center>', re.DOTALL).findall(link) 
        match_stream=re.compile("'(.+?)'", re.DOTALL).findall(match_streams[0])

	if xbmcplugin.getSetting(pluginhandle,"quality") == '2':
		stream = match_stream[2]

	elif xbmcplugin.getSetting(pluginhandle,"quality") == '1':
		stream = match_stream[1]

	elif xbmcplugin.getSetting(pluginhandle,"quality") == '0':
		stream = match_stream[0] 

	item = xbmcgui.ListItem(path=stream)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)

def LIST_VIDEOS(url):#3
	req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	match=re.compile('<div class="videothumbnail".+?<a href="(.+?)".+?<img src="(.+?)".+?title="(.+?)"', re.DOTALL).findall(link) 
        for url,thumb,name in match:
                addLink(name,'http://www.massive-mag.tv/user/preferences/set/videoformat/wmv'+url,4,'http://www.massive-mag.tv'+thumb)
	match_next=re.compile('<span class="next"><a href="(.+?)">').findall(link) 
	addDir('Next','http://www.massive-mag.tv'+match_next[0],3,'')

def PLAY_VIDEOS(url,name):#4
	print '#####url##### '+url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = opener.open(req)
        link=response.read()
        response.close()
        match_videos=re.compile('<center>(.+?)</center>', re.DOTALL).findall(link) 
        match_video=re.compile("'(.+?)'", re.DOTALL).findall(match_videos[0])

	if xbmcplugin.getSetting(pluginhandle,"quality") == '2':
		video = match_video[2]

	elif xbmcplugin.getSetting(pluginhandle,"quality") == '1':
		video = match_video[1]

	elif xbmcplugin.getSetting(pluginhandle,"quality") == '0':
		video = match_video[0] 

	item = xbmcgui.ListItem(path=video)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)

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
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)##
	ok=True##
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)##
	liz.setInfo( type="Video", infoLabels={ "Title": name } )##
	liz.setProperty('IsPlayable', 'true')##
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)##
	return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

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
        INDEX()
       
elif mode==1:
        print ""+url
        PLAY_LIVE(url,name)
        
elif mode==2:
        print ""+url
        PLAY_CHANNEL(url,name)            

elif mode==3:
        print ""+url
        LIST_VIDEOS(url)

elif mode==4:
        print ""+url
        PLAY_VIDEOS(url,name)
  
xbmcplugin.endOfDirectory(int(sys.argv[1]))
