import os.path
import time

import jmcomic

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register


@register("astrbot_plugin_jmcomic_downloader", "Sh1roCu", "JM下载", "v1.0.0",
          "https://github.com/Sh1roCu/astrbot_plugin_jmcomic_downloader")
class JMComicDownloader(Star):
    base_path: str = os.path.split(os.path.realpath(__file__))[0]

    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("jm")
    async def execute_download(self, event: AstrMessageEvent, comic_id: int):
        option: jmcomic.JmOption = jmcomic.create_option_by_file(JMComicDownloader.base_path + "/option.yml")
        yield event.plain_result("开始下载...")
        result: tuple = jmcomic.download_album(comic_id, option)
        downloader: jmcomic.JmDownloader = result[1]
        while True:
            time.sleep(1)
            if downloader.all_success and os.path.exists(JMComicDownloader.base_path + "/pdf/{}.pdf".format(id)):
                break
        if event.get_platform_name() == "aiocqhttp":
            from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
            assert isinstance(event, AiocqhttpMessageEvent)
            client = event.bot
            payloads = {
                "group_id": event.get_group_id(),
                "message": [
                    {
                        "type": "file",
                        "data": {
                            "file": JMComicDownloader.base_path + "/pdf/{}.pdf".format(id)
                        }
                    }
                ]
            }
            await client.api.call_action('send_group_msg', **payloads)
