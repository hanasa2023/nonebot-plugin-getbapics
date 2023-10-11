import os

from pathlib import Path
from typing import List
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    pic_dir: Path = Path(os.path.dirname(os.path.abspath(__file__))).joinpath("./pics")
    r18: bool = False
    num: int = 1
    uid: int = 1
    tag: List[str] = ["BlueArchive", "碧蓝档案", "蔚蓝档案", "ブルーアーカイブ", "ブルアカ"]
    size: str = "original"
    proxy: str = "1-cf.pximg.net"
    excludeAI: bool = False
