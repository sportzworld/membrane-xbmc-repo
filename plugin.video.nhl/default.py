import urllib,urllib2,re,random,xbmcplugin,xbmcgui






def YEAR():
        addDir('2011','&year=2011',1,'')#hardcoded because i'm lazy. also, no site request required.
        addDir('2010','&year=2010',1,'')
        addDir('2009','&year=2009',1,'')
        addDir('2008','&year=2008',1,'')
        addDir('2007','&year=2007',1,'')
        addDir('2006','&year=2006',1,'')
        addDir('2005','&year=2005',1,'')

               
def MONTH(url):
        addDir('Jan','&month=1'+url,2,'')
        addDir('Feb','&month=2'+url,2,'')
        addDir('Mar','&month=3'+url,2,'')
        addDir('Apr','&month=4'+url,2,'')
        addDir('May','&month=5'+url,2,'')
        addDir('Jun','&month=6'+url,2,'')
        addDir('Jul','&month=7'+url,2,'')
        addDir('Aug','&month=8'+url,2,'')
        addDir('Seb','&month=9'+url,2,'')
        addDir('Oct','&month=10'+url,2,'')
        addDir('Nov','&month=11'+url,2,'')
        addDir('Dec','&month=12'+url,2,'')

def RESULTS(url):        
        req = urllib2.Request('http://video.nhl.com/videocenter/highlights?xml=0'+url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        print link
        match=re.compile('<game>.+?<game-date>(.+?)</game-date>.+?<name>(.+?)</name>.+?<city>(.+?)</city>.+?<goals>(.+?)</goals>.+?<name>(.+?)</name>.+?<city>(.+?)</city>.+?<goals>(.+?)</goals>.+?<alt-video-clip>(.+?)</alt-video-clip>.+?<video-clip-thumbnail>(.+?)</video-clip-thumbnail>.+?</game>', re.DOTALL).findall(link)
        for date,guestname,guestcity,guestgoals,homename,homecity,homegoals,url,thumb in match:
                addLink(date+' '+homecity+' '+homename+' vs. '+guestcity+' '+guestname+' - '+homegoals+':'+guestgoals,url,thumb)

                
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
        YEAR()
       
elif mode==1:
        print ""+url
        MONTH(url)
        
elif mode==2:
        print ""+url
        RESULTS(url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
