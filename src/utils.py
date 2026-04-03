def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % (int(rgb['r'] * 255), int(rgb['g'] * 255), int(rgb['b'] * 255))
def rgb_to_rgb_swing(rgb):
    return f"new Color({int(rgb['r'] * 255)}, {int(rgb['g'] * 255)}, {int(rgb['b'] * 255)})"