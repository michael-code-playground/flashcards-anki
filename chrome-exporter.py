
from datetime import datetime, timedelta
import json
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

#determine current time
time_now = datetime.now()

#convert to a timestamp and round
timestamp_now = round(time_now.timestamp())

#specify a time in days to extract data from
interval = timedelta(days = 62)

#open the browsing history
with open('History.json', encoding='UTF-8') as file:
    records = json.load(file)
    
    #search through records
    for record in records['Browser History']:
        
        #extract search time, change its format
        search_time = round(record['time_usec']/1000000)
        changed_time = datetime.fromtimestamp(search_time)
        difference = time_now-changed_time
        
        #set the file name
        file_name = 'pronunciation_' + str(time_now.date()) + '.csv'
        
        if "dictionary.cambridge" in record['url']:
            
            #put data in the file
            with open(file_name, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';',quotechar='"')
                formatted_name = record['title'].split('|')[0]
                writer.writerow([formatted_name, record['url'], changed_time])
            
        #break if time interval is reached
        if difference.days == interval.days:
            break

#sort, remove duplicates, save
sheet = pd.read_csv(file_name, sep=';', encoding='UTF-8')
sheet.sort_values(by=sheet.columns[2], ascending=False, inplace=True)
sheet.drop_duplicates(subset=sheet.columns[0], keep='first', inplace=True)
pd.DataFrame.to_csv(sheet, path_or_buf=file_name, sep=';', index=False)

