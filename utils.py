import os
import json
import aiohttp
import aiofiles
import sqlite3

from pathlib import Path
from typing import Any, List

from nonebot import logger
from .config import Config, PIC_DIR, DATABASE, TAG



async def createImageDir() -> Path:
    """若无本地图片文件夹则创建本地图片文件夹"""
    image_dir = PIC_DIR
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
    return image_dir

async def getImage(id: int) -> List[Any]:
    """获取图片对应JSON数据"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    info = c.execute("SELECT * FROM CONFIG WHERE ID = ?", (id, )).fetchone()
    url="https://api.lolicon.app/setu/v2"
    if info[4]:
        tag = [TAG, info[4]]
    else:
        tag = [TAG]
    data = {
        "tag": tag,
        "r18": info[1],
        "num": info[2],
        #"uid": info[3],
        "size": "original",
        "proxy": info[6],
        "excludeAI": info[7]
    }
    logger.debug(data["tag"])
    conn.close()
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as sess:
        async with sess.post(url=url, data=json.dumps(data), headers=headers) as resp:
            resp_dict = json.loads(json.dumps(await resp.json()))
            print(resp_dict)
            return_data = []
            for r_data in resp_dict["data"]:
                return_data.append([
                    r_data["title"], 
                    r_data["urls"][data["size"]], 
                    r_data["ext"]
                ])
            return return_data

async def saveImage(id: int) -> List[Path]:
    """功能：保存图片至本地"""
    pic_paths = []
    pic_datas = await getImage(id)
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

def check_database() -> bool:
    """检查数据库是否存在，若不存在则创建数据库"""
    if (not os.path.exists(DATABASE)):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''CREATE TABLE CONFIG(
            ID INTEGER PRIMARY KEY NOT NULL,
            R18 INTEGER,
            NUM INTEGER,
            UID TEXT,
            TAG TEXT,
            SIZE TEXT,
            PROXY TEXT,
            EXCLUDEAI INTEGER,
            TYPE TEXT
        );''')
        conn.close()
        return True
    return False

async def update_database(config: Config) -> None:
    """更新数据库"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    sql = "SELECT * FROM CONFIG WHERE ID = ?"
    data = c.execute(sql, (config.id, )).fetchone()
    if not data:
        logger.debug("start to update database!")
        sql = """INSERT INTO CONFIG (ID, R18, NUM, UID, TAG, 
                                    PROXY, EXCLUDEAI, TYPE)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        c.execute(sql, (config.id, config.r18, config.num, config.uid, config.tag,
                        config.proxy, int(config.excludeAI), config.message_type))
        logger.debug("finish update database!")
        conn.commit()
    else:
        logger.debug("start to update database")
        sql = "UPDATE CONFIG SET TAG = ?, NUM = ?, R18 = ?, TYPE = ? WHERE ID = ?"
        c.execute(sql, (config.tag, config.num, config.r18, 
                        config.message_type, config.id))
        logger.debug("finish update database")
        conn.commit()
    conn.close()

async def update_optional_status(cmd: int, tag: str, id: int):
    """更新可选状态"""
    config = Config()
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    sql = "SELECT * FROM CONFIG WHERE ID = ?"
    data = c.execute(sql, (id, )).fetchone()
    # 如果对应id的行在数据库中未创建，则需通过初始数据创建
    if not data:
        logger.debug("start to update database!")
        sql = """INSERT INTO CONFIG (ID, R18, NUM, UID, TAG, 
                                    PROXY, EXCLUDEAI, TYPE)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        c.execute(sql, (id, config.r18, config.num, config.uid, config.tag,
                        config.proxy, int(config.excludeAI), config.message_type))
        logger.debug("finish update database!")
        conn.commit()
    if tag == "r18":
        sql = "UPDATE CONFIG SET R18 = ? WHERE ID = ?"
        logger.debug("start to update r18 status")
        c.execute(sql, (cmd, id))
        conn.commit()
        logger.debug("finish to update r18 status")
    else:
        sql = "UPDATE CONFIG SET EXCLUDEAI = ? WHERE ID = ?"
        logger.debug("start to update ai status")
        c.execute(sql, (cmd, id))
        conn.commit()
        logger.debug("finish to update ai status")
    conn.close()

