from dataclasses import dataclass
from typing import Any

@dataclass()
class SimpleArticle(object):
    """A unified way to handle the textual content"""

    title : str = ""
    summary : str = ""
    content : str = ""
    link : str = ""
    source : str = ''
    time_published: Any = ""    # Hopefully, a datetime
    original_data : Any = ""
    
