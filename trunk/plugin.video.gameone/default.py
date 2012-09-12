# -*- coding: iso-8859-1 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui

pluginhandle = int(sys.argv[1])
#gameone
base_url = 'http://gameone.de'
def CATEGORIES():
        addDir('Alle Folgen','http://gameone.de/tv',1,'http://assets.gameone.de/images/element_bg/logo-game-one.png')
        addDir('Blog','http://gameone.de/blog',6,'http://assets.gameone.de/images/element_bg/logo-game-one.png')
        addDir('Playtube','http://gameone.de/playtube/',3,'http://assets.gameone.de/images/element_bg/logo-game-one.png')
        addDir('Podcast','http://www.gameone.de/specials/der-gameone-plauschangriff',9,'http://assets.gameone.de/images/element_bg/logo-game-one.png')
        
################################tv################################


def INDEX_TV(url):#1
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="/tv/(.+?)" class="image_link"><img alt=".+?" src="(.+?)" /></a>\n<h5>\n<a href=\'.+?\'.+?<p class=\'desc\'>(.+?)</p>', re.DOTALL).findall(link)
        #<a href="/tv/162" class="image_link"><img alt="156543_87ac3a65_mp4_640x480_1600" src="http://asset.gameone.de/gameone/assets/video_metas/teaser_images/000/618/246/featured/156543_87ac3a65_mp4_640x480_1600.mp4_cropped.jpg?1300200447" /></a><h5><a href='/tv/162' title='Flirtgewitter, Yakuza 4, Next'>GameOne - Folge 162</a>
        for folge,thumbnail,title in match:
		#if int(folge) > 101:
                addLink('Folge '+folge+' - '+title,folge,2,thumbnail)



def VIDEOLINKS_TV(folge):#2
	req = urllib2.Request('http://www.gameone.de/api/mrss/mgid%3Agameone%3Avideo%3Amtvnn.com%3Atv_show-'+folge)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile("<media:content.+?url='(.+?)'></media:content>").findall(link)
	for video_xml in match:
		req = urllib2.Request(video_xml)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link_video=response.read()
		response.close()

		swfurl = "http://media.mtvnservices.com/player/prime/mediaplayerprime.1.9.0.swf"
		match_video=re.compile('<src>(.+?)</src>').findall(link_video)

		url=match_video[-1]+' swfurl='+swfurl+' swfvfy=true' + " pageUrl=www.gameone.de app=ondemand?ovpfv=2.1.4"

		listitem = xbmcgui.ListItem(name,thumbnailImage='')
		xbmc.PlayList(1).add(url, listitem)
	
"""
	if int(folge) > 101:
		req = urllib2.Request('http://gameone.de/tv/'+folge)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		match_id=re.compile('riptide_video_id: "(.+?)"').findall(link)

		req = urllib2.Request("http://riptide.mtvnn.com/mediagen/"+match_id[0])
        	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        	response = urllib2.urlopen(req)
        	link=response.read()
        	response.close()
	
		swfurl = "http://media.mtvnservices.com/player/prime/mediaplayerprime.1.9.0.swf"

	else:
		print "alte videos"
		#alte videos (1-100)
		req = urllib2.Request('http://www.gameone.de/api/mrss/mgid%3Agameone%3Avideo%3Amtvnn.com%3Atv_show-'+folge)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		match=re.compile("<media:content.+?url='(.+?)'></media:content>").findall(link)

		for video in match:
			print "videocontainer: "+video
		req = urllib2.Request(match[0])
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		

		#swfurl = "http://media.mtvnservices.com/player/prime/mediaplayerprime.1.9.0.swf"
		swfurl = "http://media.mtvnservices.com/player/prime/"

	
	match=re.compile('<src>(.+?)</src>').findall(link)
	video=match[-1]+' swfurl='+swfurl+' swfvfy=true' + " pageUrl=www.gameone.de app=ondemand?ovpfv=2.1.4"
	item = xbmcgui.ListItem(path=video)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)






#        <video width="566" height="424" controls="controls" src="http://cdn.riptide-mtvn.com/production/0016/1260/161262_bff037dd_mp4_640x480_1400.mp4" 
#poster="http://asset.gameone.de/gameone/assets/video_metas/teaser_images/000/620/792/big/161262_bff037dd_mp4_640x480_1400.mp4_cropped.jpg?1306681883"></video>
        item = xbmcgui.ListItem(path=video)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
        #<param name="href" value="http://cdn.riptide-mtvn.com/production/0015/6542/156543_87ac3a65_mp4_640x480_1600.mp4" />
#        for url in match:
#                addLink('Play',url+'_mp4_640x480_1600.mp4','')

"""

