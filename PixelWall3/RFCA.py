# RelativeFrameCompressionAlgorithm
import numpy as np

class RFCA:
    def __init__(self):
        self.frame = None
        self.latest_encoding = None
        self.frame_counter = -1
        self.recovery_length = 20
        self.recovery_position = 0
        self.layer_pointers = []
        self.layers = None
        self.pixels = None

    def get_byte_code(self):
        init_seq = []
        for i in range(self.layers):
            init_seq.append(self.layer_pointers[i] // 255)
            init_seq.append(self.layer_pointers[i] % 255)
        ret = bytearray(init_seq)
        for i in range(self.layers):
            ret += bytearray(self.latest_encoding[i,:self.layer_pointers[i]].tobytes())
        return ret

    def compute_encoding(self, base_frame, new_frame):
        assert base_frame.shape == new_frame.shape
        result = np.zeros((self.layers, self.pixels), dtype=np.uint8)
        difference = base_frame - new_frame
        in_layer_pointer = 0
        self.layer_pointers = [0]*self.layers
        for layer in range(self.layers):
            jump_counter = 0
            for pixel in range(self.pixels):
                if pixel >= self.recovery_position and pixel < self.recovery_position+self.recovery_length:
                    difference[layer][pixel] = 1

                if difference[layer][pixel] == 0:
                    jump_counter += 1

                elif jump_counter == 0 and difference[layer][pixel] != 0:
                    result[layer][in_layer_pointer] = RFCA._escape_symbol(new_frame[layer][pixel])
                    in_layer_pointer += 1

                elif jump_counter - 2 <= 0 and difference[layer][pixel] != 0:
                    for i in range(0, jump_counter+1):
                        result[layer][in_layer_pointer + i] = RFCA._escape_symbol(
                            new_frame[layer][pixel - jump_counter + i])
                    in_layer_pointer += jump_counter+1
                    jump_counter = 0

                elif jump_counter > 3 and difference[layer][pixel] != 0
                    for r in range(0, jump_counter//255):
                        result[layer][in_layer_pointer] = 1
                        result[layer][in_layer_pointer + 1] = 255
                        in_layer_pointer += 2
                    result[layer][in_layer_pointer] = 1
                    result[layer][in_layer_pointer + 1] = jump_counter % 255
                    in_layer_pointer += 2
                    jump_counter = 0
                    result[layer][in_layer_pointer] = RFCA._escape_symbol(new_frame[layer][pixel])
                    in_layer_pointer += 1
            self.layer_pointers[layer] = in_layer_pointer
        return result

    def push_frame(self, new_frame):
        if self.is_first_push(new_frame) is True:
            return
        self.latest_encoding = self.compute_encoding(self.frame, new_frame)
        self.frame_counter += 1
        self.frame = new_frame

    def is_first_push(self, new_frame):
        if self.frame is None:
            self.layers = new_frame.shape[0]
            self.pixels = new_frame.shape[1]
            self.frame = np.zeros((self.layers, self.pixels), dtype=np.uint8)
            self.latest_encoding = self.compute_encoding(self.frame, new_frame)
            self.frame_counter = 1
            self.frame = new_frame
            return True
        return False

    @staticmethod
    def _escape_symbol(i):
        if i == 1:
            return 2
        if i == 3:
            return 4
        return i
