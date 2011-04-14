import urllib,urllib2,re,xbmcplugin,xbmcgui

# -*- coding: cp1252 -*-


req = urllib2.Request('http://www.servustv.com/')
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
response = urllib2.urlopen(req)
main_site=response.read()
response.close()
#print main_site


def MAIN():
        match_mediathek=re.compile("<a class='navItem5' href='(.+?)'>Mediathek").findall(main_site)
        #<a class='navItem5' href='/cs/Satellite/VOD-Mediathek/001259088496198?p=1259088496182'>Mediathek
        #match_live=re.compile("href='http://redbullmediahouse.edgeboss.net/flash-live/(.+?)'").findall(main_site)
#        href='http://redbullmediahouse.edgeboss.net/flash-live/redbullmediahouse/59353/500_redbullmediahouse_stv_090817.xml'
        for mediathek_url in match_mediathek:
                #print mediathek_url
                addDir('Mediathek','http://www.servustv.com'+mediathek_url,1,'')
        #for live_xml in match_live:
        #        addDir('Livestream','http://redbullmediahouse.edgeboss.net/flash-live/'+live_xml,7,'')
        #        print live_xml






#http://www.servustv.com/cs/Satellite?articleId=1259339508854&c=ST_Video&cid=1259337827964&pagename=servustv/ST_Video/VideoPlayerDataXML&programType=live


                       
def INDEX(url):#1
#        addDir('Top Video: ',url,2,'')#todo
        addDir('Neuste Videos',url,5,'')
        addDir('Nach Thema',url,2,'')
        addDir('Nach Sparte',url,3,'')
        addDir('Nach Sendung',url,4,'') 


                
def THEMA(url):#2
        #print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile("<li class='category.+?'><a href='(.+?)'>(.+?)</a></li>", re.DOTALL).findall(link)
#        <li class='category1'><a href='/cs/Satellite/VOD-Mediathek/001259088496198?p=1259088496213'>Unterhaltung</a></li>
        for url,name in match:
                #print 'url :'+url
                #print 'name'+name
                addDir(name,'http://www.servustv.com'+url,5,'')




def SPARTE(url):#3
        #print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match_sparten=re.compile('<label for="nachThemen">Sparte</label>.+?\n.+?<select name="nachThemen" id="nachThemen">.+?\n.+?<option value=\'all\' selected="selected">Alle</option>(.+?)</select>', re.DOTALL).findall(link)
        #<label for="nachThemen">Sparte</label>
	#	<select name="nachThemen" id="nachThemen">
	#	        <option value='all' selected="selected">Alle</option>
	#	        <option value='1259088496301'>Abenteuer & Reisen</option>
	#       </select>
        for sparten in match_sparten:
                match_sparte=re.compile("<option value='(.+?)'>(.+?)</option>").findall(sparten)
                #<option value='1259088496301'>Abenteuer & Reisen</option>
                for value,name in match_sparte:
                        addDir(name,'http://www.servustv.com/cs/Satellite?pagename=ServusTV%2FAjax%2FMediathekData&nachThemen='+value+'&nachSendung=all&nachThemenNodeId=null&nachThemen_changed=2&nachSendung_changed=1&ajax=true',5,'')
                        #http://www.servustv.com/cs/Satellite?pagename=ServusTV%2FAjax%2FMediathekData&nachThemen=1259088496301&nachSendung=all&nachThemenNodeId=null&nachThemen_changed=2&nachSendung_changed=1&ajax=true        

def SENDUNG(url):#4
        #print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match_sendungen=re.compile('<label for="nachSendung">Sendung</label>.+?\n.+?<select name="nachSendung" id="nachSendung">.+?\n.+?<option value=\'all\' selected="selected">Alle</option>(.+?)</select>', re.DOTALL).findall(link)
        #<label for="nachSendung">Sendung</label>
	#	<select name="nachSendung" id="nachSendung">
	#		<option value='all' selected="selected">Alle</option>
	#		<option value='1259356338646'>360Five International World Series</option>
	#	</select>
        for sendungen in match_sendungen:
                print sendungen
                match_sendung=re.compile("<option value='(.+?)'>(.+?)</option>").findall(sendungen)
                #<option value='1259088496301'>Abenteuer & Reisen</option>
                for value,name in match_sendung:
                        print value
                        addDir(name,'http://www.servustv.com/cs/Satellite?pagename=ServusTV%2FAjax%2FMediathekData&nachThemen=all&nachSendung='+value+'&nachThemenNodeId=null&nachThemen_changed=1&nachSendung_changed=2&ajax=true',5,'')
                        #http://www.servustv.com/cs/Satellite?pagename=ServusTV%2FAjax%2FMediathekData&nachThemen=all&nachSendung=1259356338646&nachThemenNodeId=null&nachThemen_changed=1&nachSendung_changed=2&ajax=true



                
                
