from typing import Union, Optional
from urllib.parse import quote

import aiohttp
import types

from .utils import Attrify as attr
from .exceptions import *
from .types import Language

class Piston:
    def __init__(
        self,
        base_url: Optional[str] = "https://emkc.org/api/v2/piston"
    ):
        """Setup all urls and session."""
        self.base_url = base_url

    async def execute(
        self,
        language=str,
        source=str,
        version=str,
        stdin: str = None,
        args: list = None
    ) -> attr:
        url = f"{self.base_url}/execute"
        data = {
            'language': language,
            'version': version,
            'files': source
        }
        if stdin:
            data['stdin'] = stdin
        if args:
            data['args'] = args
        async with aiohttp.ClientSession() as ses:
            async with ses.post(url, data=data) as resp:
                try:
                    return attr((await resp.json()))
                except aiohttp.client_exceptions.ContentTypeError:
                    raise EndpointDown("Client cannot reach the Endpoint")
            await ses.close()

    async def versions(self) -> None:
        url = f"{self.base_url}/runtimes"
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as resp:
                out = await resp.json()
                vers = []
                try:
                    for l in out:
                        vers.append(Language(l))
                    return (vers)
                except aiohttp.client_exceptions.ContentTypeError:
                    raise EndpointDown("Client cannot reach the Endpoint")
            await ses.close()
        
        