################################playtube################################

                
def INDEX_PLAYTUBE(url):#3
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile("<ul class='channels'>(.+?)</ul>", re.DOTALL).findall(link)
        match=re.compile("<a class='name' href='(.+?)' title='(.+?)'>", re.DOTALL).findall(match[0])
	for url,title in match:
		addDir(title,url,4,'')

def CAT_PLAYTUBE(url):#4
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<h3><a href="(.+?)">(.+?)</a></h3>\n<p><a href=".+?">.+?</a></p>\n</div>\n<a href=".+?" class="img_link"><img alt=".+?" src="(.+?)" /></a>', re.DOTALL).findall(link)
        #<li class='odd teaser_medium'>
        #<div class='overlay team_video'>
        #<h3><a href="http://gameone.de/playtube/zurueck-in-die-zukunft-extended/616299">Zurück in die Zukunft Extended</a></h3>
        #<p><a href="http://gameone.de/playtube/zurueck-in-die-zukunft-extended/616299">&quot;Zurück in die Zukunft The Game Episode 1&quot; - Langer Titel, noch längerer &quot;Ext...</a></p>
        #
        #</div>
        #<a href="http://gameone.de/playtube/zurueck-in-die-zukunft-extended/616299" class="img_link"><img alt="153791_0ed79c30_mp4_640x480_1600" src="http://asset.gameone.de/gameone/assets/video_metas/teaser_images/000/616/299/medium/153791_0ed79c30_mp4_640x480_1600.mp4_cropped.jpg?1295845477" /></a>
        for url,name,thumbnail in match:
                #print 'video: '+name
                addLink(name,url,5,thumbnail)
        match_a=re.compile('<a href=(.+?)>').findall(link)
        #<a href="/playtube/channel/game-one-movies/6?page=2" class="next_page" rel="next">Nächste Seite</a></div>
        for href in match_a:
                #print 'hrefplaytube: '+href
                match_next=re.compile('"/playtube/channel/(.+?)" class="next_page" rel="next"').findall(href)
                for naechste_seite in match_next:
                        #print 'next'+naechste_seite
                        addDir('Nächste Seite','http://gameone.de/playtube/channel/'+naechste_seite,4,'')


def VIDEOLINKS_PLAYTUBE(url,name):#5
	video = get_video(get_video_ids(url)[0])
	item = xbmcgui.ListItem(path=video)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)

"""
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('hqv: "riptide/(.+?)"').findall(link)
        #var variables = { file: "riptide/production/0015/3789/153790_0ed79c30_flv_448x336_650.flv", streamer: "rtmp://cp8619.edgefcs.net/ondemand/", pageName: "gameone/zurueck-in-die-zukunft-extended", usehq: false, hqv: "riptide/production/0015/3789/153791_0ed79c30_mp4_640x480_1600.mp4", duration: "636.3", adson: true, autostart: false, configFile: "http://assets.gameone.de/flash/g2_player/config.xml?1289856314", image: "http://asset.gameone.de/gameone/assets/video_metas/teaser_images/000/616/299/big/153791_0ed79c30_mp4_640x480_1600.mp4_cropped.jpg?1295845477", available_profiles: [{"id":153792,"filename":"riptide/production/0015/3789/153792_0ed79c30_mp4_256x192_350.mp4","height":192,"width":256}], playername: "153790_video_meta_616299" };
        item = xbmcgui.ListItem(path='http://cdn.riptide-mtvn.com/'+match[0])
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
#        for url in match:
#                addLink('Play','http://cdn.riptide-mtvn.com/'+url,'')

"""
        
        

################################blog################################


def INDEX_BLOG(url):#6
	addDir('Alle',url,7,'')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match_teasers=re.compile('<ul class="teasers">(.+?)</ul>', re.DOTALL).findall(link)
	for teaser in match_teasers:
		match_cat=re.compile('<a title="(.+?)" href="(.+?)">.+?src="(.+?)"', re.DOTALL).findall(teaser)
		for title,url,thumb in match_cat:
			addDir(title,base_url+url,7,base_url+thumb)

