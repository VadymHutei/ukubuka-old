import re

def parsePrice(data):
    if isinstance(data, str):
        temp = data.replace(',', '.')
        coma_position = temp.rfind('.')
        foo = (temp,) if coma_position == -1 else (temp[:coma_position], temp[coma_position:])
        bar = [''.join(re.findall(r'[0-9]', part)) for part in foo]
        price = int(bar[0]) * 100 if bar[0] else 0
        if len(bar) > 1: price += int(bar[1][:2])
    elif isinstance(data, int):
        price = price * 100
    elif isinstance(data, float):
        price = round(price * 100)
    else:
        price = None
    return price

def formatPrice(data):
    if not data: return '0,00 ₴'
    if not isinstance(data, str): data = str(data)
    if not re.fullmatch(r'[0-9]+', data): return '0,00 ₴'
    return '{0},{1} ₴'.format(data[:-2], data[-2:])