# url="https://dictionary.cambridge.org/dictionary/english/object"
# #headers = {
#     #'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
#     #'Accept-Encoding':'gzip, deflate, br',
#     #'Accept-Language':'pl,en-US;q=0.7,en;q=0.3',
#     #'Cache-Control':'no-cache',
#     #'Connection':'keep-alive',
#     #'Cookie':'_ga=GA1.3.1351901234.1690820720; amp-access=amp-Dckv1GCrA3ZYoFGPMnO8_A; preferredDictionaries=^\^"english-polish,english,british-grammar,english-russian^\^"; iawpvccs=1; _fbp=fb.1.1690820721611.2083075929; OptanonAlertBoxClosed=2023-07-31T16:25:23.159Z; _sharedID=f2ee6725-841b-4cca-814d-935f1838e7cd; OTAdditionalConsentString=1~61.70.89.93.108.122.124.136.143.144.147.149.159.192.196.202.211.228.230.239.259.266.291.311.317.323.338.371.385.394.397.407.413.415.424.430.436.482.486.491.494.495.522.523.540.550.559.568.574.576.584.591.737.802.803.820.821.839.864.899.922.981.1051.1095.1097.1201.1205.1276.1301.1365.1415.1421.1449.1570.1577.1651.1716.1765.1870.1878.1889.2008.2072.2074.2135.2253.2299.2322.2328.2357.2465.2501.2526.2568.2571.2575.2677.2958.2999.3028.3225.3226.3231.3234.3235.3236.3237.3238.3240.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3295.3296.3299.3300.3306.3307.3314.3315.3316.3318.3324.3327.3328.3330.3331.3531.3731.3831.3931.4131.4531.4631.4731.4831.5031.5231.6931.7031.7235.7831.7931.8931.9731.10231; _tfpvi=N2VkNjU0YzUtYWMyYy00ZWU1LWJhZWQtNzZhNDMzNTQwZDllIzkw; iawppid=3ceb5ecadaee43f0b64fc98fede8990a; iawpvc1m=1; _lr_env_src_ats=false; pbjs-unifiedid=^%^7B^%^22TDID_LOOKUP^%^22^%^3A^%^22FALSE^%^22^%^2C^%^22TDID_CREATED_AT^%^22^%^3A^%^222023-07-31T16^%^3A25^%^3A27^%^22^%^7D; _gid=GA1.3.2047955064.1691414809; iawsc1m=2; iawpvc=2; iawpvtc1m=2; _hjSessionUser_2790984=eyJpZCI6ImQ4NGE1ODA2LWYyZjAtNWU1OS1hNTA0LWRlN2MzM2I0Njg2MiIsImNyZWF0ZWQiOjE2OTA4MjA3MjE0NDYsImV4aXN0aW5nIjp0cnVlfQ==; eupubconsent-v2=CPvxKXAPvxKXAAcABBENDRCsAP_AAH_AAChQJWJD7T7FYSnC-PZ4fLsQcAhHR9TkA6QACASAAmABAAKQIIQCkmAYlAQgBAgCAAAgAAJBAAIECAEACUAAwAAAIQAEAAAABAAIACAAgAARAkAICAACAAAAAAAIgAAAEAAAmwgAQIIACEgABAAAAAAAAAgAAAAAAgAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAD8EqoEgACwAHgAVAAuABkADgAIAASAAyABoAD8AKwAfgBCACOAEwAKMAUoAwACEAERAI6AZ8A14BxIDpAOoAeQBF4CYgF_gMEAZYA7ECFQEqAJVAJggAQAiwFNhICYAPIAhgCIAEwAJ4AVQAsQCIAIkAUoAtwBhgD2AH6AQMAkwBTwDFAKRAXmAycIAFAEWANQBHoCbAFNhgAwATwBFgDUANkAmwBTYaACAU8QAFACeAIsAagCbAFNiIAIBTxUAEAIYoAGANQBHoCbBkAEAIYwAGANQBHoCbB0BkAHkAQwBEACYAE8AKoAWAAugBiADNAIgAiQBSgC3AGGANEAewA_QCBgEWAJMAU8AxQC8wF9AMnAZYOADABfAGoAVkBHoCbAFNkIA4AQwAmABVADEAU8AxQDJyAAUAL4A1ACsgI9ATYSgFgA8ACIAEwAKoAYoBEAESALcAp4BigF5gMnJABQAvgDUAKyAj0BNhSAkADyAIYAiABMACeAFUALAAYgAzQCIAIkAUoAtwBogD9AIsAYoBeYC-gGTlAAwAXwBqAFZAR6AmwBTY.f_gAD_gAAAAA; _pbjs_userid_consent_data=6878694398241685; AMP_MKTG_067b9b07c8=JTdCJTdE; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Aug+07+2023+15^%^3A26^%^3A52+GMT^%^2B0200+(czas+^%^C5^%^9Brodkowoeuropejski+letni)&version=202303.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=771a460d-bfe7-4d45-a0d6-4ff9a0139e1c&interactionCount=1&landingPath=NotLandingPage&groups=C0001^%^3A1^%^2CC0002^%^3A1^%^2CC0003^%^3A1^%^2CC0004^%^3A1^%^2CSTACK42^%^3A1&geolocation=PL^%^3B24&AwaitingReconsent=false; _sp_id.7ecc=c192e2c4-5cc4-4761-8011-dc9c12413e18.1690820724.2.1691414812.1690820724.cb881980-8fe4-49df-8685-71222c45a801.fddc4bb3-5e0a-4545-8a57-91bcbb3932f3...0; cto_bidid=sFViNl9YNHFoUE9LJTJCd3FyZFpreGlHb3RvZVJkclpqVHhLWHdDTmp6Zmt6bGE4a1M1NE9RU2ZleElzMHhXNnVVZU91Mjl4WUF4NmlkcCUyRkl5JTJGam5sNTVMeFB4STh6NHdGbWlrJTJGU1BrJTJCYWFpQVF4c2clM0Q; AMP_067b9b07c8=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI3NTc3NmQ3ZS05MGJiLTRjMTktODU0ZS1mNDEyMDgwMGEzMzUlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNjkxNDE0ODExNjM4JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTY5MTQxNDgxNzU1NyUyQyUyMmxhc3RFdmVudElkJTIyJTNBMiU3RA==; cto_bundle=OtkIjV85cE91JTJGU2hGU2tyNDVqVmNxSVN4Z21DdkdGTWdzVWwlMkZpT0hXc3BPazRmMnZ4Z1NBUWZEU2NNVEFXcVc5TGQ2dGQxUDJLOUJzRWREa2hzbFN2JTJGbDhuTGcwSWtXTCUyRk5IUHBaYVlSczdZb0lRSThpJTJGcWx4MXBwUVBSY2wxbXV4dFN3dUlJa1dlVXBKZUplTGFaUWFDUFFnJTNEJTNE; __gads=ID=af0699bd21dfe691:T=1690820724:RT=1691416361:S=ALNI_MauwRYfRqvRbXu3ujYQXh9RfPzyzQ; __gpi=UID=00000c4ae3c4eee5:T=1690820724:RT=1691416361:S=ALNI_MYF3iueC1Uz0dnb2MJ9Z-R3vQChRA; _ga_L9GCR21SZ7=GS1.3.1691416967.3.0.1691416967.60.0.0; XSRF-TOKEN=4bf1854c-5b13-4fa0-b394-f86aa9028ef7; loginPopup=3',
#     #'Host':'dictionary.cambridge.org',
#     #'Pragma':'no-cache',
#     #'Sec-Fetch-Dest':'document',
#    # 'Sec-Fetch-Mode':'navigate',
#     #'Sec-Fetch-Site':'cross-site',
#     #'Upgrade-Insecure-Requests':'1',
#    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0'
#    # }

