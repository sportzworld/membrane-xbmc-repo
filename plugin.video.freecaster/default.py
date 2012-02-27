# -*- coding: latin-1 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui

pluginhandle = int(sys.argv[1])


if xbmcplugin.getSetting(pluginhandle,"sort") == '0':
	sort = 'latest'

elif xbmcplugin.getSetting(pluginhandle,"sort") == '1':
	sort = 'top_all'

elif xbmcplugin.getSetting(pluginhandle,"sort") == '2':
	sort = 'top_1d'

elif xbmcplugin.getSetting(pluginhandle,"sort") == '3':
	sort = 'top_7d'

elif xbmcplugin.getSetting(pluginhandle,"sort") == '4':
	sort = 'top_30d'




                       
def INDEX():
	addDir('Auto Sports','/autosports',1,'')
	addDir('BMX','/bmx',1,'')
	addDir('FMX','/fmx',1,'')
	addDir('Freeski','/freeski',1,'')
	addDir('Kayak','/kayak',1,'')
	addDir('Kitesurf','/kite',1,'')
	addDir('MTB','/mountainbike',1,'')
	addDir('Outdoor','/outdoor',1,'')
	addDir('MX','/mx',1,'')
	addDir('Skate','/skate',1,'')
	addDir('Snowboard','/snowboard',1,'')
	addDir('Supermoto','/supermoto',1,'')
	addDir('Surf','/surf',1,'')
	addDir('Wake','/wake',1,'')
	addDir('Windsurf','/windsurf',1,'')


                
def TOPICSELECTION_A(url):
	addDir('News','http://extreme.com'+url+'?tab=news&ajax=1&filter='+sort+'&ajax=1',2,'')
	addDir('Pro Videos','http://extreme.com'+url+'?tab=pro&ajax=1&filter='+sort+'&ajax=1',2,'')
	addDir('Member Videos','http://extreme.com'+url+'?tab=member&ajax=1&filter='+sort+'&ajax=1',2,'')
	#http://freecaster.tv/autosports?filter=latest&ajax=1&ajax=1
        req = urllib2.Request('http://extreme.com'+url+'?filter='+sort+'&ajax=1&ajax=1')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li class="node_item video "><a href="(.+?)" class=".+?"><img class=".+?" src="(.+?)" .+? title="(.+?)" />').findall(link) 
	match_next=re.compile('<a href="(.+?)">next&nbsp;&raquo;</a>').findall(link) 

        for url,thumb,name in match:
                addLink(name,'http://extreme.com'+url,3,thumb)
	for next in match_next:
		addDir('Next','http://extreme.com'+next,2,'')


def TOPICSELECTION_B(url):
	#http://freecaster.tv/autosports?filter=latest&ajax=1&ajax=1
        req = urllib2.Request(url+'?filter='+sort+'&ajax=1&ajax=1')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li class="node_item video"><a href="(.+?)" class=".+?"><img class=".+?" src="(.+?)" .+? title="(.+?)" />').findall(link) 
	match_next=re.compile('<a href="(.+?)">next&nbsp;&raquo;</a>').findall(link) 

        for url,thumb,name in match:
                addLink(name,'http://extreme.com'+url,3,thumb)
	for next in match_next:
		addDir('Next','http://extreme.com'+next,2,'')


def VIDEOLINKS(url,name):
	#http://player.freecaster.com/info/dj0xMDE3MzUxJmM9MTAwMDE3OQ?source=freecaster&source%5Furl=http%3A%2F%2Ffreecaster%2Etv%2Fautosports%2F1017351%2Fdc%2Dshoes%2Dgymkhana%2Dfour%2Dwith%2Dken%2Dblock%2Dthe%2Dhollywood%2Dmegamercia
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
#        match_id=re.compile('<param name="flashvars" value="id=(.+?)&').findall(link)
        match_id=re.compile('<meta property="og:video" content="http://player.extreme.com/FCPlayer.swf\?id=(.+?)&').findall(link)

        req = urllib2.Request('http://player.extreme.com/info/'+match_id[0]+'?source=freecaster&source%5Furl='+url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	print 'got stream links'

	match_streams=re.compile('<streams type="(.+?)"(.+?)</streams>', re.DOTALL).findall(link)
	for streamtype,streams in match_streams:
		print "streamtype[0]: "+streamtype[0]
		print match_streams[0]
		if "youtu" in streams:
			match_videoid=re.compile('http://youtu.be/(.+?)</stream>').findall(streams)
			print "youtube video:"+match_videoid[0]
			play_youtube_video(match_videoid[0], name)
			"""
			#plugin://plugin.video.youtube?path=/root&action=play_video&videoid=
			url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % (match_videoid[0])
#			item = xbmcgui.ListItem(path=url)

			listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=url )
			infolabels = { "title": name, "plot": name}

			listitem.setInfo( type="Video", infoLabels=infolabels)
			xbmc.Player( xbmc.PLAYER_CORE_DVDPLAYER ).play( str(url), listitem)
			"""
#			return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
#			item = xbmcgui.ListItem(path=rtmp+video+' swfurl=http://player.freecaster.com/FCPlayer.swf?id='+match_id[0]+' swfvfy=true')
#			return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
		else:
			match_video=re.compile('<stream quality=".+?" ref=".+?" label=".+?" bitrate=".+?" width=".+?" height=".+?" duration=".+?">(.+?)</stream>').findall(streams)
			match_rtmp=re.compile('server="(.+?)"').findall(streams)
	
			if xbmcplugin.getSetting(pluginhandle,"quality") == '3':
				video = match_video[-1]
	
			elif xbmcplugin.getSetting(pluginhandle,"quality") == '2':
				video = match_video[2]
	
			elif xbmcplugin.getSetting(pluginhandle,"quality") == '1':
				video = match_video[1]
	
			elif xbmcplugin.getSetting(pluginhandle,"quality") == '0':
				video = match_video[0]
			url=match_rtmp[0]+video
			item = xbmcgui.ListItem(path=url)
#			item = xbmcgui.ListItem(path=match_rtmp[0]+video+' swfurl=http://player.freecaster.com/FCPlayer.swf?id='+match_id[0]+' swfvfy=true')
			return xbmcplugin.setResolvedUrl(pluginhandle, True, item)


def play_youtube_video(video_id, name):
        print ("Playing video " + name + " id: " + video_id)
        url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % (video_id)
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=url )
        infolabels = { "title": name, "plot": name}
        listitem.setInfo( type="Video", infoLabels=infolabels)
        xbmc.Player( xbmc.PLAYER_CORE_DVDPLAYER ).play( str(url), listitem)


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
        TOPICSELECTION_A(url)
        
elif mode==2:
        print ""+url
        TOPICSELECTION_B(url)            

elif mode==3:
        print ""+url
        VIDEOLINKS(url,name)

  
xbmcplugin.endOfDirectory(int(sys.argv[1]))
