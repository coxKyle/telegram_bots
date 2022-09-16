# import cloudscraper
import time, telegram
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pycoingecko import CoinGeckoAPI

# scraper = cloudscraper.create_scraper()
cg = CoinGeckoAPI()
bot = telegram.Bot(token="5074734502:AAGz1C-ZmbNDjZ00CTmi0nICyyLbzpC7WOM")
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
urlBsc = 'https://bscscan.com/readContract?m=normal&a=0x0cD022ddE27169b20895e0e2B2B8A33B25e63579&v=0x0cD022ddE27169b20895e0e2B2B8A33B25e63579#readCollapse36'
urlEth = 'https://etherscan.io/readContract?m=normal&a=0x0cD022ddE27169b20895e0e2B2B8A33B25e63579&v=0x0cD022ddE27169b20895e0e2B2B8A33B25e63579#readCollapse36'
urlPoly = 'https://polygonscan.com/readContract?m=normal&a=0x0cD022ddE27169b20895e0e2B2B8A33B25e63579&v=0x0cD022ddE27169b20895e0e2B2B8A33B25e63579#readCollapse36'
urlFtm = 'https://ftmscan.com/readContract?m=normal&a=0x0cd022dde27169b20895e0e2b2b8a33b25e63579&v=0x0cd022dde27169b20895e0e2b2b8a33b25e63579&t=false#readCollapse36'
urlAvax = 'https://snowtrace.io/readContract?m=normal&a=0xc3a8d300333bffe3ddf6166f2bc84e6d38351bed&v=0xc3a8d300333bffe3ddf6166f2bc84e6d38351bed&t=false#readCollapse36'
currentVol = [0, 0, 0, 0, 0]
volAtBuyBack = []  # +0
volPrev = []  # +5
rewardsPrev = []  # +10
buyVolumePrev = []  # +15
sellVolumePrev = []  # +20
bbAmount = []  # +25
audioWowBoomBoom = "CQACAgEAAx0CasYPEgACEaZh7y9XeeDADtYCT-KAdA75Z9GBIwACQQIAAtO6eEej7QWRNoSbjCME"
tt = 0


def toSave(bbVol, pVol, pRew, volBuy, volSell, bbbAmount):
    val = bbVol + pVol + pRew + volBuy + volSell + bbbAmount
    np.savetxt('kraken.txt', val)

# toSave([0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0])

def toRead(i):
    data = open("C:/Users/kawoo/PycharmProjects/statsEverRise/kraken.txt").read()
    data = list(map(str, data.split("\n")))
    data.remove('')
    data = np.asarray(data, dtype=float)
    return data[i]


def boomBotSend(ms):
    bot.send_message(chat_id="-1001791364882", text=ms, parse_mode=telegram.ParseMode.HTML)

def boomBotSendAudio(ms):
    bot.send_audio(chat_id="-1001791364882", audio=ms)

def rewBotSend(ms):
    bot.send_message(chat_id="-1001729037212", text=ms, parse_mode=telegram.ParseMode.HTML)

def arbBotSend(ms):
    bot.send_message(chat_id="-1001500576052", text=ms, parse_mode=telegram.ParseMode.HTML)


def findVolume(url):
    vol = []
    browser.get(url)
    browser.refresh()
    data = WebDriverWait(browser, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//body'))).text
    if data.find('[Reset]') != -1 or data.find('[Expand all]') != -1:
        if url == urlEth:  # click expand and visible vs presence
            WebDriverWait(browser, 20).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'expandCollapseAllButton'))).click()
            data = WebDriverWait(browser, 20).until(
                expected_conditions.visibility_of_all_elements_located((By.XPATH, '//*[@target="_blank"]')))
            vol.append(round(float(data[9].text) / 10 ** 18, 0))  # totalVolume
            vol.append(round(float(data[6].text) / 10 ** 18, 0))  # totalBuyVolume
            vol.append(round(float(data[7].text) / 10 ** 18, 0))  # totalSellVolume
        elif url == urlFtm:
            data = WebDriverWait(browser, 20).until(
                expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, 'form-group')))
            vol.append(round(float(str(data[42].text.replace(' uint256', ''))) / 10 ** 18, 0))  # totalVolume
            vol.append(round(float(str(data[39].text.replace(' uint256', ''))) / 10 ** 18, 0))  # totalBuyVolume
            vol.append(round(float(str(data[40].text.replace(' uint256', ''))) / 10 ** 18, 0))  # totalSellVolume
        elif url == urlAvax:
            data = WebDriverWait(browser, 20).until(
                expected_conditions.presence_of_all_elements_located((By.XPATH, '//*[@target="_blank"]')))
            vol.append(round(float(data[8].text) / 10 ** 18, 0))  # totalVolume
            vol.append(round(float(data[5].text) / 10 ** 18, 0))  # totalBuyVolume
            vol.append(round(float(data[6].text) / 10 ** 18, 0))  # totalSellVolume
        else:
            data = WebDriverWait(browser, 20).until(
                expected_conditions.presence_of_all_elements_located((By.XPATH, '//*[@target="_blank"]')))
            vol.append(round(float(data[9].text) / 10 ** 18, 0))  # totalVolume
            vol.append(round(float(data[6].text) / 10 ** 18, 0))  # totalBuyVolume
            vol.append(round(float(data[7].text) / 10 ** 18, 0))  # totalSellVolume
        return vol
    else:
        print('ERROR: host is offline')
        time.sleep(10)
        return findVolume(url)


