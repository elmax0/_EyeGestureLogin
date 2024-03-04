import csv
import json
import os
from os import path

import pandas as pd

from app.config import config

JSON_NAME = 'config.json'
EVENT_COLUMNS = ['LOCAL_TIME', 'TIMESTAMP', 'EVENT', 'X', 'Y', 'END_X', 'END_Y', 'Duration', 'Password_entry',
                 'X_OFFSET', 'Y_OFFSET']

TRAINING = config['training']


class StorageHandler:
    def __init__(self, root=config['root'], participant=config['participant'], modality="Gaze"):
        self._root = root
        self._participant = participant
        self._modality = modality
        self._participant_path = path.join(self._root, self._participant)
        self._modality_path = path.join(self._participant_path, self._modality)
        self.setup()

    def setup(self):
        if TRAINING:
            return
        if not path.exists(self._root):
            raise Exception(f"Root-folder at {self._root} does not exist")
        if not path.exists(self._participant_path):
            os.mkdir(self._participant_path)
        if path.exists(self._modality_path):
            raise Exception(f"Modality path: {self._modality_path} does exist -> Won't overwrite")
        os.mkdir(self._modality_path)
        json_destiny = path.join(self._modality_path, JSON_NAME)
        with open(json_destiny, 'w+') as f:
            json.dump(config, f)

    def save(self, events, raw_data=None, scenario=config['scenario'], scenario_attempt=1):
        if TRAINING:
            return
        # create scenario-folder
        scenario_path = path.join(self._modality_path, f"{scenario}_{scenario_attempt}")
        if path.exists(scenario_path):
            raise Exception(f"Scenario path: {scenario_path} does exist -> wont overwrite")
        os.mkdir(scenario_path)
        # write events
        event_path = path.join(scenario_path, 'events.csv')
        with open(event_path, 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(EVENT_COLUMNS)
            writer.writerows(events)

        # write raw data (if exists)
        if raw_data:
            raw_data_path = path.join(scenario_path, 'raw_data.csv')
            df = pd.DataFrame.from_dict(raw_data)
            df.to_csv(raw_data_path, index=False)
