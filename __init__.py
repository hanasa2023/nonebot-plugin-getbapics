from nonebot import get_driver, on_command, logger
from nonebot.plugin import PluginMetadata
from nonebot.adapters.red import Bot, MessageEvent, MessageSegment

from .config import Config
from .utils import saveImage

__plugin_meta = PluginMetadata(
    name="BaImages",
    description="Get BA Images",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

get_a_image = on_command("setu")

@get_a_image.handle()
async def _(bot: Bot, event: MessageEvent):
    files = await saveImage()
    for file in files:
        try:
            await bot.send(event, MessageSegment.image(file=file))
        except Exception as e:
            await bot.send(event, MessageSegment(e))