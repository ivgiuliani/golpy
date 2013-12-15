import re

RE_EXTR_SEQUENCE = re.compile(r'((\d+(b|o)?)|(b|o))', re.IGNORECASE)
RE_EXTR_NUMBER = re.compile(r'\d+')


def __extr_number(string):
    return string


def rle_loader(f):
    """
    Partial implementation of a RLE loader.
    @return: a set of pairs (x, y) suitable for our GoL simulator.
    """
    count = 0
    fulltext = []
    for line in f:
        if line.startswith("#"):
            continue
        count += 1
        if count == 1:
            # ignore the header
            continue
        fulltext.append(line)
    fulltext = "".join(fulltext).replace(" ", "").lower()

    pairs = set()
    y = 0
    for line in fulltext.split("$"):
        x = 0
        items = [item[0] for item in RE_EXTR_SEQUENCE.findall(line)]

        for item in items:
            try:
                number = RE_EXTR_NUMBER.match(item).group(0)
                ch = item[len(number):]
                number = int(number)
            except AttributeError:
                number = 1
                ch = item

            for n in range(number):
                if ch == 'o':
                    pairs.add((x, y))
                x += 1

        y += 1
    return pairs