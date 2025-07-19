class TTYDTxtParser:
    def __init__(self, filepath):
        self.__filepath = filepath
        self.content = None

    def __read_chunk(self, chunk_size=4096):
        with open(self.__filepath, "rb") as f:
            buffer = b""
            while True:
                data = f.read(chunk_size)
                if not data:
                    if buffer:
                        yield buffer
                    break
                buffer += data
                while b'\0' in buffer:
                    chunk, buffer = buffer.split(b'\0', 1)
                    yield chunk

    def load(self):
        self.content = {}

        state = 'key'
        key = None

        for chunk in self.__read_chunk():
            if state == 'key':
                key = chunk.decode('latin1')
                state = 'value'
            else:
                self.content[key] = chunk.decode('latin1')
                state = 'key'

    def search(self, search):
        matches = []

        for key, value in self.content.items():
            if search in key or search in value:
                matches.append((key, value))

        return matches

    def set(self, key, value):
        self.content[key] = value

    def save(self):
        with open(self.__filepath, "wb") as f:
            for key, value in self.content.items():
                f.write(key.encode('latin1'))
                f.write(bytes([0]))
                f.write(value.encode('latin1'))
                f.write(bytes([0]))
            f.write(bytes([0]))
