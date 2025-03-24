import os.path
import sys

import jmcomic

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register


@register("astrbot_plugin_jmcomic_downloader", "Sh1roCu", "JM下载", "v1.0.0",
          "https://github.com/Sh1roCu/astrbot_plugin_jmcomic_downloader")
class JMComicDownloader(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("jm")
    async def execute_download(self, event: AstrMessageEvent, id: int):
        option: jmcomic.JmOption = jmcomic.create_option_by_file(sys.path[0] + "/option.yml")
        result: tuple = jmcomic.download_album(id, option)
        downloader: jmcomic.JmDownloader = result[1]
        while True:
            if downloader.all_success and os.path.exists("images/{}.jpg".format(id)):
                break
        yield event.image_result("images/{}.jpg".format(id))
