import os
import json
import aiohttp
import asyncio
import aiofiles

from pathlib import Path
from typing import Tuple


async def createImageDir() -> Path:
    """功能：若无本地图片文件夹则创建本地图片文件夹"""
    image_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    image_dir = image_dir.joinpath("./pics")
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
    return image_dir

async def getImage() -> Tuple[str, str, str]:
    """功能：获取图片对应JSON数据"""
    data = {
        "tag": [
            ["BlueArchive", "碧蓝档案", "蔚蓝档案", "ブルーアーカイブ", "ブルアカ"]
        ],
        "proxy": "1-cf.pximg.net"
    }
    data = json.dumps(data)
    async with aiohttp.ClientSession() as sess:
        async with sess.post("https://api.lolicon.app/setu/v2", data=data) as resp:
            resp_dict = json.loads(json.dumps(await resp.json()))
            print(resp_dict["data"][0])
            return resp_dict["data"][0]["title"], resp_dict["data"][0]["urls"]["original"], resp_dict["data"][0]["urls"]["original"][-3:]

async def saveImage() -> Path:
    """功能：保存图片至本地"""
    title, url, type = await getImage()
    pic_dir = await createImageDir()
    pic_path = pic_dir.joinpath(f"{title}.{type}")
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url) as resp:
            response = await resp.read()
    async with aiofiles.open(pic_path, 'wb') as f:
        await f.write(response)
    return pic_path

if __name__ == "__main__":
    asyncio.run(saveImage())