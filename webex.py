from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import time

# selenium service start
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

"""check version of chrome
check for camera and mic"""
opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("--disable-extensions")
opt.add_argument("--disable-default-apps")
opt.add_argument("--disable-notifications")
opt.add_argument("--disable-popup-window")
opt.add_argument("--mute-audio")
opt.add_argument("--use-fake-ui-for-media-stream")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 2,
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
})

wait = 15



class Webex:
    def __init__(self, nameofuser, email, link):

        self.email = email
        self.link = link
        self.nameofuser = nameofuser
        self.driver = webdriver.Chrome(options=opt, service=Service(ChromeDriverManager().install()))

    def login(self):

        self.driver.get(self.link)

        time.sleep(3)

        url: str = self.driver.current_url
        if "dashboard" in url:
            btn = self.driver.find_element_by_id("smartJoinButton-action")
            btn.click()
            time.sleep(3)

        url = self.driver.current_url

        # 웹앱으로 전환
        if "download" in url and "?launchApp=true" not in url:
            url = url + "?launchApp=true"

        if "?launchApp=true" not in self.driver.current_url:
            self.driver.execute_script('window.open()')
            nxt_handle = self.driver.window_handles[1]
            self.driver.switch_to.window(nxt_handle)
            self.driver.get(url)
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.close()
            self.driver.switch_to.window(nxt_handle)

        # meeting screen
        WebDriverWait(self.driver, wait).until(EC.frame_to_be_available_and_switch_to_it("thinIframe"))

        # 이름, 이메일 기입 후 엔터
        name = WebDriverWait(self.driver, wait).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '''#meetingSimpleContainer div[class*="name"] input''')))
        name.send_keys(self.nameofuser)

        email = WebDriverWait(self.driver, wait).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '''#meetingSimpleContainer div[class*="email"] input''')))
        email.send_keys(self.email)

        nxtBtn = WebDriverWait(self.driver, wait).until(
            EC.presence_of_element_located((By.ID, "guest_next-btn")))

        nxtBtn.click()

        self.driver.switch_to.default_content()  # switch back

        # meeting screen
        WebDriverWait(self.driver, wait).until(EC.frame_to_be_available_and_switch_to_it("thinIframe"))

        try:
            # mute button click
            mBtn = WebDriverWait(self.driver, wait).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-doi^="AUDIO:MUTE_SELF"]')))
            mBtn.click()
        except:
            print("마이크 음소거 버튼을 누르지 못했습니다.")

        try:
            # video button click
            vBtn = WebDriverWait(self.driver, wait).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-doi^="VIDEO:STOP_VIDEO"]')))
            vBtn.click()
        except:
            print("비디오 끄기 버튼을 누르지 못했습니다.")

        # join button click
        joinBtn = WebDriverWait(self.driver, wait).until(
            EC.presence_of_element_located((By.ID, "interstitial_join_btn")))
        joinBtn.click()

        self.driver.switch_to.default_content()  # switch back
        time.sleep(2)  # TODO: 다른 wait로 변환 필요
        WebDriverWait(self.driver, wait).until(EC.frame_to_be_available_and_switch_to_it("thinIframe"))

    def getUsernameList(self):
        # meeting screen

        uList: list[str] = []
        for el in self.driver.find_elements(By.CSS_SELECTOR, 'div[role="listbox"] div[title]'):
            # uList.append(el.text)
            uList.append(el.get_attribute('title').strip())
        # p_section = self.driver.find_element_by_css_selector('section[class^="plist-scrollbar"]')
        # html = p_section.get_attribute('innerHTML')
        # soup = BeautifulSoup(html, 'html.parser')
        # hList = soup.select('div[class^="styles-user-name"]')
        # for el in hList:
        #     uList.append(el.text.strip())
        return uList

    def activateUserListView(self) -> bool:
        self.driver.switch_to.default_content()  # switch back
        WebDriverWait(self.driver, wait).until(EC.frame_to_be_available_and_switch_to_it("thinIframe"))

        try:
            WebDriverWait(self.driver, wait).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class^="style-loading-lobby-box"]')))
        except:
            print("아직 미팅이 시작되지 않았습니다.")
            return False

        pBtn = WebDriverWait(self.driver, wait).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-doi^="PARTICIPANT"]')))
        pBtn.click()

        return True

        # 스크롤을 Bottom-Up 하면서 유저 리스트 갱신
        # percent = .1
        # while percent < 9.9:
        #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % percent)
        #     percent += .01
        # elements = self.driver.find_elements_by_css_selector('div[class^="styles-user-name"]')
        # self.driver.execute_script('arguments[0].scrollIntoView({block: "center"})', elements[-1])
        # self.driver.execute_script('arguments[0].scrollIntoView({behavior: "smooth", block: "center"})', elements[0])

    def run(self):
        self.login()
        while True:
            uList = self.getUsernameList()
            if not uList:
                self.activateUserListView()
            time.sleep(3)
            print(uList)


if __name__ == "__main__":
    sess = Webex("AAA_출석봇",
                 "AAA@abc.com",
                 "<웹엑스 접속 링크>")
    sess.run()
