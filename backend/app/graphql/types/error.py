from typing import Optional
import strawberry


@strawberry.type
class Error:
    message: str
