# -*- coding: iso-8859-1 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui

pluginhandle = int(sys.argv[1])
#gameone

def CATEGORIES():
		INDEX_TV('http://gameone.de/tv')
        #addDir('Ganze Folgen','http://gameone.de/tv',1,'http://assets.gameone.de/images/element_bg/logo-game-one.png')
#        addDir('Blog (nur teilweise mit Videos)','http://gameone.de/blog',5,'http://assets.gameone.de/images/element_bg/logo-game-one.png')
#        addDir('Blog: Games','http://gameone.de/blog/categories/games',5,'http://gameone.de/images/dummys/games.jpg')
#        addDir('Blog: Unplugged','http://gameone.de/blog/categories/unplugged',5,'http://gameone.de/images/dummys/unplugged.jpg')
#        addDir('Blog: Beef','http://gameone.de/blog/categories/beef',5,'http://gameone.de/images/dummys/beef.jpg')
#        addDir('Blog: Kopfkino','http://gameone.de/blog/categories/kopfkino',5,'http://gameone.de/images/dummys/kopfkino.jpg')
#        addDir('Blog: Schame-One','http://gameone.de/blog/categories/shame-one',5,'http://gameone.de/images/dummys/shame-one.jpg')
#        addDir('Blog: alt!1','http://gameone.de/blog/categories/alt-1',5,'http://gameone.de/images/dummys/alt-1.jpg')
#        addDir('Playtube: Gameone-Movies','http://gameone.de/playtube/channel/game-one-movies/6',3,'http://asset.gameone.de/gameone/assets/video_channels/teaser_images/000/000/006/sidebar/g1movies_small.jpg')
#        addDir('Playtube: Beef','http://gameone.de/playtube/channel/beef/26',3,'http://asset.gameone.de/gameone/assets/video_channels/teaser_images/000/000/026/sidebar/keysmall_beef.jpg')        
#        addDir('Playtube: Wir spielen','http://gameone.de/playtube/channel/wir-spielen/38',3,'http://asset.gameone.de/gameone/assets/video_channels/teaser_images/000/000/038/sidebar/keysmall_wirspielen.jpg')
#        addDir('Playtube: Featured','http://gameone.de/playtube/channel/featured/42',3,'http://asset.gameone.de/gameone/assets/video_channels/teaser_images/000/000/042/sidebar/keysmall_featured.jpg')
#        addDir('Playtube: Uservideos','http://gameone.de/playtube/channel/uservideos/18',3,'http://asset.gameone.de/gameone/assets/video_channels/teaser_images/000/000/018/sidebar/keysmall_uservideos.jpg')
#        addDir('Playtube: Gametrailers','http://gameone.de/playtube/channel/gametrailers/50',3,'')


        
################################tv################################


def INDEX_TV(url):#1
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="/tv/(.+?)" class="image_link"><img alt=".+?" src="(.+?)" /></a>\n<h5>\n<a href=\'.+?\' title=\'(.+?)\'>').findall(link)
        #<a href="/tv/162" class="image_link"><img alt="156543_87ac3a65_mp4_640x480_1600" src="http://asset.gameone.de/gameone/assets/video_metas/teaser_images/000/618/246/featured/156543_87ac3a65_mp4_640x480_1600.mp4_cropped.jpg?1300200447" /></a><h5><a href='/tv/162' title='Flirtgewitter, Yakuza 4, Next'>GameOne - Folge 162</a>
        for folge,thumbnail,title in match:
                addLink('Folge: '+folge+' - '+title,'http://gameone.de/tv/'+folge,2,thumbnail)



def VIDEOLINKS_TV(url):#2
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	match_id=re.compile('riptide_video_id: "(.+?)"').findall(link)
	for video_id in match_id:
		req = urllib2.Request("http://riptide.mtvnn.com/mediagen/"+video_id)
        	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        	response = urllib2.urlopen(req)
        	link=response.read()
        	response.close()
		match=re.compile('<src>(.+?)</src>').findall(link)
		video=match[-1]+' swfurl=http://media.mtvnservices.com/player/prime/mediaplayerprime.1.9.0.swf swfvfy=true'
