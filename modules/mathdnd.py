def get_modifier(characteristic):
    modifiers = {
        1: -5,
        range(2, 4): -4,
        range(4, 6): -3,
        range(6, 8): -2,
        range(8, 10): -1,
        range(10, 12): 0,
        range(12, 14): 1,
        range(14, 16): 2,
        range(16, 18): 3,
        range(18, 20): 4,
        range(20, 22): 5,
        range(22, 24): 6,
        range(24, 26): 7,
        range(26, 28): 8,
        range(28, 30): 9,
        30: 10,
    }

    for key in modifiers.keys():
        if isinstance(key, int) and characteristic == key:
            return modifiers[key]
        elif isinstance(key, range) and characteristic in key:
            return modifiers[key]

    return None