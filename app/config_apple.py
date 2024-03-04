participant = 'training_test'
training = True
modality = 'Touch'

config = {

    'participant': participant,
    'set_size': 15,
    'training': training,
    'modality': modality,
    'scenario': 'test2',

    # 'WIDTH': 3840,
    # 'HEIGHT': 2160,
    'AOI_RADIUS': 20,

    'POSITIONS': [[.166, .833], [0.5, 0.833], [.833, .833],
                  [.166, .5], [0.5, 0.5], [.833, .5],
                  [.166, .166], [0.5, 0.166], [.833, .166]],
    'TOUCH_POSITIONS': [[.362, .734], [0.5, 0.734], [.637, .734],
                        [.362, .5], [0.5, 0.5], [.637, .5],
                        [.362, .265], [0.5, 0.265], [.637, .265]],

    'WIDTH': 1920,
    'HEIGHT': 1080,

    'root': '/Users/elmaxo/Desktop/Projects/EyeGestureLogin/records',
    'acc_precision_root': '/Users/elmaxo/Desktop/Projects/EyeGestureLogin/acc_precision_records',
    'video_root': '/Users/elmaxo/Desktop/Projects/EyeGestureLogin/video_records',
    # 'root': '/Users/max/Desktop/Bachelor/EyeGestureLogin/records',
    'avatar': '/Users/elmaxo/Desktop/Projects/EyeGestureLogin/resources/avatar.png',
    # 'avatar': '/Users/max/Desktop/Bachelor/EyeGestureLogin/resources/avatar.png',

    'debug': True,
    'draw': False,

    'ARROW_PATH': '/Users/elmaxo/Desktop/Projects/EyeGestureLogin/resources/arrows_2.0',
    'ARROW_PATH2': '/Users/elmaxo/Desktop/Projects/EyeGestureLogin/resources/arrows',
    'ARROW_PATH3': '/Users/elmaxo/Desktop/Projects/EyeGestureLogin/resources/arrows_small',
    'ARROW_PATH4': '/Users/elmaxo/Desktop/Projects/EyeGestureLogin/resources/arrows_small_2',
    'GREETING_ARROW_PATH': '/Users/elmaxo/Desktop/Projects/EyeGestureLogin/app/resources/circle-arrow-icon2.png',

    # SCREEN OPTIONS:
    'PASSWORD_SHOW_TIME': 4,
    'GREETING_TIME': 2,
    'INTRO_TIME': .2,
    'AVATAR_SIZE': 50,

    # screen sizing-options
    'WIDTH_PERCENTAGE': .549,
    'HEIGHT_PERCENTAGE': .965,

    # FIXATIONS/SACCADE OPTIONS:

    'duration_threshold': 100,
    'dispersion_threshold': 100,

    # Offset/greeting options
    'eyes_recognition_duration': .300,
    'greetings_duration': 3.000,
    'offset_calculation_duration': 2.00,
    'offset_trigger_radius': .2,
    'time_limit': 10.000,

    'offset_timespan': 2000,
    # 'offset_collection_start_time': 800,
    # 'offset_collection_end_time': 1800,
    'offset_collection_start_time': 500,
    'offset_collection_end_time': 1200,

    # PASSWORD OPTIONS:
    'strict_password': False,
    'PASSWORD_LIST': [[5, 3, 2, 6],
                      [4, 1, 2, 6],
                      [2, 1, 5, 7],
                      [5, 6, 3, 2],
                      [5, 2, 4, 7],
                      [4, 1, 5, 6],
                      [8, 7, 5, 3],
                      [6, 5, 3, 2],
                      [9, 8, 7, 4],
                      [8, 5, 2, 4],
                      [2, 5, 8, 4],
                      [9, 5, 8, 6],
                      [8, 4, 2, 1],
                      [4, 2, 5, 7],
                      [6, 8, 5, 2]],

    'TRAININGS_PASSWORD_LIST': [[2, 6, 3, 5],
                                [2, 4, 7, 8],
                                [1, 4, 5, 7],
                                [3, 5, 9, 8],
                                [5, 3, 2, 1]]

}

if training:
    config['PASSWORD_LIST'] = config['TRAININGS_PASSWORD_LIST']
    config['set_size'] = 3

"""
    SCREENS:

# 1920 × 1200 -> Home screen
# 2560 x 1600 -> HIWI-screen
# 2560 × 1440 -> Omair/Michael-buero 
# 3840 × 2160 -> BenQ

HOME LG:
    'WIDTH':    2560,
    'HEIGHT':   1440,

HOME LG Scaled?:
    'WIDTH':    1920,
    'HEIGHT':   1080,

BENQ:
    'WIDTH':    3840,
    'HEIGHT':   2160,
"""
