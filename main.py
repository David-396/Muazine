from pathlib import Path

# file_name = r".\podcasts\download.wav"
# file_path = Path(file_name)
# stats = file_path.stat()
# print(file_path.name)
# print(file_path.suffix)
# print(file_path.absolute())
# print(stats.st_mtime)
# print(stats.st_ctime)
# print(f'{stats.st_size / 1000000} mega_bytes.')


path = Path('podcasts')
files = [item for item in path.iterdir() if item.is_file()]
for file in files:
    print(file)
    print(file.stat().st_size)
