import re
from typing import Annotated, Any
from nonebot import get_driver, logger, on_command, on_regex
from nonebot.params import RegexDict
from nonebot.plugin import PluginMetadata
from nonebot.adapters.red import Bot, MessageEvent, MessageSegment

from .config import MAX_PICS, Config
from .utils import saveImage, _check_database, update_database

__plugin_meta = PluginMetadata(
    name="BaImages",
    description="Get BA Images",
    usage="""使用方法: 输入 /setu+[tag]+[x|X|*][num]+量词 使用
                        tag自选， x X *可选，num可选，量词可选 张 个 份
                        已实现空格自由
            例子:   /setu
                    /setu 4
                    /setu 美游 x4张
                    /setu x4张
                    /setu 美游 x4个
                    /setu 美游 4张
                    /setu 美游 4""",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

get_a_image = on_regex(r'^\/setu\s*(?P<tag>\S*)?\s*[x|*]?(?P<num>\d+)?[张|个|份]?$'
                       , re.I)
r18_status = on_command("")

if _check_database():
    logger.info("数据库已创建！")
else:
    logger.info("数据库创建成功！")

@get_a_image.handle()
async def _(bot: Bot, event: MessageEvent, 
            regex_group: Annotated[dict[str, Any], RegexDict()]):
    args = dict(regex_group)
    logger.debug(args)
    config.id = int(event.scene)
    if tag := args["tag"]:
        config.tag = tag
    if num := int(args["num"]):
        if num > MAX_PICS:
            await bot.send(event, MessageSegment.text(
                f"当前单次获取数量已超过最大限制{MAX_PICS}张，已使用默认数量～ "
            ))
        else:
            config.num = num
    if not event.is_group:
        config.message_type = "private"
    await bot.send(event, "请耐心等待喵～")
    await update_database(config)
    files = await saveImage(config.id)
    for file in files:
       try:
           await bot.send(event, MessageSegment.image(file=file))
       except Exception as e:
           await bot.send(event, MessageSegment(str(e)))
