import heapq
import os

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    def __init__(self):
        self.heap = []
        self.codes = {}

    def make_frequency_dict(self, text):
        frequency = {}
        for char in text:
            frequency[char] = frequency.get(char, 0) + 1
        return frequency

    def make_heap(self, frequency):
        for char, freq in frequency.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while len(self.heap) > 1:
            left = heapq.heappop(self.heap)
            right = heapq.heappop(self.heap)

            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not properly padded!")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return bytes(b)

    def compress(self, text):
        frequency = self.make_frequency_dict(text)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        encoded_text = self.get_encoded_text(text)
        padded_encoded_text = self.pad_encoded_text(encoded_text)
        byte_array = self.get_byte_array(padded_encoded_text)

        return byte_array

    def compress_file(self, file_path):
        file_name, file_extension = os.path.splitext(file_path)
        output_path = file_name + "_compressed.bin"

        with open(file_path, 'r') as file, open(output_path, 'wb') as output:
            text = file.read()
            compressed_data = self.compress(text)
            output.write(compressed_data)

        print(f"File compressed successfully: {output_path}")

    def decompress(self, byte_array):
        bit_string = ""
        for byte in byte_array:
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits

        padded_info = bit_string[:8]
        extra_padding = int(padded_info, 2)

        bit_string = bit_string[8:]
        encoded_text = bit_string[:-extra_padding]

        current_code = ""
        decoded_text = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.codes.values():
                char = [k for k, v in self.codes.items() if v == current_code][0]
                decoded_text += char
                current_code = ""

        return decoded_text

    def decompress_file(self, file_path):
        file_name, file_extension = os.path.splitext(file_path)
        output_path = file_name + "_decompressed.txt"

        with open(file_path, 'rb') as file, open(output_path, 'w') as output:
            byte_array = file.read()
            decompressed_text = self.decompress(byte_array)
            output.write(decompressed_text)

        print(f"File decompressed successfully: {output_path}")

if __name__ == "__main__":
    huffman_coding = HuffmanCoding()

    # Example of compressing and decompressing text
    text_to_compress = "hello world"
    compressed_data = huffman_coding.compress(text_to_compress)
    decompressed_text = huffman_coding.decompress(compressed_data)

    print(f"Original text: {text_to_compress}")
    print(f"Compressed data: {compressed_data}")
    print(f"Decompressed text: {decompressed_text}")

    # Example of compressing and decompressing a file
    file_to_compress = "sample.txt"
    huffman_coding.compress_file(file_to_compress)
    huffman_coding.decompress_file("sample_compressed.bin")
