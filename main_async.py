import asyncio
import httpx
import tqdm


async def download_files(url: str, filename: str):
    with open(filename, 'wb') as f:
        async with httpx.AsyncClient() as client:
            async with client.stream('GET', url) as r:
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))
                tqdm_params = {
                    'desc': url,
                    'total': total,
                    'miniters': 1,
                    'unit': 'it',
                    'unit_scale': True,
                    'unit_divisor': 1024,
                }
                with tqdm.tqdm(**tqdm_params) as pb:
                    async for chunk in r.aiter_bytes():
                        pb.update(len(chunk))
                        f.write(chunk)


async def main():
    loop = asyncio.get_event_loop()
    urls = [
        ('https://download.samplelib.com/mp4/sample-5s.mp4', '5s.mp4'),
        ('https://download.samplelib.com/mp4/sample-10s.mp4', '10s.mp4'),
        ('https://download.samplelib.com/mp4/sample-15s.mp4', '15s.mp4'),
    ]

    tasks = [loop.create_task(download_files(url, filename)) for url, filename in urls]
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())