def VIDEOSELECTION(url):#5
        print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #print link
        match1=re.compile('<ul class="programScrollerSmall">(.+?)</ul>', re.DOTALL).findall(link)
        #<a href='/cs/Satellite?iCurrentPage=2&pagename=ServusTV%2FAjax%2FMediathekData' class="nachste">nächste</a>

        #match_next=re.compile('<a href=\'(.+?)\' class="nachste">nächste</a>').findall(link)
        
        for videos in match1:
                match2=re.compile('<li>(.+?)</li>', re.DOTALL).findall(videos)
                for video in match2:
                        print video
                        print '################################'
                        match3=re.compile('<a href=\'/cs/Satellite\?assetId=(.+?)&c=ST_Video&cid=(.+?)&ida=.+?&pagename=servustv%2FST_Video%2FVideoPlayer&programType=vod.+?>.+?<img src=\'(.+?)\'.+?<a href=.+?\n									(.+?)</a>.+?<div class="programDescription">.+?\n										(.+?)</div>', re.DOTALL).findall(video)#, re.DOTALL
                        #.+?<div class="programDescription">.+?\n(.+?)</div>.+?
                        #<a href=\'/cs/Satellite\?assetId=(.+?)&c=ST_Video&cid=(.+?)&ida=.+?&pagename=servustv%2FST_Video%2FVideoPlayer&programType=vod.+?>.+?<img src=\'(.+?)\'.+?height
                        #.+?<a href=".+?">.+?\n(.+?)</a>.+?<div.+?\n(.+?)</div>
                        #/cs/Satellite?assetId=1259356008257&c=ST_Video&cid=1259364585399&ida=1259364585399&pagename=servustv%2FST_Video%2FVideoPlayer&programType=vod
                        for assetid,videoid,thumbnail,name1,name2 in match3:
                                addDir(name1+' - '+name2,'http://www.servustv.com/cs/Satellite?articleId='+assetid+'&c=ST_Video&cid='+videoid+'&pagename=servustv/ST_Video/VideoPlayerDataXML&programType=vod',6,'http://www.servustv.com'+thumbnail)

        #TODO: nächste seite implementieren (ruft nur ne "statische" seite auf, infos werden über den referer übertragen)
        #for nxt in match_next:
        #        addDir('Nächste Seite','http://www.servustv.com'+nxt,5,'')
        #Referer	http://www.servustv.com/cs/Satellite/VOD-Mediathek/001259088496198?p=1259088496182

def VIDEOPLAY(url,name):#6
        #print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        xml=response.read()
        response.close()
        match_video=re.compile('<(.+?)_video_url>(.+?)</.+?_video_url>').findall(xml)
        #<high_video_url>rtmp://cp81614.edgefcs.net/ondemand/mp4:IKA11_Humm_high.mp4</high_video_url>
        #<low_video_url>rtmp://cp81614.edgefcs.net/ondemand/mp4:IKA11_Humm_low.mp4</low_video_url>
        for quality,video in match_video:
                addLink('Play '+quality,video,'')                        

                #answ: http://www.servustv.com/cs/Satellite?assetId=1259356001688&c=ST_Video&cid=1259364551440&ida=1259364551440&pagename=servustv%2FST_Video%2FVideoPlayer&programType=vod&ajax=true
#        for url in match2:
#                addDir('Next Site',url,3,'')

def LIVEPLAY(url,name):#7
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        xml=response.read()
        response.close()
        print xml
        match_video=re.compile('<video src="(.+?)".+?\n.+?\n.+? value="(.+?)".+?>').findall(xml)
        #<video src="rtmp://cp56429.live.edgefcs.net/live/1309@s13392" title="ServusTV" copyright="ServusTV" author="ServusTV">
        #<param name="isLive" value="1" valuetype="data"/>
        #<param name="playAuthParams" value="auth=daEbibtaqd3bPcPdjczdub9aea.bEaeabcG-bnPDPt-eS-JDJnpywxqABAxtzq&aifp=0001" valuetype="data"/>
        for url,auth in match_video:
                addLink('Play low',url+'&'+auth,'')
                print url+'&'+auth


                
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




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
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
#print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        MAIN()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        THEMA(url)

elif mode==3:
        print ""+url
        SPARTE(url)            

elif mode==4:
        print ""+url
        SENDUNG(url)

elif mode==5:
        print ""+url
        VIDEOSELECTION(url)
        
elif mode==6:
        print ""+url
        VIDEOPLAY(url,name)
        
elif mode==7:
        print ""+url
        LIVEPLAY(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