def findBuyBack():
    rew = []
    stakeTotal = []
    stakeMult = []
    browser.get('https://app.everrise.com/everstake/list')
    browser.refresh()
    data = WebDriverWait(browser, 20).until(
        expected_conditions.presence_of_element_located((By.ID, "root"))).text
    if data.find('EVERSTAKE') != -1:
        data = WebDriverWait(browser, 20).until(
            expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "css-xgfg2k")))
        stakeTotal.append(float(str(data[0].text.replace(',', '')).split(' ')[0]))  # bscStakeTotal
        stakeTotal.append(float(str(data[0 + 3].text.replace(',', '')).split(' ')[0]))  # ethStakeTotal
        stakeTotal.append(float(str(data[0 + 3 * 2].text.replace(',', '')).split(' ')[0]))  # polyStakeTotal
        stakeTotal.append(float(str(data[0 + 3 * 3].text.replace(',', '')).split(' ')[0]))  # ftmStakeTotal
        stakeTotal.append(float(str(data[0 + 3 * 4].text.replace(',', '')).split(' ')[0]))  # avaxStakeTotal
        stakeMult.append(float(data[1].text.replace(' months', '')))  # bscStakeMultiplier
        stakeMult.append(float(data[1 + 3].text.replace(' months', '')))  # ethStakeMultiplier
        stakeMult.append(float(data[1 + 3 * 2].text.replace(' months', '')))  # polyStakeMultiplier
        stakeMult.append(float(data[1 + 3 * 3].text.replace(' months', '')))  # ftmStakeMultiplier
        stakeMult.append(float(data[1 + 3 * 4].text.replace(' months', '')))  # avaxStakeMultiplier
        rew.append(float(data[2].text.replace(',', '')))  # bscRewards
        rew.append(float(data[2 + 3].text.replace(',', '')))  # ethRewards
        rew.append(float(data[2 + 3 * 2].text.replace(',', '')))  # polyRewards
        rew.append(float(data[2 + 3 * 3].text.replace(',', '')))  # ftmRewards
        rew.append(float(data[2 + 3 * 4].text.replace(',', '')))  # avaxRewards
        return [rew, stakeTotal, stakeMult]
    else:
        print('ERROR: everstake browser')
        boomBotSend(data)
        time.sleep(10)
        return findBuyBack()


def findRewardsMultiplier(dRew, i):
    arr = findBuyBack()
    x = dRew / arr[1][i] / arr[2][i] * 12 * 100  # 12x as a percent
    return x


def findArb():
    indexes = []
    prices = []
    names = []
    data = cg.get_coin_ticker_by_id(id='everrise', vs_currency='usd')
    data = str(data).split(',')
    for e in data:
        if e.find("'usd': ") != -1:
            indexes.append(data.index(e))
        if e.find("name") != -1 and data.index(e) > 1:
            names.append(e.replace(" 'market': {'name': ", '').replace("'", '').replace(' (v2)', ''))
    for e in indexes:
        if e % 2 != 0:
            indexes.remove(e)
    for e in indexes:
        prices.append(float(data[e].replace(" 'usd': ", '').replace('}', '')))
    for i in range(len(prices) - 1):
        for j in range(len(prices) - 1):
            calcArb(names[i], names[j], prices[i], prices[j])


def calcArb(n1, n2, p1, p2):
    tax = 6  # as percent
    gain = (p1*(1-tax/100)**2-p2)/p2
    s = ''
    if gain > .15:  # as decimal
        s += '\ud83d\udd35 '
    elif gain > .1:  # as decimal
        s += '\ud83d\udfe2 '
    elif gain > .05:  # as decimal
        s += '\ud83d\udfe1 '
    if gain > 0.02:  # as decimal
        s += 'SELL ' + n1 + ' BUY ' + n2 + '\n' + str(round(gain*100, 1)) + '% gain'
        time.sleep(0.3)
    if s != '':
        arbBotSend(s)


