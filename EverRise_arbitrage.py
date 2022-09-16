import time
import telegram
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

bot = telegram.Bot(token="5182557952:AAGL9FrlVYAHcB02WP5_mVW4OtFkW2Nv0I4")
browserBSC = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browserETH = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browserPOLY = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browserFTM = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browserAVAX = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def botSend(ms):
    bot.send_message(chat_id="-1001588132946", text=ms, parse_mode=telegram.ParseMode.HTML)


def getPrice(browser):
    if browser == browserBSC:
        # find sellPrice
        sellPrice = WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_all_elements_located((
                By.CLASS_NAME, 'crWxyC')))
        print('1')
        sellPrice = 1.0 / float(sellPrice[1].text.replace(' ', '').replace('RISE', '').replace('per', '').replace('USDC', ''))
        # find buyPrice
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="swap-page"]/div[1]/div[2]/div/button'))).click()
        print('2')
        buyPrice = WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_all_elements_located((
                By.CLASS_NAME, 'crWxyC')))
        print('3')
        p = 0
        for e in buyPrice:
            if e.text.find('RISE') != -1:
                p = buyPrice.index(e)
        buyPrice = float(buyPrice[p].text.replace(' ', '').replace('RISE', '').replace('per', '').replace('USDC', ''))
        # reset
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="swap-page"]/div[1]/div[2]/div/button'))).click()
        print('4')

    elif browser == browserETH:
        # find sellPrice
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'kJukNQ'))).click()
        print('5')
        sellPrice = WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'kJukNQ'))).text
        print('6')
        sellPrice = sellPrice.replace('1 RISE = ', '').replace(' USDC', '').split('\n')
        sellPrice = float(sellPrice[0])
        # find buyPrice
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'kbQZhd'))).click()
        print('7')
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'kJukNQ'))).click()
        print('8')
        buyPrice = WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'kJukNQ'))).text
        print('9')
        buyPrice = buyPrice.replace('1 RISE = ', '').replace(' USDC', '').split('\n')
        buyPrice = float(buyPrice[0])
        # reset
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'kbQZhd'))).click()
        print('10')

    elif browser == browserPOLY:
        # find sellPrice
        sellPrice = WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((
                By.XPATH, '//*[@id="swap-page"]/div[1]/div[4]/div/div/div[2]'))).text
        sellPrice = 1.0 / float(sellPrice.replace(' ', '').replace('RISE', '').replace('per', '').replace('USDC', ''))
        print('11')
        # find buyPrice
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'duoFXQ'))).click()
        print('12')
        buyPrice = WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((
                By.XPATH, '//*[@id="swap-page"]/div[1]/div[4]/div/div/div[2]'))).text
        buyPrice = float(buyPrice.replace(' ', '').replace('RISE', '').replace('per', '').replace('USDC', ''))
        print('13')
        # reset
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'duoFXQ'))).click()
        print('14')

    elif browser == browserFTM:
        # find sellPrice
        while True:
            sellPrice = WebDriverWait(browser, 20).until(
                expected_conditions.visibility_of_element_located((
                    By.CLASS_NAME, 'gBEqLy'))).text
            if sellPrice.find('best') == -1:
                break
            time.sleep(1)
        sellPrice = 1.0 / float(sellPrice.replace('1 USDC = ', '').replace(' RISE', '').replace(',', ''))
        # find buyPrice
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'dnqnwn'))).click()
        print('15')
        while True:
            buyPrice = WebDriverWait(browser, 20).until(
                expected_conditions.visibility_of_element_located((
                    By.CLASS_NAME, 'gBEqLy'))).text
            if buyPrice.find('best') == -1:
                break
            time.sleep(1)
        buyPrice = float(buyPrice.replace('1 RISE = ', '').replace(' USDC', '').replace(',', ''))
        print('16')
        # reset
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'dnqnwn'))).click()
        print('17')

    elif browser == browserAVAX:
        # find sellPrice
        sellPrice = WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_all_elements_located((
                By.CLASS_NAME, 'css-1ljiscj')))
        sellPrice = 1.0 / float(sellPrice[1].text.replace(' ', '').replace('RISE', '').replace('per', '').replace('USDC', ''))
        print('18')
        # find buyPrice
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'geXnWT'))).click()
        print('19')
        buyPrice = WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_all_elements_located((
                By.CLASS_NAME, 'css-1ljiscj')))
        buyPrice = float(buyPrice[1].text.replace(' ', '').replace('RISE', '').replace('per', '').replace('USDC', ''))
        print('20')
        # reset
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'geXnWT'))).click()
        print('21')
    else:
        print('no such chain')
        buyPrice, sellPrice = 0, 0
    return sellPrice, buyPrice


