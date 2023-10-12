import os
import json
import aiohttp
import asyncio
import aiofiles

from pathlib import Path
from typing import Any, List


async def createImageDir() -> Path:
    """功能：若无本地图片文件夹则创建本地图片文件夹"""
    image_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    image_dir = image_dir.joinpath("./pics")
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
    return image_dir

async def getImage() -> List[Any]:
    """功能：获取图片对应JSON数据"""
    url="https://api.lolicon.app/setu/v2"
    data = {
        "tag": [
            ["BlueArchive", "碧蓝档案", "蔚蓝档案", "ブルーアーカイブ", "ブルアカ"]
        ],
        "r18": 0,
        "num": 3,
        "uid": 0,
        "size": "original",
        "excludeAI": False
    }
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as sess:
        async with sess.post(url=url, data=json.dumps(data), headers=headers) as resp:
            resp_dict = json.loads(json.dumps(await resp.json()))
            print(resp_dict)
            return_data = []
            for r_data in resp_dict["data"]:
                return_data.append([r_data["title"], r_data["urls"][data["size"]], r_data["urls"][data["size"]][-3:]])
            return return_data

async def saveImage() -> List[Path]:
    """功能：保存图片至本地"""
    pic_paths = []
    pic_datas = await getImage()
    for pic_data in pic_datas:
        title, url, type = pic_data
        pic_dir = await createImageDir()
        pic_path = pic_dir.joinpath(f"{title}.{type}")
        pic_paths.append(pic_path)
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as resp:
                response = await resp.read()
        async with aiofiles.open(pic_path, 'wb') as f:
            await f.write(response)
    return pic_paths

if __name__ == "__main__":
    asyncio.run(saveImage())