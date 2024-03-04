from typing import List

import math
import numpy as np

from app.authenticator.gaze.utils import Gaze

"""

Format:

accuracy: {
        mean,
        sd
    {

precision: {
        mean,
        sd
    }
point: {
    x_norm,
    y_norm,
    x,
    y,
    radius_norm,
    radius
}
info: {
    num_gaze_samples,
    num_nan_percentage
}

"""


def calculate_accuracy(x_vals, y_vals, point):
    mean_x = np.mean(x_vals)
    mean_y = np.mean(y_vals)

    x_acc = math.fabs(point[0] - mean_x)
    y_acc = math.fabs(point[1] - (1 - mean_y))

    return {
        'x_acc': x_acc,
        'y_acc': y_acc
    }


def calculate_precision(x_vals, y_vals):
    prec_x = np.std(x_vals)
    prec_y = np.std(y_vals)
    return {
        'x_prec': prec_x,
        'y_prec': prec_y
    }


def extract_gaze_info(gaze_objects):
    nan_values = sum([1 if gaze.has_nan else 0 for gaze in gaze_objects])

    return {
        'num_samples': len(gaze_objects),
        'nan_samples': nan_values
    }


def extract_point_info(point):
    return {
        'pos_x': point[0],
        'pos_y': 1 - point[1]
    }


def calculate_accuracy_and_precision(raw_data, point):
    # get gaze information
    gaze_objects = [Gaze(raw) for raw in raw_data]
    gaze_info = extract_gaze_info(gaze_objects)
    # filter nan-values
    gaze_objects = _filter_nan(gaze_objects)
    x_vals = np.array([gaze.x for gaze in gaze_objects])
    y_vals = np.array([gaze.y for gaze in gaze_objects])
    # calculate data
    precision_result = calculate_precision(x_vals, y_vals)
    accuracy_result = calculate_accuracy(x_vals, y_vals, point)
    point_info = extract_point_info(point)
    return {
        'precision': precision_result,
        'accuracy': accuracy_result,
        'gaze_info': gaze_info,
        'aoi': point_info
    }


def _filter_nan(gaze_objects: List[Gaze]):
    result_list = []
    for gaze_obj in gaze_objects:
        if not gaze_obj.has_nan:
            result_list.append(gaze_obj)
    return result_list
