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
