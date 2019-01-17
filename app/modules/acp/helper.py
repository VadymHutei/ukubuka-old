import re

def validMenuName(name):
    return name == '' or re.fullmatch(r'\w{1,32}', name)

def validMenuParent(parent):
    return bool(re.fullmatch(r'\d{1,4}', parent))

def validMenuItemName(name):
    return name == '' or re.fullmatch(r'\w{1,64}', name)

def validMenuItemLink(link):
    return bool(re.fullmatch(r'[\w:./]{1,128}', link))