import logging
from logging import DEBUG,ERROR,INFO, WARNING
import os
import time


_DIRECTORIO_LOGS = None
_NOMBRE_LOG_PREDEFINIDO = "SSHake"
_NIVEL_LOGS = DEBUG

_loggers = {}

def set_metadata(log_directory=_DIRECTORIO_LOGS,log_app_name=_NOMBRE_LOG_PREDEFINIDO,log_level=_NIVEL_LOGS):
    global _DIRECTORIO_LOGS
    global _NOMBRE_LOG_PREDEFINIDO
    global _NIVEL_LOGS

    if isinstance(log_level,str):
        if log_level=="DEBUG":
            log_level=DEBUG
        elif log_level=="ERROR":
            log_level=ERROR
        elif log_level=="INFO":
            log_level=INFO
        elif log_level=="WARNING":
            log_level=WARNING

    _DIRECTORIO_LOGS = log_directory if log_directory else _DIRECTORIO_LOGS
    _NOMBRE_LOG_PREDEFINIDO = log_app_name if log_app_name else _NOMBRE_LOG_PREDEFINIDO
    _NIVEL_LOGS = log_level if log_level else _NIVEL_LOGS


def make_directory_if_not_exists(path):
    if not os.path.isdir(path):
        intentos = 0

        while intentos < 6:
            intentos = intentos + 1
            try:
                os.makedirs(path)
                break
            except OSError as _:
                time.sleep(1)

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


#The background is set with 40 plus the number of the color, and the foreground with 30

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

def colored_message(message,color):
    return formatter_message(f"$COLOR_{color}{message}$RESET",use_color=True)

def bold_message(message):
    return formatter_message(f"$BOLD{message}$RESET",use_color=True)


def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
        for color in range(8):
            message = message.replace(f"$COLOR_{color}",get_color(color))
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
        for color in range(8):
            message = message.replace(f"$COLOR_{color}","")
    return message

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color = True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

def get_color(color):
    return COLOR_SEQ % (30 + color)


def get_logger(nombre=None,rebuild=False) -> logging.Logger:
    '''
    Devuelve un objeto logger por un nombre, en caso de que no exista lo crea
    '''

    nombre = nombre if nombre is not None else _NOMBRE_LOG_PREDEFINIDO

    if not rebuild and nombre in _loggers:
        return _loggers[nombre]

    if nombre in _loggers:
        for h in list(_loggers[nombre].handlers):
            _loggers[nombre].removeHandler(h)
            
    logger = logging.getLogger(nombre) if not nombre in _loggers else _loggers[nombre]

    # formatter = logging.Formatter(
    #     '%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s')

    logger.setLevel(_NIVEL_LOGS)

    ch = logging.StreamHandler()
    ch.setLevel(_NIVEL_LOGS)

    FORMAT = "$BOLD[·] - %(levelname)-18s$RESET $COLOR_2|$RESET $BOLD%(message)s"
    COLOR_FORMAT = formatter_message(FORMAT, True)
    formatter = ColoredFormatter(COLOR_FORMAT)

    ch.setFormatter(formatter)

    logger.addHandler(ch)

    if _DIRECTORIO_LOGS is not None:
        fh = logging.FileHandler(f"{_DIRECTORIO_LOGS}/{nombre}.log")

        # fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)

        # # add the handlers to the logger
        logger.addHandler(fh)

    _loggers[nombre] = logger

    return logger

