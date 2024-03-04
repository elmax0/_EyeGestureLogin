def get_arrow(i, j):
    return arrow_dict[arrow_directions[i][j]]


arrow_directions = {
    1: {
        2: 'r',
        4: 'd',
        5: 'dl'
    },
    2: {
        1: 'l',
        3: 'r',
        4: 'dl',
        5: 'd',
        6: 'dr'
    },
    3: {
        2: 'l',
        5: 'dl',
        6: 'd'
    },
    4: {
        1: 'u',
        2: 'ur',
        5: 'r',
        7: 'd',
        8: 'dr'
    },
    5: {
        1: 'ul',
        2: 'u',
        3: 'ur',
        4: 'l',
        6: 'r',
        7: 'dl',
        8: 'd',
        9: 'dr'
    },
    6: {
        2: 'ul',
        3: 'u',
        5: 'l',
        8: 'dl',
        9: 'd'
    },
    7: {
        4: 'u',
        5: 'ur',
        8: 'r'
    },
    8: {
        4: 'ul',
        5: 'u',
        6: 'ur',
        7: 'l',
        9: 'r'
    },
    9: {
        5: 'ul',
        6: 'u',
        8: 'l'
    }
}

arrow_dict = {
    'u': 'up_arrow.png',
    'ul': 'ul_arrow.png',
    'ur': 'ur_arrow.png',
    'r': 'right_arrow.png',
    'd': 'down_arrow.png',
    'dl': 'dl_arrow.png',
    'dr': 'dr_arrow.png',
    'l': 'left_arrow.png'
}
