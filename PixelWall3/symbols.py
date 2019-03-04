import numpy as np


def symbol_number(char):
    if char == "1":
        return np.array([[0, 255],
                         [255, 255],
                         [0, 255],
                         [0, 255],
                         [0, 255]], dtype=np.uint8)

    if char == "2":
        return np.array([[255, 255, 255],
                         [0, 0, 255],
                         [0, 255, 255],
                         [255, 0, 0],
                         [255, 255, 255]], dtype=np.uint8)
    if char == "3":
        return np.array([[255, 255, 255],
                         [0, 0, 255],
                         [0, 255, 0],
                         [0, 0, 255],
                         [255, 255, 255]], dtype=np.uint8)
    if char == "4":
        return np.array([[255, 0, 255],
                         [255, 0, 255],
                         [255, 255, 255],
                         [0, 0, 255],
                         [0, 0, 255]], dtype=np.uint8)
    if char == "5":
        return np.array([[255, 255, 255],
                         [255, 0, 0],
                         [255, 255, 0],
                         [0, 0, 255],
                         [255, 255, 0]], dtype=np.uint8)
    if char == "6":
        return np.array([[0, 255, 255],
                         [255, 0, 0],
                         [255, 255, 255],
                         [255, 0, 255],
                         [0, 255, 255]], dtype=np.uint8)

    if char == "7":
        return np.array([[255, 255, 255],
                         [0, 0, 255],
                         [0, 255, 0],
                         [255, 0, 0],
                         [255, 0, 0]], dtype=np.uint8)
    if char == "8":
        return np.array([[255, 255, 255],
                         [255, 0, 255],
                         [255, 255, 255],
                         [255, 0, 255],
                         [255, 255, 255]], dtype=np.uint8)
    if char == "9":
        return np.array([[0, 255, 255],
                         [255, 0, 255],
                         [255, 255, 255],
                         [0, 0, 255],
                         [255, 255, 0]], dtype=np.uint8)
    if char == "0":
        return np.array([[0, 255, 255],
                         [255, 0, 255],
                         [255, 0, 255],
                         [255, 0, 255],
                         [255, 255, 0]], dtype=np.uint8)
    return None