# -*- coding: iso-8859-1 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui

pluginhandle = int(sys.argv[1])

baseurl = 'http://www.sat1.de'

if xbmcplugin.getSetting(pluginhandle,"hd_logo") == '0':
	hd_logo = "0"
elif xbmcplugin.getSetting(pluginhandle,"hd_logo") == '1':
	hd_logo = "1"


def CATEGORIES():
        req = urllib2.Request(baseurl+'/tv')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	match_section=re.compile('<section class="shows_box module_group">(.+?)</section>', re.DOTALL).findall(link)
        for section in match_section:
#		print section
        	match_shows=re.compile('<figure>.+?href="(.+?)".+?src="(.+?)".+?alt="(.+?)"', re.DOTALL).findall(section)
		for url,thumb,name in match_shows:
			name = name.replace('haraldschmidt-citylight','Die Harald Schmidt Show')#TODO: auch die anderen Sendungen so umbenennen
                	addDir(name,baseurl+url+'/video',1,baseurl+thumb)



def VIDEOLINKS(url):#1
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	match_videos=re.compile('<div class="video_teaser trackable_teaser">(.+?)</div>', re.DOTALL).findall(link)
	for video in match_videos:
		match_video=re.compile('<a href="(.+?)".+?src="(.+?)".+?title="(.+?)"', re.DOTALL).findall(video)
		for url,thumb,name in match_video:
                	addLink(name,baseurl+url,2,thumb)#TODO: naechste seite
		


                
def PLAY(url,name):#2
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

	if '"geoblocking":"ww"' in link:
		rtmp = 'rtmp://pssimsat1fs.fplive.net/pssimsat1ls/geo_worldwide/'
		app = ' app=pssimsat1ls/geo_worldwide'

	if '"geoblocking":"de_at_ch"' in link:
		rtmp = 'rtmp://pssimsat1fs.fplive.net/pssimsat1ls/geo_d_at_ch/'
		app = ' app=pssimsat1ls/geo_d_at_ch'

	if '"geoblocking":"de"' in link:
		rtmp = 'rtmp://pssimsat1fs.fplive.net/pssimsat1ls/geo_d/'
		app = ' app=pssimsat1ls/geo_d'

        match_playpath=re.compile('"downloadFilename":"(.+?)"').findall(link)
	playpath = ' playpath=mp4:'+match_playpath[0]

	swfurl =' swfurl=http://www.sat1.de/static/videoplayer/prod/gvp_all_2012-02-06/player/loader/1.0.0-SNAPSHOT-sat1/MingLoader.swf'

	url = rtmp+playpath+swfurl+' swfVfy=true'+app+' pageUrl=http://www.sat1.de'
        item = xbmcgui.ListItem(path=url)
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
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
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
        CATEGORIES()
       
elif mode==1:
        print ""+url
        VIDEOLINKS(url)

elif mode==2:
        print ""+url
        PLAY(url,name)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
