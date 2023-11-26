import logging

__logger = None


def get_logger() -> logging.Logger:
	global __logger
	logs_format = "%(asctime)s (%(name)s): %(levelname)s %(message)s"
	if not __logger:
		logging.basicConfig(
			level=logging.INFO,
			format=logs_format,
			datefmt="%Y-%m-%d %H:%M",
			filename="logs/logs.log",
			filemode="w"
		)
		console = logging.StreamHandler()
		console.setLevel(logging.INFO)
		formatter = logging.Formatter(logs_format)
		console.setFormatter(formatter)
		__logger = logging.getLogger()
		__logger.addHandler(console)
	return __logger

