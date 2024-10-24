from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import asyncio
from playwright.async_api import async_playwright
import uuid
from random import randint

app = FastAPI()

class TrackingRequest(BaseModel):
    number: str

class VesselInfo(BaseModel):
    name: str
    mmsi: str
    imo: str
    trip_data: list

def get_proxy_v3():
    uid = uuid.uuid4()
    num = uid.hex
    proxy_port=str(randint(10000, 19999))
    print(num, proxy_port)
    proxy= f"user-rdhtiwari-country-in-sessionduration-15-{num}:z1lHqev@in.smartproxy.com:{proxy_port}"
    proxy_dict= {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    print(f"###################   Fetching Proxy:{proxy_port} :  {proxy}")
    return proxy_dict

async def scrape_vessel_data(vessel_name: str, mmsi: str, imo: str):
    url = f'https://www.myshiptracking.com/vessels/{vessel_name}-mmsi-{mmsi}-imo-{imo}'
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Calling the URL inside playwright page")
        await page.goto(url)
        await page.wait_for_selector('#ft-trip .table')
        print("Got the first selector")

        rows = await page.locator('#ft-trip .table tr').all()
        data_list = []
        
        for row in rows:
            data_dict = {}
            th_elements = await row.locator('th').all_text_contents()
            td_elements = await row.locator('td').all_text_contents()

            if th_elements and td_elements:
                key = th_elements[0].strip()
                value = td_elements[0].strip()
                data_dict[key] = value
                data_list.append(data_dict)

        await browser.close()
        return data_list

@app.post("/track", response_model=VesselInfo)
async def track_container(request: TrackingRequest):
    print("INSIDE THE POST CALL")
    tracking_number = request.number

    url = f"https://www.searates.com/tracking-system/reverse/tracking?route=true&last_successful=false&number={tracking_number}"

    payload = {}
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.searates.com/container/tracking/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-a59de49a63e8e421e0f8688276fe7f41-431a73243a947e41-01',
    'tracestate': '2914910@nr=0-1-3461589-388581761-431a73243a947e41----1727333521615',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'x-referer': 'https://www.searates.com/',
    'Cookie': 'PHPSESSID=6c8tq8ot60upo0a71ovenfatip; __cf_bm=jApwhQpCLW5qVJFKXLg_uaF.Ggk9wl59MR87.B6ykNA-1727346561-1.0.1.1-R5_hksfeH_fXnebGaUMpNMIC1t_dCnxRugsZrRDNp0.d3M7iRpOON0UdPEufCmPxsa6vbTXYN3iwX3Hb3wGjnw'
    }

    print("--------PROXIES--------")
    print(get_proxy_v3())

    response = requests.request("GET", url, headers=headers, data=payload, proxies=get_proxy_v3())

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching tracking data")

    data = response.json()
    print(data)
    
    if data['status'] != "success":
        raise HTTPException(status_code=400, detail="Tracking data not found")

    # url = f"https://www.searates.com/tracking-system/reverse/tracking?route=true&last_successful=false&number={tracking_number}"

    # payload = {}
    # headers = {
    # 'accept': 'application/json, text/plain, */*',
    # 'accept-language': 'en-US,en;q=0.9',
    # 'priority': 'u=1, i',
    # 'referer': 'https://www.searates.com/container/tracking/',
    # 'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'same-origin',
    # 'traceparent': '00-a59de49a63e8e421e0f8688276fe7f41-431a73243a947e41-01',
    # 'tracestate': '2914910@nr=0-1-3461589-388581761-431a73243a947e41----1727333521615',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    # 'x-referer': 'https://www.searates.com/',
    # # 'Cookie': 'PHPSESSID=6c8tq8ot60upo0a71ovenfatip; __cf_bm=jApwhQpCLW5qVJFKXLg_uaF.Ggk9wl59MR87.B6ykNA-1727346561-1.0.1.1-R5_hksfeH_fXnebGaUMpNMIC1t_dCnxRugsZrRDNp0.d3M7iRpOON0UdPEufCmPxsa6vbTXYN3iwX3Hb3wGjnw'
    # }

    # response = requests.request("GET", url, headers=headers, data=payload)

    # if response.status_code != 200:
    #     raise HTTPException(status_code=response.status_code, detail="Error fetching tracking data")

    # data = response.json()
    # print(data)
    
    # if data['status'] != "success":
    #     raise HTTPException(status_code=400, detail="Tracking data not found")

    vessel_name = data['data']['vessels'][0]['name'].lower().replace(" ", "-")
    mmsi = str(data['data']['vessels'][0]['mmsi'])
    imo = str(data['data']['vessels'][0]['imo'])

    print("Calling the scrape vessel function")
    trip_data = await scrape_vessel_data(vessel_name, mmsi, imo)
    trip_data.append(data)

    return VesselInfo(name=vessel_name, mmsi=mmsi, imo=imo, trip_data=trip_data)

