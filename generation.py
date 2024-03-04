from random import randint

PASSWORD_LIST = [[5, 3, 2, 6],
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
                 [6, 8, 5, 2]]


def generate_passwort_set(size=15):
    passwords = []
    for i in range(size):
        new_pw = generate_password()
        while new_pw in passwords:
            new_pw = generate_password()
        passwords.append(new_pw)
    for pw in passwords:
        print(pw)
        pass


def generate_password(size=4):
    # TODO:
    password = []
    start = randint(1, 9)
    password.append(start)
    for i in range(size - 1):
        next_val = pick_next_digit(password)
        password.append(next_val)
    return password


def pick_next_digit(current):
    targets = reachable[current[-1]]
    next_val = targets[randint(0, len(targets) - 1)]
    while current.__contains__(next_val):
        # print(f"{next_val} : {current} - {current.__contains__(next_val)}")
        next_val = targets[randint(0, len(targets) - 1)]
    return next_val


reachable = {
    1: [2, 4, 5],
    2: [1, 3, 4, 5, 6],
    3: [2, 5, 6],
    4: [1, 2, 5, 7, 8],
    5: [1, 2, 3, 4, 6, 7, 8, 9],
    6: [2, 3, 5, 8, 9],
    7: [4, 5, 8],
    8: [4, 5, 6, 7, 9],
    9: [5, 6, 8]
}

if __name__ == '__main__':
    generate_passwort_set()
