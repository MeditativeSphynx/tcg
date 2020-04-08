import os
import json
import time
import inspect
import functools
from loguru import logger
from datetime import datetime

from tcg import tcg_path
from core_data import ExecutionData
# execution_data = ExecutionData()


def track_execution(_func=None, *, i_frame=None, file_name=None):
    def decorator_track_execution(func):
        @functools.wraps(func)
        def time_wrapper(*args, **kwargs):
            if i_frame is not None:
                logger.debug(f'Tracking execution >>> {func.__name__}')
                logger.debug(f'{file_name}:{i_frame.f_lineno}')

            t1 = time.time()
            value = func(*args, **kwargs)
            t2 = time.time()
            # execution_data.execution_time = t2-t1

            logger.debug(f'{func.__name__} >>> time: {t2-t1}')
            logger.debug(f'return value: {value}')
            return value
        return time_wrapper
    if _func is None:
        return decorator_track_execution
    else:
        return decorator_track_execution(_func)
