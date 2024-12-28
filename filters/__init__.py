from loader import dp
from .Admin import IsAdmin
from .Admin import IsAdmin_bot
from .Group import IsGroup
from .Chat import IsPrivate
if __name__ == 'filters':
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsAdmin_bot)