import re

def parsePrice(data):
    if not isinstance(data, str): return 0
    temp = data.replace(',', '.')
    coma_position = temp.rfind('.')
    foo = (temp,) if coma_position == -1 else (temp[:coma_position], temp[coma_position:])
    bar = [''.join(re.findall(r'[0-9]', part)) for part in foo]
    price = int(bar[0]) * 100 if bar[0] else 0
    if len(bar) > 1: price += int(bar[1][:2])
    return price