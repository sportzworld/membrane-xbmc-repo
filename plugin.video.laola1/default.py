# -*- coding: latin-1 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui


def CATEGORIES():
#        addDir('Upcoming Livestreams Deutschland','http://www.laola1.tv/de/de/home/',5,'')
#        addDir('Upcoming Livestreams Österreich','http://www.laola1.tv/de/at/home/',5,'')
#        addDir('Upcoming Livestreams International','http://www.laola1.tv/en/int/home/',5,'')
        addDir('Archiv Deutschland','http://www.laola1.tv/de/de/home/',1,'')
        addDir('Archiv Österreich','http://www.laola1.tv/de/at/home/',1,'')
        addDir('Archiv International','http://www.laola1.tv/en/int/home/',1,'')
                       
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<div id="sitemap"><a (.+?)</div>').findall(link)
        for something in match:
                match1=re.compile('href="(.+?)".*?>(.+?)</a>').findall(something)
                for url,name in match1 or match2:
                        addDir(name,url,2,'')


                
def TOPICSELECTION(url):
        #print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match1=re.compile("<td style=\".+?\" width=\".+?\"><h2><a href=\"(.+?)\" style=\".+?\">(.+?)</a></h2></td>").findall(link) 
        for url,name in match1:
                #print 'url :'+url
                #print 'name'+name
                addDir(name,url,3,'')
                ##<td style="padding-left:15px;" width="316"><h2><a href="http://www.laola1.tv/de/de/erste-bank-eishockey-liga-live/video/222-1154-.html" style="color:#ffffff; font-weight:bold; font-size:12pt;">Erste Bank Eishockey Liga LIVE</a></h2></td>
                
                
