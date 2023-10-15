import re
from typing import Annotated, Any
from nonebot import logger, on_regex
from nonebot.params import RegexDict
from nonebot.plugin import PluginMetadata
from nonebot.adapters.red import Bot, MessageEvent, MessageSegment

from .config import HELP, MAX_PICS, Config
from .utils import saveImage, check_database, update_database, update_optional_status

__plugin_meta = PluginMetadata(
    name="BaImages",
    description="Get BA Images",
    usage=HELP,
    config=Config,
)

# 获取配置
# global_config = get_driver().config
# config = Config.parse_obj(global_config)

get_a_image = on_regex(r'\/setu\s*(?P<tag>\S*)?\s*[x|*]?(?P<num>\d+)?[张|个|份]?'
                       , re.I, priority=2)
status = on_regex(r"\/setu\s+(?P<cmd>open|close|开启|关闭)\s+(?P<tag>r18|ai)", 
                  priority=1, block=True)
help = on_regex(r"\/setu\s*(help|帮助)", priority=1, block=True)

if check_database():
    logger.info("数据库已创建！")
else:
    logger.info("数据库创建成功！")

@get_a_image.handle()
async def _(bot: Bot, event: MessageEvent, 
            regex_group: Annotated[dict[str, Any], RegexDict()]):
    config = Config()
    args = dict(regex_group)
    logger.debug(args)
    config.id = int(event.scene)
    if tag := args["tag"]:
        if tag.isdigit():
            config.num = int(tag)
        else:
            config.tag = tag
    if num := args["num"]:
        num = int(num)
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

@status.handle()
async def _(bot: Bot, event: MessageEvent, 
            regex_group: Annotated[dict[str, Any], RegexDict()]):
    args = dict(regex_group)
    logger.debug(f"status={args}")
    id = int(event.scene)
    logger.debug(event.scene)
    logger.debug(id)
    logger.debug(type(id))
    # 此处应该按照群组与好友进行鉴权处理，但是adapter-red没写获取发送者id的方法……
    if args["cmd"] == "open" or args["cmd"] == "开启":
        await update_optional_status(1, args["tag"], id)
        await bot.send(event, MessageSegment.text(f"{args['tag']}已开启！"))
    else:
        await update_optional_status(0, args["tag"], id)
        await bot.send(event, MessageSegment.text(f"{args['tag']}已关闭！"))

@help.handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(event, MessageSegment.text(HELP))

