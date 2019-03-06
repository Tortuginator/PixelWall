import argparse, sys, time, traceback, threading, queue
from frame import Frame
from RFCA import RFCA
from output import SimpleSerial

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--output', type=str, help='output mode')
    parser.add_argument('--o_port', type=str, help='output port eg. COM5')
    parser.add_argument('--height', type=int, help='height of the pixel display')
    parser.add_argument('--width', type=int, help='width of the pixel display')
    args = parser.parse_args()
    print(args)


class PWi:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.generation_function = None
        self.frame = Frame(self.width, self.height)
        self.frame_counter = 0
        self.runner = None
        self.frame_queue = queue.Queue()
        self.encoder_context = None
        self.output_module = SimpleSerial()

    def run(self, generation_function):
        self.generation_function = generation_function
        self.start_runner()

    def start_runner(self):
        if self.runner is None:
            self.output_module = RFCA()
            self.runner = threading.Thread(target=PWi.runner, args=(self.encoder_context,
                                                                    self.frame_queue,
                                                                    self.output_module))
            self.runner.start()

        elif not self.runner.is_alive():
            self.runner = None
            self.start_runner()

    def push_frame(self, generated_frame):
        self.frame_queue.put(generated_frame)
        self.frame_counter += 1
        self.start_runner()

    @staticmethod
    def runner(*kargs):
        assert len(kargs) == 3
        assert kargs[0] is not None
        assert kargs[1] is not None
        assert kargs[2] is not None

        encoder_context = kargs[0]
        frame_queue = kargs[1]
        output_module = kargs[2]
        while True:
            item_frame = frame_queue.get()
            if item_frame is None:
                time.sleep(1/float(120))
                continue

            #encoding
            encoder_context.push_frame(item_frame)
            output_module.send_image(encoder_context.get_byte_code())

            #complete
            frame_queue.task_done()
