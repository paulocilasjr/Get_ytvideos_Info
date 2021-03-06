import scrapy
import re
import json


class GetvideosSpiderSpider(scrapy.Spider):
    name = 'getvideos-spider'
    allowed_domains = ['youtube.com']
    start_urls = ['https://www.youtube.com/results?search_query=ish+tecnologia&sp=EgQIBRAB']
    
    def parse(self, response):
        
        pattern = re.compile('[^.]* ytInitialData [^<]*')
        allDataJson = response.css('script::text').re_first(pattern).replace("var ytInitialData = ", "")[:-1]
        allDataDict = json.loads(allDataJson)
        
        ListWithVideosInfo = allDataDict["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
        
        videoNumber = 1
        videosArray = []
        videosDict = {"Videos": videosArray}
        
        for index in range(len(ListWithVideosInfo)):
            videoInfo = {
                "ID": videoNumber,
                "Title": ListWithVideosInfo[index]["videoRenderer"]["title"]["runs"][0]["text"],
                "URL" : "www.youtube.com" + ListWithVideosInfo[index]["videoRenderer"]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
            }
            videoNumber += 1
            videosArray.append(videoInfo)
        
        videosInfoJson = json.dumps(videosDict, indent=4, ensure_ascii=False)
        print(videosInfoJson)

        #<<<<IF YOU WANT SAVE A FILE AT THE END>>>
        page = response.url.split("/")[-2]
        filename = "ytvideos_Info_Result.json"
        with open(filename, 'w', encoding='utf8') as f:
            f.write(videosInfoJson)
        self.log(f'Saved file {filename}')
        
