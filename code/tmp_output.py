import tempfile


with tempfile.TemporaryFile(mode="w") as tmp:
    tmp.write(["index", "amino", "fold"])
    tmp.seek(0)
    tmp.read()