from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException
import pickle
from webdriver_manager.chrome import ChromeDriverManager
from aiogram import types, executor, Dispatcher, Bot


class InstagramBot():

    def __init__(self, username, password):

        self.username = username
        self.password = password
        # включаем опции драйвера
        self.options = webdriver.ChromeOptions()
        # запуск в фотоном режиме
        self.options.add_argument("--headless")
        # self.options.headless = True
        # изменяем user aget
        self.options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        # отключаем драйвер и передаем options в webdriver.Crome
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)

        # старый метод
        # self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=self.options)

        # новый метод
        # s = Service(executable_path=ChromeDriverManager().install())
        # self.driver = webdriver.Chrome(service=s, options=self.options)


    # метод для закрытия браузера
    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    # метод логина
    def login(self):
        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(7, 10))


        # вводим логин и пароль
        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

        # for cookie in pickle.load(open(f"{username}_cookies", "rb")):
        #     browser.add_cookie(cookie)
        # time.sleep(5)
        # browser.refresh()
        # time.sleep(5)
        #
        # #cookies
        # pickle.dump(browser.get_cookies(), open(f"{username}_cookies", "wb"))


    # проверяем по xpath существует ли элемент на странице
    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # ставим лайк на пост по прямой ссылке
    def put_exactly_like(self, userpost):
        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого поста не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пост успешно найден, ставим лайк!")
            time.sleep(2)

            like_button = "#react-root > section > main > div > div.ltEKP > article > div > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm > div > div > section.ltpMr.Slqrh > span.fr66n > button"
            browser.find_element_by_css_selector(like_button).click()
            time.sleep(2)
            print(f"Лайк на пост: {userpost} поставлен!")

    # #смотрим отключен ли режим веб драйвера
    # def exit_driver(self):
    #     try:
    #         self.browser.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
    #         time.sleep(10)
    #
    #     except Exception as ex:
    #         print(ex)
    #     finally:
    #         self.browser.close()
    #         self.browser.quit()

    # пищим пять комметариев на пост по прямой ссылке
    def put_exactly_comments(self):
            comment_button = "#react-root > section > main > div > div.ltEKP > article > div > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm > div > div.eo2As > section.ltpMr.Slqrh > span._15y0l > button > div.QBdPU.rrUvL > svg"
            self.browser.find_element_by_css_selector(comment_button).click()
            time.sleep(4)

            comment = self.browser.find_element_by_css_selector('textarea.Ypffh')
            comment.send_keys("Ваш первый коммент" + Keys.ENTER)
            time.sleep(5)
            comment.send_keys("Ваш второй коммент" + Keys.ENTER)
            time.sleep(5)
            comment.send_keys("Ваш третий коммент" + Keys.ENTER)
            time.sleep(5)
            comment.send_keys("Ваш четвертый коммент" + Keys.ENTER)
            time.sleep(5)
            comment.send_keys("Ваш пятый коммент" + Keys.ENTER)
            time.sleep(5)
            print("Пять комментариев на пост: написаны!")
            self.close_browser()


TOKEN = "token"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def begin(message: types.Message):
    await bot.send_message(message.chat.id, "Пришли ссылку")

@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    sylka = message.text
    print(sylka)
    my_bot = InstagramBot(username, password)
    my_bot.login()
    my_bot.put_exactly_like(sylka)
    await bot.send_message(message.chat.id, f"Лайк на пост: {sylka} поставлен!")
    my_bot.put_exactly_comments()
    await bot.send_message(message.chat.id, "И написано 5 комментариев под этим постом")


executor.start_polling(dp)