import logging

__logger = None


def get_logger() -> logging.Logger:
	global __logger
	if not __logger:
		__logger = logging.getLogger()
		__logger.setLevel(logging.INFO)
		file_handler = logging.FileHandler(f"logs/logs.log", mode="w")
		formatter = logging.Formatter("%(asctime)s (%(name)s): %(levelname)s %(message)s\n")
		file_handler.setFormatter(formatter)
		__logger.addHandler(file_handler)
	return __logger
