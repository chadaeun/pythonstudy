with (open("input.txt", "r", encoding="utf-8") as fread,
      open("output.txt", "w", encoding="utf-8") as fwrite):
    fwrite.write(fread.read())