def CAT_BLOG(url):#7




        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<h3><a href="(.+?)">(.+?)</a></h3>\n<p>.+?</p>\n<small>\nPosted:\n.+?\n</small>\n</div>\n<a class=\'image_link\' href=\'.+?\'>\n<img height=\'.+?\' src=\'(.+?)\' width=\'.+?\' />', re.DOTALL).findall(link)
        #<h3><a href="/blog/2011/3/30-minuten-mit-da-vincis-verschwinden">30 Minuten mit: Da Vincis Verschwinden</a></h3>
        #<p>"Assassin's Creed: Brotherhood" geht weiter!</p>
        #<small>
        #Posted:
        #Woody, Freitag, 25. März 2011, 13:21 Uhr
        #</small>
        #</div>
        #<a class='image_link' href='/blog/2011/3/30-minuten-mit-da-vincis-verschwinden'>
        #<img height='318' src='http://asset.gameone.de/gameone/assets/images/000/003/094/blog_list/Da-Vinci-Disappearance-Today.jpg?1301055077' width='566' />
        for url,name,thumb in match:
                addLink(name,url,8,thumb)
        match_a=re.compile('<a href=(.+?)>').findall(link)
        #match_a=re.compile('<a href=(.+?)>').findall(link)
        #<a href="/blog?page=2" class="next_page" rel="next">Nächste Seite</a>
        for href in match_a:
                #print 'hrefblog: '+href
                match_next=re.compile('"/blog(.+?)" class="next_page" rel="next"').findall(href)
                for naechste_seite in match_next:
                        #print 'next'+naechste_seite
                        addDir('Nächste Seite','http://gameone.de/blog'+naechste_seite,7,'')

def VIDEOLINKS_BLOG(url,name):#8
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('var so = new SWFObject.+?video_meta-(.+?)"').findall(link)
        #match18=re.compile('<img src="(.+?)dummy_agerated.jpg">').findall(link)
	if not match:
		print 'no video found'
		xbmc.executebuiltin("Notification('Title','Message')")
	else:
		for video_id in match:
			url = get_video(video_id)
			listitem = xbmcgui.ListItem(name,thumbnailImage='')
			xbmc.PlayList(1).add(url, listitem)
		        #addLinkOld('Play',get_video(video_id),'')
"""
	match=re.compile('<src>(.+?)</src>').findall(link)
	video=match[-1]+' swfurl='+swfurl+' swfvfy=true' + " pageUrl=www.gameone.de app=ondemand?ovpfv=2.1.4"
	item = xbmcgui.ListItem(path=video)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
"""



def INDEX_PODCAST(url):#9
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<p><a href="(.+?)"><img alt="(.+?)" src="(.+?)" /></a></p>', re.DOTALL).findall(link)
	for url,name,thumb in match:
		thumb = thumb.replace(' ','%20')
		if 'horror' in thumb:
			print "##############################"+thumb
		addLink(name,url,10,thumb)

def PLAY_PODCAST(url,name):#10
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<p><a href="(.+?)">Download', re.DOTALL).findall(link)

	podcast = match[0]
	item = xbmcgui.ListItem(path=podcast)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)


def get_video_ids(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        video_ids=re.compile('var so = new SWFObject.+?video_meta-(.+?)"').findall(link)
	return video_ids

def get_video(video_id):
	req = urllib2.Request("http://riptide.mtvnn.com/mediagen/"+video_id)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	
	swfurl = "http://media.mtvnservices.com/player/prime/mediaplayerprime.1.9.0.swf"

	
	match=re.compile('<src>(.+?)</src>').findall(link)
	video=match[-1]+' swfurl='+swfurl+' swfvfy=true' + " pageUrl=www.gameone.de app=ondemand?ovpfv=2.1.4"
	return video



                
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
        INDEX_TV(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS_TV(url)
        
elif mode==3:
        print ""+url
        INDEX_PLAYTUBE(url)

elif mode==4:
        print ""+url
        CAT_PLAYTUBE(url)

elif mode==5:
        print ""+url
        VIDEOLINKS_PLAYTUBE(url,name)
        
elif mode==6:
        print ""+url
        INDEX_BLOG(url)

elif mode==7:
        print ""+url
        CAT_BLOG(url)

elif mode==8:
        print ""+url
        VIDEOLINKS_BLOG(url,name)

elif mode==9:
        print ""+url
        INDEX_PODCAST(url)

elif mode==10:
        print ""+url
        PLAY_PODCAST(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