def VIDEOSELECTION(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match1=re.compile('<div class=".+?" title=".+?"><a href="(.+?)"><img src="(.+?)" border=".+?" /></a></div>.+?<div class="teaser_head_video" title=".+?">(.+?)</div>.+?<div class="teaser_text" title=".+?">(.+?)</div>', re.DOTALL).findall(link)
        #<div class="teaser_bild_video" title="Eishockey, Erste Bank Eishockey Liga, EC KAC - EC Red Bull Salzburg - Bild: LAOLA1"><a href="http://www.laola1.tv/de/de/eishockey/erste-bank-ehl/ec-kac-ec-red-bull-salzburg/video/222-1153-48060.html"><img src="http://www.laola1.tv/cache/img/thumb/48060.jpg" border="0"></a></div>
        #<div class="teaser_head_video" title="Eishockey, Erste Bank Eishockey Liga, EC KAC - EC Red Bull Salzburg - Bild: LAOLA1">Di, 05.04.2011</div>
        #<div class="teaser_text" title="Eishockey, Erste Bank Eishockey Liga, EC KAC - EC Red Bull Salzburg">EC KAC - EC Red Bull Salzburg</div>

        match2=re.compile("<a href=\"(.+)\" class=\"teaser_text\">vor</a>").findall(link)
        ##<a href="http://www.laola1.tv/de/de/eishockey/erste-bank-ehl/ehc-liwest-bw-linz-ec-red-bull-salzburg/video/222-1153--2.html" class="teaser_text">vor</a>
        for url,thumbnail,date,name in match1:
                addDir(date+' - '+name,url,4,thumbnail)
        for url in match2:
                addDir('Next Site',url,3,'')

        ##<div class="miniteaser_bild_live "><a href="http://www.laola1.tv/de/de/eishockey/erste-bank-ehl/ec-kac-rekord-fenster-vsv-/video/222-1153-45986.html"><img src="http://www.laola1.tv/cache/img/thumb/45986.jpg" border="0" width="80" /></a></div>
	##				</td><td style="padding-left:5px;" valign="top">
        ##            <div class="miniteaser_datum">15.03.2011 19:00 CET</div>
	##				<div class="miniteaser_text">EC KAC - REKORD-Fenster VSV </div>

def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match_playkey=re.compile('"playkey=(.+?)-(.+?)&adv.+?"').findall(link)
        ##"playkey=47060-Gut1cOWmlyix.&adv=laola1.tv/de/eishockey/ebel&adi=laola1.tv/de/eishockey/ebel&aps=Video1&szo=eishockey&deutschchannel=true&channel=222&teaser=1153&play=47060&fversion=player.v10.2"
        for playkey1,playkey2 in match_playkey:
                #print 'playkey1 '+playkey1
                #print 'playkey2 '+playkey2                
                req = urllib2.Request('http://www.laola1.tv/server/ondemand_xml_esi.php?playkey='+playkey1+'-'+playkey2)
                #print 'http://www.laola1.tv/server/ondemand_xml_esi.php?playkey='+playkey1+'-'+playkey2
                ##http://www.laola1.tv/server/ondemand_xml_esi.php?playkey=47060-Gut1cOWmlyix.
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link_playkey=response.read()
                #print link_playkey
                response.close()
                match_video=re.compile('<video.+?>(.+?)</video>', re.DOTALL).findall(link_playkey)
                for video in match_video:
                        #print 'video '+video
                        match_rtmp=re.compile('<(.+?) .+?erver="(.+?)/(.+?)" pfad="(.+?)" .+? ptitle="(.+?)"').findall(video)#ugly, but behind low is one space too much: '  '
                        ##<high server="cp77154.edgefcs.net/ondemand" pfad="77154/flash/2011/ebel/20102011/110327_vic_rbs_high" type="V" aifp="v002"
                        ##token="true" ptitle="Eishockey Erste Bank EHL Erste Bank Eishockey Liga" etitle="Vienna Capitals - EC Red Bull Salzburg"
                        ##firstair="2010/01/01" stype="VOD" cat="video ondemand" vidcat="laola1.tv/at/eishockey/ebel" round="" season="2010/2011" />
                        for streamquality,server,servertype,playpath,title in match_rtmp:
                                #print 'streamquality '+streamquality
                                #print 'server '+server
                                #print 'servertype '+servertype
                                #print 'playpath '+playpath
                                #print 'title '+title
                                req = urllib2.Request('http://streamaccess.laola1.tv/flash/vod/22/'+playkey1+'_'+streamquality+'.xml')
                                #print 'http://streamaccess.laola1.tv/flash/vod/22/'+playkey1+'_'+streamquality+'.xml'
                                ##http://streamaccess.laola1.tv/flash/vod/22/47060_high.xml
                                ##http://streamaccess.laola1.tv/flash/1/47215_high.xml
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                response = urllib2.urlopen(req)
                                link_token=response.read()
                                #print link_token
                                response.close()
                                match_token=re.compile('auth="(.+?)".+?url="(.+?)".+?stream="(.+?)".+?status=".+?".+?statustext=".+?".+?aifp="(.+?)"', re.DOTALL).findall(link_token)
                                ##auth="db.cibycHcwdEbhaKa4a3bUc7cIbpbLdtal-bnKofS-cOW-eS-CkBwmc-m6ke&p=&e=&u=&t=ondemandvideo&l=&a="
                                ##url="cp77154.edgefcs.net/ondemand" stream="77154/flash/2011/ebel/20102011/110327_vic_rbs_high" status="0" statustext="success" aifp="v001" comment="success"
                                for auth,url,stream,aifp in match_token:
                                        #print 'auth '+auth
                                        #print 'url '+url
                                        #print 'stream '+stream
                                        #print 'afip '+aifp
                                        req = urllib2.Request('http://'+server+'/fcs/ident')
                                        ##http://cp77154.edgefcs.net/fcs/ident
                                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                        response = urllib2.urlopen(req)
                                        link_path=response.read()
                                        response.close()
                                        match_path=re.compile('<ip>(.+?)</ip>').findall(link_path)
                                        ##<ip>213.198.95.204</ip>
                                        for ip in match_path:
                                                #print 'ip '+ip
                                        ##http://cp77154.edgefcs.net/fcs/ident
                                                if streamquality == 'high':
                                                        addLink('High: '+name,'rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+server+'&auth='+auth+'&aifp='+aifp+'&slist='+stream,'')
                                                        ##rtmp://213.198.95.204:1935/ondemand?_fcs_vhost=cp77154.edgefcs.net&auth=db.cibycHcwdEbhaKa4a3bUc7cIbpbLdtal-bnKofS-cOW-eS-CkBwmc-m6ke&p=&e=&u=&t=ondemandvideo&l=&a=
                                                        ##&aifp=v001&slist=77154/flash/2011/ebel/20102011/110327_vic_rbs_high
                                                        ##rtmp://213.198.95.204:1935/ondemand?_fcs_vhost=cp77154.edgefcs.net&auth=db.cibycHcwdEbhaKa4a3bUc7cIbpbLdtal-bnKofS-cOW-eS-CkBwmc-m6ke&p=&e=&u=&t=ondemandvideo&l=&a=&aifp=v001&slist=77154/flash/2011/ebel/20102011/110327_vic_rbs_high
                                                elif streamquality == 'low':
                                                        addLink('Low: '+name,'rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+server+'&auth='+auth+'&aifp='+aifp+'&slist='+stream,'')


                                                        ##...yeah
        




def LIVESELECTION(url):
        #print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match1=re.compile('<h2><a href="http://www.laola1.tv/(.+?)/upcoming-livestreams/(.+?)"').findall(link)
        #<h2><a href="http://www.laola1.tv/en/int/upcoming-livestreams/video/0-989-.html"
        for lang,videos in match1:
                #print videos
                req = urllib2.Request('http://www.laola1.tv/'+lang+'/upcoming-livestreams/'+videos)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                #print link
                response.close()
                match1=re.compile('<div class=".+?" title=".+?"><a href="(.+?)"><img src="(.+?)" border=".+?" /></a></div>.+?<div class="teaser_head_live" title=".+?">(.+?)</div>.+?<div class="teaser_text" title=".+?">(.+?)</div>', re.DOTALL).findall(link)
                #<div class="teaser_bild_live" title="LIVE: Eishockey, Erste Bank Eishockey Liga, EC RedBull Salzburg vs EC KAC - Bild: Gepa"><a href="http://www.laola1.tv/de/de/eishockey/erste-bank-ehl/ec-redbull-salzburg-vs-ec-kac/video/222-1369-47327.html"><img src="http://www.laola1.tv/cache/img/thumb/47327.jpg" border="0" /></a></div>
                #<div class="teaser_head_live" title="LIVE: Eishockey, Erste Bank Eishockey Liga, EC RedBull Salzburg vs EC KAC - Bild: Gepa">Do, 07.04.2011, 19:15 CET</div>
                #<div class="teaser_text" title="LIVE: Eishockey, Erste Bank Eishockey Liga, EC RedBull Salzburg vs EC KAC">EC RedBull Salzburg vs EC KAC</div>
                match2=re.compile("<a href=\"(.+)\" class=\"teaser_text\">vor</a>").findall(link)
                ##<a href="http://www.laola1.tv/de/de/eishockey/erste-bank-ehl/ehc-liwest-bw-linz-ec-red-bull-salzburg/video/222-1153--2.html" class="teaser_text">vor</a>
                for url,thumbnail,date,name in match1:
                        addDir(date+' - '+name,url,6,thumbnail)
                for url in match2:
                        addDir('Next Site',url,5,'')


def VIDEOLIVELINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match_playkey=re.compile('"playkey=(.+?)-(.+?)&adv.+?"').findall(link)
        ##"playkey=47060-Gut1cOWmlyix.&adv=laola1.tv/de/eishockey/ebel&adi=laola1.tv/de/eishockey/ebel&aps=Video1&szo=eishockey&deutschchannel=true&channel=222&teaser=1153&play=47060&fversion=player.v10.2"
        for playkey1,playkey2 in match_playkey:
                #print 'playkey1 '+playkey1
                #print 'playkey2 '+playkey2                
                req = urllib2.Request('http://www.laola1.tv/server/ondemand_xml_esi.php?playkey='+playkey1+'-'+playkey2)
                #print 'http://www.laola1.tv/server/ondemand_xml_esi.php?playkey='+playkey1+'-'+playkey2
                ##http://www.laola1.tv/server/ondemand_xml_esi.php?playkey=47060-Gut1cOWmlyix.
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link_playkey=response.read()
                #print link_playkey
                response.close()
                match_video=re.compile('<video.+?>(.+?)</video>', re.DOTALL).findall(link_playkey)
                for video in match_video:
                        print 'video '+video
                        match_rtmp=re.compile('<high server="(.+?)/(.+?)" pfad="(.+?)@(.+?)" .+? ptitle="(.+?)"').findall(video)#ugly, but behind low is one space too much: '  '
                        ##<high server="cp77154.edgefcs.net/ondemand" pfad="77154/flash/2011/ebel/20102011/110327_vic_rbs_high" type="V" aifp="v002"
                        ##token="true" ptitle="Eishockey Erste Bank EHL Erste Bank Eishockey Liga" etitle="Vienna Capitals - EC Red Bull Salzburg"
                        ##firstair="2010/01/01" stype="VOD" cat="video ondemand" vidcat="laola1.tv/at/eishockey/ebel" round="" season="2010/2011" />
                        for server,servertype,playpath1,playpath2,title in match_rtmp:
                        #for streamquality,server,servertype,playpath1,playpath2,title in match_rtmp:
                                #print 'streamquality '+streamquality
                                print 'server '+server
                                print 'servertype '+servertype
                                print 'playpath '+playpath1+'@'+playpath2
                                print 'title '+title
                                req = urllib2.Request('http://streamaccess.laola1.tv/flash/1/'+playkey1+'_high.xml')
                                #req = urllib2.Request('http://streamaccess.laola1.tv/flash/1/'+playkey1+'_'+streamquality+'.xml')
                                
                                #print 'http://streamaccess.laola1.tv/flash/1/'+playkey1+'_'+streamquality+'.xml'
                                ##http://streamaccess.laola1.tv/flash/1/47327_high.xml?partnerid=1&streamid=47327
                                ##http://streamaccess.laola1.tv/flash/vod/22/47060_high.xml
                                ##http://streamaccess.laola1.tv/flash/1/47215_high.xml
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                response = urllib2.urlopen(req)
                                link_token=response.read()
                                print link_token
                                response.close()
                                match_token=re.compile('auth="(.+?)&amp;p=.+?".+?url="(.+?)/live".+?stream="(.+?)".+?status=".+?".+?statustext=".+?".+?aifp="(.+?)"', re.DOTALL).findall(link_token)
                                ##auth="db.cibycHcwdEbhaKa4a3bUc7cIbpbLdtal-bnKofS-cOW-eS-CkBwmc-m6ke&p=&e=&u=&t=ondemandvideo&l=&a="
                                ##url="cp77154.edgefcs.net/ondemand" stream="77154/flash/2011/ebel/20102011/110327_vic_rbs_high" status="0" statustext="success" aifp="v001" comment="success"
                                for auth,url,stream,aifp in match_token:
                                        print 'auth '+auth
                                        print 'url '+url
                                        print 'stream '+stream
                                        print 'afip '+aifp
                                        req = urllib2.Request('http://'+server+'/fcs/ident')
                                        ##http://cp77154.edgefcs.net/fcs/ident
                                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                        response = urllib2.urlopen(req)
                                        link_path=response.read()
                                        response.close()
                                        match_path=re.compile('<ip>(.+?)</ip>').findall(link_path)
                                        ##<ip>213.198.95.204</ip>
                                        for ip in match_path:
                                                print 'ip '+ip
                                        ##http://cp77154.edgefcs.net/fcs/ident
#                                                if streamquality == 'high':
                                                print 'laola_debug - name: '+name
                                                print 'laola_debug - rtmp-link: rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+url+'/'+stream+'?auth='+auth+'&aifp='+aifp
                                                addLink('High: '+name,'rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+url+'/'+stream+'?auth='+auth+'&p=1&e='+playkey1+'&u=&t=livevideo&l='+'&a='+'&aifp='+aifp,'')
                                                #addLink('High: '+name,'rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+server+'/'+playpath+'?auth='+auth+'&aifp='+aifp,'')



                                                        ##rtmp://213.198.95.204:1935/ondemand?_fcs_vhost=cp77154.edgefcs.net&auth=db.cibycHcwdEbhaKa4a3bUc7cIbpbLdtal-bnKofS-cOW-eS-CkBwmc-m6ke&p=&e=&u=&t=ondemandvideo&l=&a=
                                                        ##&aifp=v001&slist=77154/flash/2011/ebel/20102011/110327_vic_rbs_high
                                                        ##rtmp://213.198.95.204:1935/ondemand?_fcs_vhost=cp77154.edgefcs.net&auth=db.cibycHcwdEbhaKa4a3bUc7cIbpbLdtal-bnKofS-cOW-eS-CkBwmc-m6ke&p=&e=&u=&t=ondemandvideo&l=&a=&aifp=v001&slist=77154/flash/2011/ebel/20102011/110327_vic_rbs_high
                                                #elif streamquality == 'low':
                                                        #addLink('Low: '+name,'rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+server+'/'+playpath+'?auth='+auth+'&aifp='+aifp,'')


                                                        ##...yeah





                
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
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        TOPICSELECTION(url)

elif mode==3:
        print ""+url
        VIDEOSELECTION(url)            
        
elif mode==4:
        print ""+url
        VIDEOLINKS(url,name)
        
elif mode==5:
        print ""+url
        LIVESELECTION(url)

elif mode==6:
        print ""+url
        VIDEOLIVELINKS(url,name)        


xbmcplugin.endOfDirectory(int(sys.argv[1]))