# headers = {
#    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#    'Accept-Language': 'pl-PL,pl;q=0.9,de-DE;q=0.8,de;q=0.7,en-GB;q=0.6,en;q=0.5,en-US;q=0.4',
#    'Cache-Control': 'max-age=0',
#    'Connection': 'keep-alive', 
#    'Cookie': '_ga=GA1.3.1351901234.1690820720; amp-access=amp-Dckv1GCrA3ZYoFGPMnO8_A; preferredDictionaries=^\^"english-polish,english,british-grammar,english-russian^\^"; iawpvccs=1; _fbp=fb.1.1690820721611.2083075929; OptanonAlertBoxClosed=2023-07-31T16:25:23.159Z; _sharedID=f2ee6725-841b-4cca-814d-935f1838e7cd; OTAdditionalConsentString=1~61.70.89.93.108.122.124.136.143.144.147.149.159.192.196.202.211.228.230.239.259.266.291.311.317.323.338.371.385.394.397.407.413.415.424.430.436.482.486.491.494.495.522.523.540.550.559.568.574.576.584.591.737.802.803.820.821.839.864.899.922.981.1051.1095.1097.1201.1205.1276.1301.1365.1415.1421.1449.1570.1577.1651.1716.1765.1870.1878.1889.2008.2072.2074.2135.2253.2299.2322.2328.2357.2465.2501.2526.2568.2571.2575.2677.2958.2999.3028.3225.3226.3231.3234.3235.3236.3237.3238.3240.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3295.3296.3299.3300.3306.3307.3314.3315.3316.3318.3324.3327.3328.3330.3331.3531.3731.3831.3931.4131.4531.4631.4731.4831.5031.5231.6931.7031.7235.7831.7931.8931.9731.10231; _tfpvi=N2VkNjU0YzUtYWMyYy00ZWU1LWJhZWQtNzZhNDMzNTQwZDllIzkw; iawppid=3ceb5ecadaee43f0b64fc98fede8990a; iawpvc1m=1; _lr_env_src_ats=false; pbjs-unifiedid=^%^7B^%^22TDID_LOOKUP^%^22^%^3A^%^22FALSE^%^22^%^2C^%^22TDID_CREATED_AT^%^22^%^3A^%^222023-07-31T16^%^3A25^%^3A27^%^22^%^7D; _gid=GA1.3.2047955064.1691414809; _hjSessionUser_2790984=eyJpZCI6ImQ4NGE1ODA2LWYyZjAtNWU1OS1hNTA0LWRlN2MzM2I0Njg2MiIsImNyZWF0ZWQiOjE2OTA4MjA3MjE0NDYsImV4aXN0aW5nIjp0cnVlfQ==; eupubconsent-v2=CPvxKXAPvxKXAAcABBENDRCsAP_AAH_AAChQJWJD7T7FYSnC-PZ4fLsQcAhHR9TkA6QACASAAmABAAKQIIQCkmAYlAQgBAgCAAAgAAJBAAIECAEACUAAwAAAIQAEAAAABAAIACAAgAARAkAICAACAAAAAAAIgAAAEAAAmwgAQIIACEgABAAAAAAAAAgAAAAAAgAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAD8EqoEgACwAHgAVAAuABkADgAIAASAAyABoAD8AKwAfgBCACOAEwAKMAUoAwACEAERAI6AZ8A14BxIDpAOoAeQBF4CYgF_gMEAZYA7ECFQEqAJVAJggAQAiwFNhICYAPIAhgCIAEwAJ4AVQAsQCIAIkAUoAtwBhgD2AH6AQMAkwBTwDFAKRAXmAycIAFAEWANQBHoCbAFNhgAwATwBFgDUANkAmwBTYaACAU8QAFACeAIsAagCbAFNiIAIBTxUAEAIYoAGANQBHoCbBkAEAIYwAGANQBHoCbB0BkAHkAQwBEACYAE8AKoAWAAugBiADNAIgAiQBSgC3AGGANEAewA_QCBgEWAJMAU8AxQC8wF9AMnAZYOADABfAGoAVkBHoCbAFNkIA4AQwAmABVADEAU8AxQDJyAAUAL4A1ACsgI9ATYSgFgA8ACIAEwAKoAYoBEAESALcAp4BigF5gMnJABQAvgDUAKyAj0BNhSAkADyAIYAiABMACeAFUALAAYgAzQCIAIkAUoAtwBogD9AIsAYoBeYC-gGTlAAwAXwBqAFZAR6AmwBTY.f_gAD_gAAAAA; _pbjs_userid_consent_data=6878694398241685; AMP_MKTG_067b9b07c8=JTdCJTdE; XSRF-TOKEN=ab574085-c319-4085-8ade-fc28218a1bc7; _gat=1; _ga_L9GCR21SZ7=GS1.3.1691480186.5.0.1691480186.60.0.0; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Aug+08+2023+09^%^3A36^%^3A27+GMT^%^2B0200+(czas+^%^C5^%^9Brodkowoeuropejski+letni)&version=202303.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=771a460d-bfe7-4d45-a0d6-4ff9a0139e1c&interactionCount=1&landingPath=NotLandingPage&groups=C0001^%^3A1^%^2CC0002^%^3A1^%^2CC0003^%^3A1^%^2CC0004^%^3A1^%^2CSTACK42^%^3A1&geolocation=PL^%^3B24&AwaitingReconsent=false; iawsc1m=4; iawpvc=4; iawpvtc1m=4; _hjIncludedInSessionSample_2790984=0; _hjSession_2790984=eyJpZCI6ImY3ODViNzYzLWNhMjktNDNiNi1hMjY3LTllNzQ1ZTU3MDZjOSIsImNyZWF0ZWQiOjE2OTE0ODAxODc0NDYsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _hjHasCachedUserAttributes=true; _sp_ses.7ecc=*; _sp_id.7ecc=c192e2c4-5cc4-4761-8011-dc9c12413e18.1690820724.3.1691480188.1691414812.8859d80f-7e1e-4b65-ad8c-c99e071f83ab.cb881980-8fe4-49df-8685-71222c45a801...0; __gads=ID=af0699bd21dfe691:T=1690820724:RT=1691480188:S=ALNI_MauwRYfRqvRbXu3ujYQXh9RfPzyzQ; __gpi=UID=00000c4ae3c4eee5:T=1690820724:RT=1691480188:S=ALNI_MYF3iueC1Uz0dnb2MJ9Z-R3vQChRA; AMP_067b9b07c8=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI3NTc3NmQ3ZS05MGJiLTRjMTktODU0ZS1mNDEyMDgwMGEzMzUlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNjkxNDgwMTkxNzQ0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTY5MTQ4MDE5MjMxOSUyQyUyMmxhc3RFdmVudElkJTIyJTNBNCU3RA==; _lr_retry_request=true; cto_bundle=cQcfBl85cE91JTJGU2hGU2tyNDVqVmNxSVN4Z29LY3VPVWp5c0c2c29lN0VGR0Qzc2U0VUdINUVrJTJGMkJuRUxpTmlQVkVjek81bWFHQzhqSUs3RzZCSmhGbzU1U3JIJTJCTWhFQ1hNcUhFQ01hc1BzemNGMDhxb1MxdHN3TE1WREJVN0sxSSUyQkpnd3VWaSUyQiUyQkRlRG5PSmxJU2F4UUIxRWclM0QlM0Q; cto_bidid=JkAWwl9YNHFoUE9LJTJCd3FyZFpreGlHb3RvZVJkclpqVHhLWHdDTmp6Zmt6bGE4a1M1NE9RU2ZleElzMHhXNnVVZU91Mjl4WUF4NmlkcCUyRkl5JTJGam5sNTVMeFB4QjJMMWhaZmFYJTJCWGg5dGo5dUkyS1lnJTNE; loginPopup=7',
#    'Sec-Fetch-Dest': 'document',
#    'Sec-Fetch-Mode': 'navigate', 
#    'Sec-Fetch-Site': 'none', 
#    'Sec-Fetch-User': '?1', 
#    'Upgrade-Insecure-Requests': '1', 
#    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
#    'sec-ch-ua': '^\^"Not/A)Brand^\^";v=^\^"99^\^", ^\^"Google Chrome^\^";v=^\^"115^\^", ^\^"Chromium^\^";v=^\^"115^\^""',
#    'sec-ch-ua-mobile': '?0',
#    'sec-ch-ua-platform': '^\^"Windows^\^""'



# }
# time.sleep(2)
# r = requests.get(url, headers=headers)

# doc = BeautifulSoup(r.text, "html.parser")

# with open("response.html", "w", encoding="utf-8") as f:
#     f.write(r.text)

# for characters in doc.select(".ipa dipa lpr-2 lpl-1"):
#     print(characters)

#search through products
#for product in doc.select(".cat-prod-row"):
    #price = product.select_one(".value").text
    #link = product.select_one(".go-to-product").attrs["href"]
    #memory = product.select(".cat-prod-row__params strong")[3].text