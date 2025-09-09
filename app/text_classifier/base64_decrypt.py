import base64


def decrypt_from_base64(string: str):
    base64_bytes = string.encode("utf-8")
    str_decode = base64.b64decode(base64_bytes)
    decoded = str_decode.decode('utf-8')

    return decoded
