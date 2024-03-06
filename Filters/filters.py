from aiogram.filters import BaseFilter
from aiogram.types import Message

from Config_data.config import Config, load_config

config: Config = load_config()


class IsAdmin(BaseFilter):

    admin_id = config.admin.Admin

    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) == self.admin_id