#        <video width="566" height="424" controls="controls" src="http://cdn.riptide-mtvn.com/production/0016/1260/161262_bff037dd_mp4_640x480_1400.mp4" 
#poster="http://asset.gameone.de/gameone/assets/video_metas/teaser_images/000/620/792/big/161262_bff037dd_mp4_640x480_1400.mp4_cropped.jpg?1306681883"></video>
        item = xbmcgui.ListItem(path=video)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
        #<param name="href" value="http://cdn.riptide-mtvn.com/production/0015/6542/156543_87ac3a65_mp4_640x480_1600.mp4" />
#        for url in match:
#                addLink('Play',url+'_mp4_640x480_1600.mp4','')



################################playtube################################

                
def INDEX_PLAYTUBE(url):#3
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
                addLink(name,url,4,thumbnail)
        match_a=re.compile('<a href=(.+?)>').findall(link)
        #<a href="/playtube/channel/game-one-movies/6?page=2" class="next_page" rel="next">Nächste Seite</a></div>
        for href in match_a:
                #print 'hrefplaytube: '+href
                match_next=re.compile('"/playtube/channel/(.+?)" class="next_page" rel="next"').findall(href)
                for naechste_seite in match_next:
                        #print 'next'+naechste_seite
                        addDir('Nächste Seite','http://gameone.de/playtube/channel/'+naechste_seite,3,'')


def VIDEOLINKS_PLAYTUBE(url,name):#4
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
        
        

################################blog################################


def INDEX_BLOG(url):#5
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
        for url,name,thumbnail in match:
                addDir(name,url,6,thumbnail)
        match_a=re.compile('<a href=(.+?)>').findall(link)
        #match_a=re.compile('<a href=(.+?)>').findall(link)
        #<a href="/blog?page=2" class="next_page" rel="next">Nächste Seite</a>
        for href in match_a:
                #print 'hrefblog: '+href
                match_next=re.compile('"/blog(.+?)" class="next_page" rel="next"').findall(href)
                for naechste_seite in match_next:
                        #print 'next'+naechste_seite
                        addDir('Nächste Seite','http://gameone.de/blog'+naechste_seite,5,'')


def VIDEOLINKS_BLOG(url,name):#6
        print 'Url: '+'http://gameone.de'+url
        req = urllib2.Request('http://gameone.de'+url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        print link
        response.close()
        match=re.compile('hqv: "riptide/(.+?)"').findall(link)
        match18=re.compile('<img src="(.+?)dummy_agerated.jpg">').findall(link)
        #<img src="/images/dummys/dummy_agerated.jpg">
        #http://cdn.riptide-mtvn.com/production/0015/7077/157093_eca4df1f_mp4_640x480_1400.mp4
        #var variables = { file: "riptide/production/0015/3789/153790_0ed79c30_flv_448x336_650.flv", streamer: "rtmp://cp8619.edgefcs.net/ondemand/", pageName: "gameone/zurueck-in-die-zukunft-extended", usehq: false, hqv: "riptide/production/0015/3789/153791_0ed79c30_mp4_640x480_1600.mp4", duration: "636.3", adson: true, autostart: false, configFile: "http://assets.gameone.de/flash/g2_player/config.xml?1289856314", image: "http://asset.gameone.de/gameone/assets/video_metas/teaser_images/000/616/299/big/153791_0ed79c30_mp4_640x480_1600.mp4_cropped.jpg?1295845477", available_profiles: [{"id":153792,"filename":"riptide/production/0015/3789/153792_0ed79c30_mp4_256x192_350.mp4","height":192,"width":256}], playername: "153790_video_meta_616299" };
        for url in match:
                addLinkOld('Play','http://cdn.riptide-mtvn.com/'+url,'')
        for restricted in match18:
                addLinkOld('Video nur zwischen 22:00 und 06:00 verfügbar','','http://gameone.de/images/dummys/dummy_agerated.jpg')
                
                
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
        VIDEOLINKS_PLAYTUBE(url,name)
        
elif mode==5:
        print ""+url
        INDEX_BLOG(url)

elif mode==6:
        print ""+url
        VIDEOLINKS_BLOG(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
