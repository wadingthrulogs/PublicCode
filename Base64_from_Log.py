import base64
# This code looks through a log file for base64 encoded strings and decodes them
# This was a question I bomb during an interview and I wanted to see if I could solve it



def is_base64(s):
    try:
        if isinstance(s, str):
            # Convert string to bytes
            s_bytes = s.encode('ascii')
        else:
            s_bytes = s

        # Try decoding the base64 string
        base64.b64decode(s_bytes, validate=True)
        return True
    except (base64.binascii.Error, ValueError):
        return False

def decode_base64(s):
    if is_base64(s):
        decoded_bytes = base64.b64decode(s)
        try:
            decoded_str = decoded_bytes.decode('utf-8')
            print("Decoded string:", decoded_str)
        except UnicodeDecodeError:
            print("Decoded bytes:", decoded_bytes)
    else:
        print("string is not Base64 encoded string.")

log = "file.log"



with open(log, "r") as f:
    for line in f:
        for word in line.split():
            decode_base64(word)