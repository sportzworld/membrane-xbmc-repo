# -*- coding: utf8 -*-

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,base64,socket,sys,string,random,cookielib,httplib,base64



__settings__ = xbmcaddon.Addon(id='plugin.video.ran')
#__settings__ = xbmcaddon.Addon()
__language__ = __settings__.getLocalizedString

#xbmc.PLAYER_CORE_MPLAYER

pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.ran')

base_url = 'http://www.ran.de'



###set strings

scommercial = __language__(30002)
snotstarted = __language__(30003)
sstartsat = __language__(30004)
sat = __language__(30005)
scet = __language__(30006)


#xip = xbmcplugin.getSetting(pluginhandle,"ip")
#print 'xip: '+xip
                       
#if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#	print 'laola: use trick'







def INDEX():
	#name,thumb = get_livedata(base_url+'/de/index.html')
	addLinkOld('Livestream 1','rtmp://soran2livefs.fplive.net:1935/soran2live-live swfurl=http://is.myvideo.de/player/GP/2.8.8/player.swf swfvfy=true pageUrl=http://www.ran.de playpath=ran live=true','')
	addLinkOld('Livestream 2','rtmp://pssims1flashlivefs.fplive.net:1935/pssims1flashlive-live swfurl=http://is.myvideo.de/player/GP/3.0.0/player.swf swfvfy=true pageUrl=http://www.ran.de playpath=pssims1flashlive-stream01 live=true','')

        #addDir('Live',base_url+'/de/index.html',1,'')
	"""
        response = getUrl(videos_url)

        match=re.compile('<div id="sitemap"><a (.+?)</div>').findall(response)

        for something in match:
                match1=re.compile('href="(.+?)".*?>(.+?)</a>').findall(something)
                for url,name in match1 or match2:
                        addDir(name,url,1,'')
	"""


def get_livedata(url):
	response = getUrl(url)
	#print response
        match_all=re.compile('<div class="outer">(.+?)<div class="bueMid">', re.DOTALL).findall(response) 
	#print match_all[0]
        match_item=re.compile('<i(.+?)</li>', re.DOTALL).findall(match_all[0]) 
        for item in match_item:
		if 'JETZT im Livestream' in item:
			name = 'Jetzt Live: '
		elif 'Live' in item or 'LIVE' in item or 'live' in item:
			name = 'Kommender Livestream: '
		thumb = ''
        	match_thumb=re.compile('src="(.+?)".+?width="(.+?)"').findall(item) 
		for possible_thumb,width in match_thumb:
			if width == '794':
				thumb = possible_thumb

        	match_name=re.compile('<li><a href=".+?">(.+?)</a>').findall(item) 
        	match_url=re.compile('<li><a href="(.+?)">.+?</a>').findall(item) 

		if 'Live' in match_name[0] or 'LIVE' in match_name[0] or 'live' in match_name[0]:
			addLink(name+match_name[0],base_url+match_url[0],2,base_url+thumb)
		"""
		print item
		print base_url+match_url[0]
		print name+match_name[0]
		print thumb
		"""
                


def PLAY_LIVE(url,name,thumb=''):#2
	response = getUrl(url)

def enc_url(url):
	url = url.replace(':','%3A')
	url = url.replace('/','%2F')
	url = url.replace('?','%3F')
	url = url.replace('=','%3D')
	url = url.replace('&','%26')
	return url

                
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

def char_gen(size=1, chars=string.ascii_uppercase):
	return ''.join(random.choice(chars) for x in range(size))

def num_gen(size=1, chars=string.digits):
	return ''.join(random.choice(chars) for x in range(size))


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
    opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;)')]
    opener.addheaders = [('Host', 'ad.smartclip.net')]
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

def log(message):
	if debug == '1':
		print "#####Laola1 Debug: "+message
	return



def addLinkOld(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addLink(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&thumb="+urllib.quote_plus(iconimage)+"&name="+urllib.quote_plus(name)##
	ok=True##
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)##
	liz.setInfo( type="Video", infoLabels={ "Title": name } )##
	liz.setProperty('IsPlayable', 'true')##
	liz.setProperty('mimetype', 'video/x-flv')
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
link=None
thumb=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        name=urllib.unquote_plus(params["link"])
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
print "Thumbnail: "+str(thumb)

if mode==None or url==None or len(url)<1:
        print ""
        INDEX()
       
elif mode==1:
        print ""+url
        LIVE(url)
        
elif mode==2:
        print ""+url
        PLAY_LIVE(url,name,thumb)            


  
xbmcplugin.endOfDirectory(int(sys.argv[1]))
