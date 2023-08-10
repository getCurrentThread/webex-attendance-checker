import datetime
import json
import os.path
import sys
import threading
import time
from typing import Dict

from PySide6.QtWidgets import QApplication

from form import XYTableDialog, MyTable
from webex import Webex
import baselogger

logger = baselogger.getLogger(__name__)

class Worker(threading.Thread):
    def __init__(self, table: MyTable, info: Dict[str, str]):
        super().__init__()
        self.table = table
        with open("members.csv") as fp:
            text = fp.read()
            data = text.replace("\r\n", "\n").split("\n")
            data2D = []
            for i in data:
                data2D.append(i.split(","))
            for idx, arr in enumerate(data2D):
                if len(arr) < 3:
                    for i in range(3 - len(arr)):
                        data2D[idx].append('')
            self.table.setData(data2D)
        self.sess = Webex(info["nickname"], info["email"], info["url"])

    def run(self):
        logger.info("webex 로그인을 시도합니다")
        self.sess.login()
        while True:
            data = self.table.data2()
            uList = self.sess.getUsernameList()
            if not uList:
                try:
                    if self.sess.activateUserListView() == False:
                        continue
                except:
                    logger.info("webex 유저 리스트뷰를 불러오는데 실패했습니다.")
                    continue
            logger.info(f"총인원 : {len(uList)}, {uList}")
            for idx, val in enumerate(data):
                if val[1] or val[0] == '':  # 이름이 비어있거나, 접속한 시간이 이미 있는 컬럼이면 제외
                    continue
                name = val[0]
                for username in uList:
                    if name in username:
                        data[idx][1] = datetime.datetime.now().strftime('%H:%M:%S')
                        logger.info(f"{name} 님이 들어왔습니다")
                        break

            self.table.setData(data)
            time.sleep(3)


if __name__ == "__main__":
    data = [['이열에_이름을_넣어주세요', '', ''],
            ['', '', ''],
            ['', '', '']]
    app = QApplication(sys.argv)
    dlg = XYTableDialog(["이름", "접속시간", "출석여부"], data)
    dlg.show()

    login_info = {}
    with open('secrets.json', encoding='utf-8') as fp:
        login_info = json.loads(fp.read())

    # TODO: 조금 더 설계적인 코드 리펙토링 필요 (동기화 등)
    t = Worker(dlg.table, login_info)
    t.daemon = True
    t.start()

    app.exec_()
