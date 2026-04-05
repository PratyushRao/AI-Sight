def get_position(cx, width, config):
    if cx < width * config.LEFT_RATIO:
        return "left"
    elif cx < width * config.RIGHT_RATIO:
        return "center"
    return "right"


def get_distance(depth_value, config):
    if depth_value < config.NEAR_DEPTH:
        return "near"
    elif depth_value < config.MEDIUM_DEPTH:
        return "medium"
    return "far"