"""查看数据库内容
"""

import os
from pathlib import Path
import sqlite3

DATABASE: Path = Path(os.path.dirname(
    os.path.abspath(__file__))).joinpath("../config.db")
conn = sqlite3.connect(DATABASE)
c = conn.cursor()

result = c.execute("SELECT * FROM CONFIG")
COLUMN = ["id", "r18", "num", "uid", "tag", "size", "proxy", "excludeai", "type"]
for rs in result:
    print("--------------------------------------")
    for i in range(9):
        print(f"{COLUMN[i]}={rs[i]}")
    print("--------------------------------------")
