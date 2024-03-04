import json
import os
from os import path

import pandas as pd

from app.config import config

EVENT_COLUMNS = ['LOCAL_TIME', 'TIMESTAMP', 'EVENT', 'X', 'Y', 'END_X', 'END_Y', 'Duration', 'Password_entry',
                 'X_OFFSET', 'Y_OFFSET']
TRAINING = config['training']


class AccuracyAndPrecisionStorageHandler:

    def __init__(self):
        self.participant = config['participant']
        self.root = config['acc_precision_root']
        self._raw_data_file_name = 'raw_data.csv'

        if TRAINING:
            return
        self._participant_path = path.join(self.root, self.participant)
        if path.exists(self._participant_path):
            print(f'path: {self._participant_path} already exists!')
            self._participant_path += '_duplicate'
        os.mkdir(self._participant_path)

    def save_raw_data(self, raw_data):
        if TRAINING:
            return
        raw_data_file = path.join(self._participant_path, self._raw_data_file_name)
        if raw_data:
            df = pd.DataFrame.from_dict(raw_data)
            df.to_csv(raw_data_file, index=False)

    def save(self, point_id, result_data, raw_data):
        if TRAINING:
            return
        file_prefix = f"Point_{point_id}_"
        raw_data_file = path.join(self._participant_path, f"{file_prefix}raw_data.cvs")

        result_json_file = path.join(self._participant_path, f"{file_prefix}result.json")

        with open(result_json_file, 'w+') as f:
            json.dump(result_data, f)

        if raw_data:
            df = pd.DataFrame.from_dict(raw_data)
            df.to_csv(raw_data_file, index=False)


if __name__ == '__main__':
    acc = AccuracyAndPrecisionStorageHandler()

    pass
