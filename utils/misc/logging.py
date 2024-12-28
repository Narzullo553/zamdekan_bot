import logging
import sys

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    handlers=[
                        logging.FileHandler('bot.log'),
                        logging.StreamHandler(sys.stdout)
                    ],
                    level=logging.INFO,
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )
