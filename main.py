import base64

# hostile
base64_string ="R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2Vl cyxJQ0MsQkRT"
base64_bytes = base64_string.encode("utf-8")

sample_string_bytes = base64.b64decode(base64_bytes)
sample_string = sample_string_bytes.decode('utf-8')

print(f"Decoded string: {sample_string}")

# less hostile
base64_string ="RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ=="
base64_bytes = base64_string.encode("utf-8")

sample_string_bytes = base64.b64decode(base64_bytes)
sample_string = sample_string_bytes.decode('utf-8')

print(f"Decoded string: {sample_string}")