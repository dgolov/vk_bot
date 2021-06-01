from pymysql.cursors import DictCursor
import logging.config


# ----------------------- #
#    Data base sitting    #
# ----------------------- #

DATABASE = {
    'host': 'localhost',
    'user': 'root',
    'db': 'vk_bot',
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}


# ----------------------- #
#     Logging setting     #
# ----------------------- #

log_config = {
    'version': 1,
    'formatters': {
        'bot_formatter': {
            'format': '%(asctime)s - %(name)s -%(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'bot_formatter',
            'filename': 'events.log'
        }
    },
    'loggers': {
        'bot_logger': {
            'handlers': ['file_handler'],
            'level': 'INFO'
        }
    }
}

logging.config.dictConfig(log_config)
log = logging.getLogger('bot_logger')
