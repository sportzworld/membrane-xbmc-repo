import urllib,urllib2,re,xbmcplugin,xbmcgui,time

#membrane's tv.hokej.cz addon
#todo:
# -clean up
# -add live section
# -change icon (placeholder)
# -seperate language file
# -translate
# -randomize video and thumbnail mirror

#date = time.strftime("%d.%m.%Y",time.gmtime())
day = time.strftime("%d",time.gmtime())
month = time.strftime("%m",time.gmtime())
year = time.strftime("%Y",time.gmtime())

req = urllib2.Request('http://tv.hokej.cz/xml/archivTest.xml')
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
response = urllib2.urlopen(req)
link=response.read()
response.close()


def CATEGORIES():
#        addDir('Live','',1,'') #todo        
        addDir( 'Archive','text',1,'')

		
def INDEX(url):
        match=re.compile('<round value="(.+?)" active=.+?<date date="(.+?)\.(.+?)\.(.+?)">').findall(link)
        for roundvalue,mday,mmonth,myear in match:
                if roundvalue == 'R':#todo: clean up
                        #todo
                        print 'folder R ignored'
                elif myear < year:
                        if re.match("^[0-9]*$", roundvalue):
                                addDir('Round '+roundvalue,roundvalue,2,'')
                        else:
                                addDir(roundvalue,roundvalue,2,'')
                                #print 'a'+url
                elif mmonth < month and myear == year:
                        if re.match("^[0-9]*$", roundvalue):
                                addDir('Round '+roundvalue,roundvalue,2,'')
                        else:
                                addDir(roundvalue,roundvalue,2,'')
                                #print 'b'+url
                elif mday <= day and mmonth == month and myear == year:
                        if re.match("^[0-9]*$", roundvalue):
                                addDir('Round '+roundvalue,roundvalue,2,'')
                        else:
                                addDir(roundvalue,roundvalue,2,'')
                                #print 'c'+url


def ROUNDSECTION(roundvalue):
        match_rv=re.compile('<round value="'+roundvalue+'" active=.+?>(.+?)</round>').findall(link)
        for date in match_rv:
                print date
                match_date=re.compile('<date date="(.+?)\.(.+?)\.(.+?)">(.+?)</date>').findall(date)
                for mday,mmonth,myear,games in match_date:
                        print games
                        if myear < year:
                                VIDEOLINK(games,roundvalue,mday,mmonth,myear)
                        elif mmonth < month and myear == year:
                                VIDEOLINK(games,roundvalue,mday,mmonth,myear)
                        elif mday <= day and mmonth == month and myear == year:
                                VIDEOLINK(games,roundvalue,mday,mmonth,myear)

def VIDEOLINK(games,roundvalue,mday,mmonth,myear):                                
        match=re.compile('<game cislozapasu="(.+?)".+?home="(.+?)" guest="(.+?)" status="(.+?)" HomeScore="(.+?)" GuestScore="(.+?)"').findall(games)
        for video_id,home,guest,status,homescore,guestscore in match:
                print video_id
                if status == '1':
                        if re.match("^[0-9]*$", roundvalue):
                                addLink(mday+'.'+mmonth+'.'+myear+' - '+home+' vs '+guest+' - '+homescore+' : '+guestscore,'http://extraliga.archiv.livebox.cz/ELHARCHIV2/'+roundvalue+'/'+home+'_H.wmv?h=','http://tv.hokej.cz/thumbnail/'+home+'-1.jpg')
                        elif 'R' == roundvalue:#not in use
                                addLink(mday+'.'+mmonth+'.'+myear+' - '+home+' vs '+guest+' - '+homescore+' : '+guestscore,'http://extraliga.archiv.livebox.cz/ELHARCHIV2/R/'+video_id+'_H.wmv?h=','')
                        else:
                                addLink(mday+'.'+mmonth+'.'+myear+' - '+home+' vs '+guest+' - '+homescore+' : '+guestscore,'http://extraliga.archiv.livebox.cz/ELHARCHIV2/0/'+video_id+'_H.wmv?h=','http://tv.hokej.cz/thumbnail/'+home+'-1.jpg')


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
        ROUNDSECTION(url)        
        


xbmcplugin.endOfDirectory(int(sys.argv[1]))
		
