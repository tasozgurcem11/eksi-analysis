import requests
from bs4 import BeautifulSoup
import pandas as pd


def crawl_eksi_updated():

    headers = {
        'authority': 'eksisozluk.com',
        'accept': '*/*',
        'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'ASP.NET_SessionId=zsiblpffhj44n5ta42noeggw; channel-filter-preference-cookie=W3siSWQiOjEsIlByZWYiOnRydWV9LHsiSWQiOjIsIlByZWYiOnRydWV9LHsiSWQiOjQsIlByZWYiOnRydWV9LHsiSWQiOjUsIlByZWYiOnRydWV9LHsiSWQiOjEwLCJQcmVmIjpmYWxzZX0seyJJZCI6MTEsIlByZWYiOmZhbHNlfSx7IklkIjozOSwiUHJlZiI6ZmFsc2V9XQ==; _ga=GA1.2.1408552547.1604684912; __RequestVerificationToken=jSRMTU3Xw--zuoB4unbAlT0Vxzf3iw9aCicXz5HPO57DuhRq-row8v_IoSUMrRs3ytdehfvUnQj5hfLqi4Dmm6KQKBy-EGzKTcT9hvW8jv81; gadsTest=test; cookies_info_viewed=yes; __qca=P0-1389389516-1629211620330; iq=37aa2631fdab41f0943cc9d34fbf02c4; __gads=ID=b431719aa91474a5:T=1639835257:S=ALNI_Mb05hFA5ozUvdOHtQdnoE1AhDtcfg; cf_clearance=C_xKA1BY.Y2815bSft2cGLF2.ZbQ41_68etko7b3_Ho-1640033783-0-150; OptanonAlertBoxClosed=2022-02-14T14:10:42.505Z; __auc=043911db18056df7c04c9eaf3c5; led_msg=; FCNEC=[["AKsRol92lGwWgewmKyJlv6lLXZ6MUpjeaggVhQGtWlUj_vixn-yV7twoHFap_pWfv1IbaWg7DjvMtF5VPg3BTmQ-zrIb2z_FRxgj-9fsGvS1RletpBfRZK1r4EVquEuIHhlJyE0s7CXfYYEL2BImxYFhxlZuEi4ing=="],null,[]]; _gid=GA1.2.1069717626.1657479352; a=ob35Lds34FsHkUDYI0KuSbmedfXb6sArzN3vbeWNnk9Yby2iv/H5A2Z+UT8jDqbmp/syuMsY6lr01BLUTaJcvicTfCArHxC56Dj4LSY5YY6Am/wqBUUf6uyhdR4iStHz0P9DZN0f0sPzdlajbIvn0cjqA92bDaosqnUxsrZWCTIEZJLhCyV82+vex3osrDNR; __gfp_64b=tblngPAnzx9iXn51Cny8xJmmh8NJ83i74f8tIFEwMY7.F7|1638519162; __gpi=UID=000002280cf58ceb:T=1646119780:RT=1658643921:S=ALNI_Mbh_LfltZV4ViyjQmuWUqJ14u0udw; led_tra=1; led_evt=1; cto_bundle=75pk_V85Rnd2dFdKeSUyQkJxem93UUpnZ0VreElEN25MbW55MGJIOU5ZajNreWpMZWclMkZmWld6Q3N2V2s3MUY1VVlHYk5BMldpY0Q4aTY2cGE0a2lsbUNWdlg5cE9hQ0VjNmRRNzFjcHFLQVlHeXZRMnclMkZYWVA2T01IODdTREZ4a2c4ZUpPaVh2b0YlMkY4MkRJdlJBaXBWQUdZVDNSNFJpaVVQUk1kdXhFd3FQNFhLblFSQmZwa3VFUmViZkR6cEpXR1NXUjE3Z2xYZEVmanE2TzNxV0U4QkhWMVZMc1ElM0QlM0Q; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Jul+24+2022+13%3A11%3A38+GMT%2B0300+(GMT%2B03%3A00)&version=6.34.0&isIABGlobal=false&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&hosts=H32%3A1%2CH43%3A1%2CH33%3A1%2CH34%3A1%2CH35%3A1%2CH2%3A1%2CH3%3A1%2CH4%3A1%2CH5%3A1%2CH36%3A1%2CH6%3A1%2CH7%3A1%2CH9%3A1%2CH10%3A1%2CH37%3A1%2CH11%3A1%2CH12%3A1%2CH13%3A1%2CH27%3A1%2CH14%3A1%2CH38%3A1%2CH39%3A1%2CH44%3A1%2CH16%3A1%2CH18%3A1%2CH40%3A1%2CH19%3A1%2CH20%3A1%2CH21%3A1%2CH41%3A1%2CH42%3A1%2CH22%3A1%2CH45%3A1&AwaitingReconsent=false&genVendors=&geolocation=TR%3B34&consentId=19272a5a-0cbf-4b22-bdfd-e2b225c3731d&interactionCount=0; _dc_gtm_UA-2362171-2=1',
        'referer': 'https://eksisozluk.com/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    # Insert entries as dictionary to the data_dict_list:
    data_dict_list = []

    for i in range(5):
        params = {
            'p': f"{str(i+1)}",
            '_': '1658657496403',
        }
        response = requests.get('https://eksisozluk.com/basliklar/gundem', params=params, headers=headers)

        raw_data = response.text
        soup = BeautifulSoup(raw_data, 'html.parser')

        for soup_item in soup.find_all('a')[1:-1]:

            number_of_entries = soup_item.text.split(' ')[-1]

            if number_of_entries.isdigit():
                entry = soup_item.text.replace(f' {number_of_entries}', '')
                number_of_entries = int(number_of_entries)

            else:
                entry = soup_item.text
                number_of_entries = 1

            data_dict_list.append({'title': entry,
                                   'entries': number_of_entries})

    entries_df = pd.DataFrame(data_dict_list)

    return entries_df


