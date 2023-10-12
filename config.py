import os

from pathlib import Path
from typing import List, Any
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    pic_dir: Path = Path(os.path.dirname(os.path.abspath(__file__))).joinpath("./pics")
    r18: int = 0
    num: int = 1
    uid: Any = 0
    tag: List[Any] = [["BlueArchive", "碧蓝档案", "蔚蓝档案", "ブルーアーカイブ", "ブルアカ"]]
    size: List[str] = ["original"]
    proxy: str = "i.pixiv.re"
    excludeAI: bool = False
