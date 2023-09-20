import requests
import httpx

headers = {
    "authority": "spa16.scrape.center",
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31",
}

# params = (
#     ("limit", "20"),
#     ("offset", "200"),
# )

# client = httpx.Client(http2=True)

# req = httpx.Request(
#     "GET", "https://spa16.scrape.center/api/book", headers=headers, params=params
# )

# resp = client.send(req, follow_redirects=True)


# x = resp.json()

# print(x)
# response = requests.get(
#     "https://spa16.scrape.center/api/book", headers=headers, params=params
# )

# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('https://spa16.scrape.center/api/book?limit=18&offset=0', headers=headers)
# print(response.json())
import httpx
import random
import datetime
import json
import asyncio
import time

result_list = []


async def request(client, params, sem):
    async with sem:
        resp = await client.request(
            "GET",
            "https://spa16.scrape.center/api/book",
            headers=headers,
            params=params,
            follow_redirects=True,
        )
        resp.encoding = "utf-8"
        result = resp.json()
        result_list.append({params[-1][-1]: result})
        print(result)


async def main():
    sem = asyncio.Semaphore(3)
    async with httpx.AsyncClient(http2=True, default_encoding="utf-8") as client:
        start = time.time()
        task_list = []
        for i in range(113):
            params = (
                ("limit", "80"),
                ("offset", 80 * i),
            )
            req = request(client, params, sem)
            task = asyncio.create_task(req)
            task_list.append(task)
        await asyncio.gather(*task_list)
        end = time.time()
    print(f"发送100次请求，耗时：{end - start}")


asyncio.run(main())
print(result_list)
with open("result.txt", "w", encoding="utf-8") as f:
    f.write(json.dumps(result_list, ensure_ascii=False))