def findKrakenBalance(i):
    if i == 0:
        url = 'https://bscscan.com/address/0x0cD022ddE27169b20895e0e2B2B8A33B25e63579'
    elif i == 1:
        url = 'https://etherscan.io/address/0x0cd022dde27169b20895e0e2b2b8a33b25e63579'
    elif i == 2:
        url = 'https://polygonscan.com/address/0x0cD022ddE27169b20895e0e2B2B8A33B25e63579'
    elif i == 3:
        url = 'https://ftmscan.com/address/0x0cD022ddE27169b20895e0e2B2B8A33B25e63579'
    elif i == 4:
        url = 'https://snowtrace.io/address/0xC3A8d300333BFfE3ddF6166F2Bc84E6d38351BED'
    else:
        url = ''

    browser.get(url)
    browser.refresh()
    data = WebDriverWait(browser, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//body'))).text
    if data.find('Donate') != -1:
        data = WebDriverWait(browser, 20).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "col-md-8")))
        bal = data[1].text.replace('$', '').replace(',', '').split(' ')
        return float(bal[0])
    else:
        print('balance error')
        return findKrakenBalance(i)


def check():
    rewards = findBuyBack()[0]
    totalVolume = [findVolume(urlBsc), findVolume(urlEth), findVolume(urlPoly), findVolume(urlFtm), findVolume(urlAvax)]
    boomBotStr = ''
    rewBotStr = ''
    for i in range(5):
        if i == 0:
            iStr = 'BSC'
            bbThreshold = 100 * 10 ** 6
        elif i == 1:
            iStr = 'ETH'
            bbThreshold = 100 * 10 ** 6
        elif i == 2:
            iStr = 'POLY'
            bbThreshold = 100 * 10 ** 6
        elif i == 3:
            iStr = 'FTM'
            bbThreshold = 10 * 10 ** 6
        elif i == 4:
            iStr = 'AVAX'
            bbThreshold = 10 * 10 ** 6
        else:
            iStr = 'GLITCH'
            bbThreshold = 100 * 10 ** 6

        volAtBuyBack.append(toRead(i))
        volPrev.append(toRead(i + 5))
        rewardsPrev.append(toRead(i + 5 * 2))
        buyVolumePrev.append(toRead(i + 5 * 3))
        sellVolumePrev.append(toRead(i + 5 * 4))
        bbAmount.append(toRead(i + 5 * 5))
        buyVolume = totalVolume[i][1]
        sellVolume = totalVolume[i][2]
        currentVol[i] = buyVolume + sellVolume - volAtBuyBack[i]

        # buyback and rewards
        if rewards[i] - rewardsPrev[i] > 25 * 10 ** 6:
            volAtBuyBack[i] = buyVolume + sellVolume
            boomBotStr += '\ud83d\udd35 ' + iStr + ' KABOOOOOOOOOOM ' + str(round((rewards[i] - rewardsPrev[i])/1000000, 6)) + 'M rewards\n'
            rewBotStr += '\ud83d\udd35 ' + iStr + ' KABOOOOOOOOOOM ' + str(round((rewards[i] - rewardsPrev[i])/1000000, 6)) + 'M rewards\n'
            bbAmount[i] = 0
            boomBotSendAudio(audioWowBoomBoom)
        elif rewards[i] - rewardsPrev[i] > 3 * 10 ** 6:
            volAtBuyBack[i] = buyVolume + sellVolume
            boomBotStr += '\ud83d\udd35 ' + iStr + ' KABOOM ' + str(round((rewards[i] - rewardsPrev[i])/1000000, 6)) + 'M rewards\n'
            rewBotStr += '\ud83d\udd35 ' + iStr + ' KABOOM ' + str(round((rewards[i] - rewardsPrev[i])/1000000, 6)) + 'M rewards\n'
            bbAmount[i] = 0
            boomBotSendAudio(audioWowBoomBoom)
        elif rewards[i] - rewardsPrev[i] > 100 * 10 ** 3 and currentVol[i] > bbThreshold:
            volAtBuyBack[i] = buyVolume + sellVolume
            boomBotStr += '\ud83d\udd35 ' + iStr + ' BOOM ' + str(
                round((rewards[i] - rewardsPrev[i]) / 1000000, 6)) + 'M rewards\n'
            rewBotStr += '\ud83d\udd35 ' + iStr + ' BOOM ' + str(
                round((rewards[i] - rewardsPrev[i]) / 1000000, 6)) + 'M rewards\n'
            bbAmount[i] = 0
        elif rewards[i] > rewardsPrev[i]:
            rewBotStr += iStr + '\tkraken is lurking around for the unworthy, ' + str(round(rewards[i] - rewardsPrev[i], 6)) + ' rewards distributed\n'

        # reward multiplier
        if rewards[i] > rewardsPrev[i]:
            rewMult = findRewardsMultiplier(rewards[i] - rewardsPrev[i], i)
            rewBotStr += '\n12 month stakers received (' + str(rewMult) + '%) of their current stake\n\n'

        # buy vs sell color
        # currentVol[i] = buyVolume + sellVolume - volAtBuyBack[i]
        if buyVolume - buyVolumePrev[i] < sellVolume - sellVolumePrev[i] and currentVol[i] > 0:
            boomBotStr += '\ud83d\udd34 '
        elif buyVolume - buyVolumePrev[i] > sellVolume - sellVolumePrev[i] and currentVol[i] > 0:
            boomBotStr += '\ud83d\udfe2 '
        else:
            boomBotStr += '\ud83d\udfe1 '

        # kraken hunger and volume
        if currentVol[i] - volPrev[i] > 15 * 10 ** 6:
            boomBotStr += 'kraken devours ' + iStr + '\t' + str(round(currentVol[i] / bbThreshold * 100, 1)) + '%\n'
        elif currentVol[i] - volPrev[i] > 5 * 10 ** 6:
            boomBotStr += 'kraken munches ' + iStr + '\t' + str(round(currentVol[i] / bbThreshold * 100, 2)) + '%\n'
        elif currentVol[i] - volPrev[i] > 1 * 10 ** 6:
            boomBotStr += 'kraken chews ' + iStr + '\t' + str(round(currentVol[i] / bbThreshold * 100, 3)) + '%\n'
        elif currentVol[i] - volPrev[i] > 0:
            boomBotStr += 'kraken gnaws ' + iStr + '\t' + str(round(currentVol[i] / bbThreshold * 100, 4)) + '%\n'
        else:
            boomBotStr += 'no action for ' + iStr + ' kraken\t' + str(round(currentVol[i] / bbThreshold * 100, 0)).replace('.0', '') + '%\n'

        # buyback amount
        if sellVolume - sellVolumePrev[i] > 10 ** 6 and currentVol[i] < bbThreshold * 1.2:
            bbAmount[i] += findKrakenBalance(i) / 1000  # inaccurate when multiple sells above 1M rise within tickRate

        # if currentVol[i] - volPrev[i] > 0:
        #     if currentVol[i] > 120 * 10 ** 6:
        #         p = int(currentVol[i] / 100*10**6)
        #         boomBotStr += 'the next buyback will happen near ' + str(p) + '00%'
        #     else:
        #         boomBotStr += iStr + ' will buyback $' + str(round(bbAmount[i], 2)) + '\n'

        buyVolumePrev[i] = buyVolume
        sellVolumePrev[i] = sellVolume
        volPrev[i] = currentVol[i]
        rewardsPrev[i] = rewards[i]
    return [boomBotStr, rewBotStr]


def run(t):
    tickRate = 120  # x sec
    # findArb()
    time.sleep(1)
    msg = check()
    toSave(volAtBuyBack, volPrev, rewardsPrev, buyVolumePrev, sellVolumePrev, bbAmount)
    volAtBuyBack.clear()
    volPrev.clear()
    rewardsPrev.clear()
    buyVolumePrev.clear()
    sellVolumePrev.clear()
    bbAmount.clear()
    if msg[0] != '':
        boomBotSend(msg[0])
    if msg[1] != '':
        rewBotSend(msg[1])
    if t % (tickRate * 1000) == (tickRate * 20):
        boomBotSend('speculating precisely')
    elif t % (tickRate * 1000) == (tickRate * 20)*5:
        boomBotSend('wen rewards')
    elif t % (tickRate * 1000) == (tickRate * 20)*10:
        boomBotSend('things happen as time goes by')
    elif t % (tickRate * 1000) == (tickRate * 20)*15:
        boomBotSend('its dangerous to go alone, take this')
    time.sleep(tickRate)
    t += tickRate

boomBotSend('\ud83d\udd25 start')
while True:
    try:
        run(tt)
    except:
        time.sleep(20)
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
