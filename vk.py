import aiohttp
import asyncio

async def fetch_status():
    url = 'https://api.vk.com/method/status.get'
    access_token = 'vk1.a.MyyhirpsAX0bp56l9iZXs7e_VHxv2RvJR0xox_xeTe8o2RQvgAvYRsogk7O6ntWZxAb6T9crCLfg7ZkSwXycsPp_qGDU8t-CdBQ8_88Qt2xSAXy2RuafXjK3mwusyomPqUn3JFzo9fmYe5Ii2LmovhSrQxZ1zUYyvyOjjMtL1hHl-UGB_0n6q9TqPw8fSti0sdHcy8sPDNc55gvdZFkeow'
    user_id = 'user_id_here'
    
    params = {
        'access_token': access_token,
        'v': '5.199'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            response_json = await response.json()
            return response_json

async def main():
    status = await fetch_status()
    print(status["response"]["audio"])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
