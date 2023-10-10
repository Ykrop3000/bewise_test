from typing import List

import aiohttp

async def fetch_random_question(question_num: int) -> List[dict]:
    async with aiohttp.ClientSession() as session:
        res = await session.get(f'https://jservice.io/api/random?count={question_num}')
        res_json = await res.json()
        return res_json