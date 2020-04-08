"""This module provides logging and execution details of the entire package."""

import os
import json


class ExecutionData:
    def __init__(self, file_name=None, func_name=None, return_value=None,
                 *args, **kwargs):
        # A MD5 hash of the file name, func name, and line number
        self.selected_finger_print = None
        self.selected_file_name = file_name
        self.selected_func_name = func_name
        self.selected_total_exe_time = None
        self.selected_execution_count = None
        self.selected_created_date = None
        self.selected_updated_date = None
        self.selected_args = args
        self.selected_kwargs = kwargs
        self.selected_return_value = return_value

        # Should be a list of dict.
        self.execution_data_collection = []

        # if self.is_save_data_available():
        #     self.get_saved_data()

    def is_save_data_available(self):
        pass

    def get_saved_data(self):
        pass

    def add_to_collection(self):
        self.execution_data_collection\
            .append(self.__dict__)
