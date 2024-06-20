from loguru import logger 

class Logger:
    def __new__(cls):
        log_file_path = "~/.pybox/pybox.log"
        log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        log_level = "DEBUG"
        log_rotation = "10 MB"

        logger.remove()  # 移除默认的logger配置
        logger.add(log_file_path, format=log_format, level=log_level, rotation=log_rotation)

        return logger