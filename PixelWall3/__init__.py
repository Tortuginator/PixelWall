import argparse, sys, time, traceback, threading, queue
from frame import Frame

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--output', type=str, help='output mode')
    parser.add_argument('--o_port', type=str, help='output port eg. COM5')
    parser.add_argument('--input', type=str, help='input mode')
    parser.add_argument('--i_port', type=int, help='input port eg. 9000')
    parser.add_argument('--height', type=int, help='height of the pixel display')
    parser.add_argument('--width', type=int, help='width of the pixel display')
    args = parser.parse_args()
    print(args)


class PWi:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.output_function = None
        self.input_function = None
        self.frame = Frame(self.width, self.height)
        self.runner = None
        self.frame_counter = 0
        self.frame_counter_timer = None
        self.frame_queue = queue.Queue()

    def run(self, output_function, input_function):
        self.output_function = output_function
        self.input_function = input_function


