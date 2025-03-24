import os.path

import jmcomic

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register


@register("JMComicDownloader", "Sh1roCu", "JM下载", "1.0.0","https://github.com/Sh1roCu/JMComicDownloader ")
class JMComicDownloader(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("jm")
    async def execute_download(self, event: AstrMessageEvent, id: int):
        option: jmcomic.JmOption = jmcomic.create_option_by_file("option.yml")
        result: tuple = jmcomic.download_album(id, option)
        downloader: jmcomic.JmDownloader = result[1]
        while True:
            if downloader.all_success and os.path.exists("images/{}.jpg".format(id)):
                break
        yield event.image_result("images/{}.jpg".format(id))