def setupSite(browser):
    inputRISE = '5000000'
    browser.maximize_window()
    if browser == browserBSC:
        browser.get('https://pancakeswap.finance/swap')
        # input RISE
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="swap-currency-input"]/div[1]/button'))).click()
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'eSruuq'))).send_keys(
                '0cD022ddE27169b20895e0e2B2B8A33B25e63579')
        try:
            WebDriverWait(browser, 8).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'jDURXQ'))).click()
            WebDriverWait(browser, 20).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'bykDxt'))).click()
            WebDriverWait(browser, 20).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'iSokCE'))).click()
        except:
            WebDriverWait(browser, 20).until(
                expected_conditions.visibility_of_element_located((
                    By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]'))).click()
        # input USDC
        WebDriverWait(browser, 20).until(
            expected_conditions.presence_of_element_located((
                By.XPATH, '//*[@id="swap-currency-output"]/div[1]/button'))).click()
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'eSruuq'))).send_keys(
                '0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d')
        try:
            WebDriverWait(browser, 8).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, 'jDURXQ'))).click()
            WebDriverWait(browser, 20).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, 'bykDxt'))).click()
            WebDriverWait(browser, 20).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, 'iSokCE'))).click()
        except:
            WebDriverWait(browser, 20).until(
                expected_conditions.visibility_of_element_located((
                    By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]'))).click()

        # input amount
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'SItsC'))).click()
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'SItsC'))).send_keys(
            inputRISE)

    elif browser == browserETH:
        browser.get('https://app.uniswap.org/#/swap?chain=mainnet')
        # input RISE
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'cxfJOR'))).click()
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'dhJtzB'))).send_keys(
            '0cD022ddE27169b20895e0e2B2B8A33B25e63579')
        try:
            WebDriverWait(browser, 8).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'BDrHY'))).click()
            WebDriverWait(browser, 20).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'dXylXG'))).click()
        except:
            WebDriverWait(browser, 20).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '/html/body/reach-portal[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div/div'))).click()
        # input USDC

        WebDriverWait(browser, 20).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="swap-currency-output"]/div/div/button/span/div/span'))).click()
        browser.minimize_window()
        time.sleep(1)
        browser.maximize_window()
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.XPATH, '/html/body/reach-portal[2]/div[3]/div/div/div/div/div[1]/div[3]/div/div[3]/div'))).click()
        # input amount
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'kpLMn'))).click()
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'kpLMn'))).send_keys(
            inputRISE)

    elif browser == browserPOLY:
        browser.get('https://quickswap.exchange/#/swap')
        # input RISE
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'bDdbTq'))).click()
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'hseXrP'))).send_keys(
            '0cD022ddE27169b20895e0e2B2B8A33B25e63579')
        time.sleep(.5)
        # if rise doesn't show, refresh
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'ionkDx'))).click()
        # input USDC
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'bbjeGH'))).click()
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'hseXrP'))).send_keys(
            '2791bca1f2de4661ed88a30c99a7a9449aa84174')
        time.sleep(.5)
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'ionkDx'))).click()
        # input amount
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'kJTFAb'))).click()
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'kJTFAb'))).send_keys(
            inputRISE)

    elif browser == browserFTM:
        browser.get('https://matcha.xyz/markets/250/0x04068da6c83afcfa0e13ba15a6696662335d5b75/0x0cd022dde27169b20895e0e2b2b8a33b25e63579')
        # import tokens
        try:
            WebDriverWait(browser, 8).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'hMlefr'))).click()
            time.sleep(1)
            WebDriverWait(browser, 20).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'hMlefr'))).click()
        except:
                print('ftm fix')
        # input amount
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'oBMLO'))).click()
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'oBMLO'))).send_keys(
            inputRISE)

    elif browser == browserAVAX:
        browser.get('https://traderjoexyz.com/trade')
        # input RISE
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'bYuzLP'))).click()
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'kwoaaQ'))).send_keys(
            '0xC3A8d300333BFfE3ddF6166F2Bc84E6d38351BED')
        time.sleep(.5)
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'css-8mokm4'))).click()
        # input USDC
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((
                By.XPATH, '//*[@id="swap-currency-output"]/div[2]/div/div/span/span'))).click()
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'kwoaaQ'))).send_keys(
            '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E')
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'kewpBx'))).click()
        # input amount
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'cykxFH'))).click()
        WebDriverWait(browser, 20).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'cykxFH'))).send_keys(
            inputRISE)
        browser.minimize_window()


def calcArb():
    tax = 6  # as percent
    thresh = 1  # as percent
    c = 0
    gain = []
    results = []
    names = ['BSC', 'ETH', 'POLY', 'FTM', 'AVAX']
    prices = [getPrice(browserBSC), getPrice(browserETH), getPrice(browserPOLY), getPrice(browserFTM), getPrice(browserAVAX)]
    for i in range(len(prices)):
        for j in range(len(prices)):
            if prices[i][0] > prices[j][0]:
                gain.append((prices[i][0] * (1 - tax / 100) ** 2 - prices[j][1]) / prices[j][1])
                if gain[c] > thresh/100:
                    results.append('SELL ' + names[i] + ' BUY ' + names[j] + ' ' + str(round(gain[c]*100, 3)) + '% gain')
                    c += 1
                else:
                    gain.remove(gain[c])
    for e in results:
        botSend(e)


def setup():
    try:
        setupSite(browserBSC)
        setupSite(browserETH)
        setupSite(browserPOLY)
        setupSite(browserFTM)
        setupSite(browserAVAX)
    except:
        print('setup error')
        time.sleep(2)
        setup()


setup()
while True:
    tickRate = 20
    try:
        calcArb()
    except:
        print('pricing error')
        setup()
    time.sleep(tickRate)
