from os import environ as envs
import logging
from termcolor import colored
from functools import partial
from contextlib import suppress

import cfg_it

@cfg_it.props
class config:
    log_level: str = "INFO"
    #  = envs.get("LOG_LEVEL", "INFO").upper()

class logger(logging.LoggerAdapter):
    def __init__(self, name):
        logger = logging.getLogger(name)
        super().__init__(logger, {})
        self.nicify = not logger.hasHandlers()
        if self.nicify:
            handler = logging.StreamHandler()
            handler.setFormatter(Formatter())
            logger.addHandler(handler)
            logger.setLevel(config.log_level.upper())

    def process(self, msg, kwargs):
        with suppress(KeyError):
            extra = kwargs['extra']
            if self.nicify:
                kwargs['extra'] = {'extra': extra}
            else:
                kwargs['extra'] = {'_{}'.format(k):v for k, v in extra.items()}
        return msg, kwargs


class Formatter(logging.Formatter):

    def format(self, record):
        return '\n'.join(self.nice_format(record))

    def nice_format(self, record):
        '''Format logs nicely'''
        _white = partial(colored, color='white')
        _bold  = partial(colored, attrs=['bold'])

        level_colors = {
            logging.DEBUG   : ('D', 'blue'),
            logging.INFO    : ('I', 'green'),
            logging.WARNING : ('W', 'yellow'),
            logging.ERROR   : ('E', 'red'),
            logging.CRITICAL: ('C', 'red'),
        }

        def ident_line(indent, text):
                return '{indent}{text}'.format(
                    indent = indent * 4 * ' ',
                    text   = text)

        levelname, levelcolor = level_colors[record.levelno]
        message = '[{level}] {message}'.format(level  =levelname,
                                               message=record.getMessage())
        yield ident_line(indent=0, text=colored(message, levelcolor))

        if record.levelno < logging.INFO:
            called_from = '{name} {path}:{line}'.format(name=_bold(record.module),
                                                        path=record.pathname,
                                                        line=record.lineno)
            yield ident_line(indent=1, text=called_from)

            if hasattr(record, 'extra'):
                extras_label = _bold('extras')
                yield ident_line(indent=1, text=extras_label)
                for key, value in record.extra.items():
                    extras_line = '{key}: {value}'.format(
                                        key  =_white(key),
                                        value=str(value).rstrip())
                    yield ident_line(indent=2, text=extras_line)

        if record.exc_info:
            traceback_label = _bold('Traceback')
            yield ident_line(indent=1, text=traceback_label)
            traceback = self.formatException(record.exc_info)
            for trace_line in traceback.split('\n'):
                yield ident_line(indent=2, text=trace_line)
