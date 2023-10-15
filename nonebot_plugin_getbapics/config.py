import os

from pathlib import Path
from typing import Any, List
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    id: int = -1
    r18: int = 0
    num: int = 1
    tag: str = ""
    uid: Any = None
    size: str = "original"
    proxy: str = "i.pixiv.re"
    excludeAI: bool = False
    message_type: str = "group"

PIC_DIR: Path = Path(os.path.dirname(os.path.abspath(__file__))).joinpath("./pics")
DATABASE: Path = Path(os.path.dirname(
    os.path.abspath(__file__))).joinpath("./config.db")
TAG: List[str] = ["BlueArchive | 碧蓝档案 | 蔚蓝档案 | ブルーアーカイブ | ブルアカ"]
MAX_PICS = 5
HELP = """
使用方法: 
    输入 /setu+[tag]+[x|X|*][num]+量词
    tag自选， x X *可选，num可选，量词可选 张 个 份
    输入 /setu open/close/开启/关闭 r18/ai 开启/关闭 获取r18/ai图功能
    输入 /setu help|帮助 获取帮助
例: /setu
    /setu 4
    /setu 美游 x4张
    /setu x4张
    /setu 美游 x4个
    /setu 美游 4张
    /setu 美游 4"""
