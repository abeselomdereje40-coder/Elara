from dataclasses import dataclass
from typing import Optional

@dataclass
class ImageRequest:
    prompt:str
    negative_prompt:Optional[str]=None
    width:int=512
    height:int=512
    seed:Optional[int]=None

@dataclass
class ImageResult:
    success:bool
    image_path:Optional[str]=None
    error:Optional[str]=None