RTL_URL	  = 'http://www.rtl.be/'
RTL_VIDEO_URL	  = 'http://www.rtl.be'
RTL_PROGRAM_VIDEO_URL = 'http://www.rtl.be/videos/'

ICON = 'rtl_logo.png'
ART = 'art-default.png'

####################################################################################################
def Start():

  Plugin.AddPrefixHandler('/video/rtl_tv_be', MainMenu, 'RTL_TV_BE', ICON, ART)
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
  ObjectContainer.title1 = 'RTL_TV_BE'
  ObjectContainer.content = ContainerContent.GenericVideos
  ObjectContainer.art = R(ART)
  DirectoryObject.thumb = R(ICON)
  VideoClipObject.thumb = R(ICON)
  VideoClipObject.art = R(ART)
  HTTP.CacheTime = 1800

####################################################################################################
def MainMenu():

  oc = ObjectContainer(
    objects = [
      DirectoryObject(
        key     = Callback(GetItemList, url='', title2='Videos'),
        title   = L('Videos')
      )
    ]
  )                                 
  # append programs list directly
  # oc = GetProgramList(url="video/", oc=oc)
  return oc

####################################################################################################

def GetProgramList(url, oc):
  Log ("RTBF GetProgramList :" + url)
  html = HTML.ElementFromURL(RTBF_URL + url)
  programs = html.xpath('.//li[contains(@class, "col-md-2")]')
  for program in programs:
    program_url = program.xpath(".//a")[0].get("href")
    if program_url.startswith (RTBF_PROGRAM_VIDEO_URL) == True:
      program_url = program_url.split(RTBF_PROGRAM_VIDEO_URL)[1]
    Log.Info(program_url)
    title = program.xpath(".//a")[0].text
    Log.Info(title)
    do = DirectoryObject(key = Callback(GetItemList, url=program_url, title2=title), title = title)
    oc.add(do)
  return oc 
	
def GetItemList(url, title2, page=''):
  Log ("RTL GetItemList :" + url)
  Log.Exception('GetItemList')
  cookies = HTTP.CookiesForURL(RTL_URL)
  unsortedVideos = {}
  oc = ObjectContainer(title2=title2, view_group='InfoList', http_cookies=cookies)
  Log.Exception('videos')
  program_url = RTL_PROGRAM_VIDEO_URL + url
  Log ("RTL url : " + program_url)
  html = HTML.ElementFromURL(program_url)
  videos = html.xpath('.//div[contains(@class, "Thumbnail")]')
  Log.Info(videos)
  for video in videos:
    Log.Info("video:")
    try:
      video_page_url=RTL_VIDEO_URL+video.xpath("./a/@href")[0]
      Log ("video url: " + video_page_url)
      title = video.xpath("./h3/text()")[0]
      img = RTL_VIDEO_URL+video.xpath("./a/img/@src")[0]
      oc.add(VideoClipObject(url = video_page_url, title = title, thumb=img))
    except:
      Log.Exception("error adding VideoClipObject")
      pass
        
  return oc
  
