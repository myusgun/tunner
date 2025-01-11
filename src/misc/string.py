# -*- coding: utf-8 -*-


def colordiff(old, new):
    from .colored import green, red, white
    import difflib

    result = ""
    codes = difflib.SequenceMatcher(a=old, b=new).get_opcodes()
    for code in codes:
        if code[0] == "equal":
            result += white(old[code[1]:code[2]])
        elif code[0] == "delete":
            result += red(old[code[1]:code[2]])
        elif code[0] == "insert":
            result += green(new[code[3]:code[4]])
        elif code[0] == "replace":
            result += (red(old[code[1]:code[2]]) + green(new[code[3]:code[4]]))
    return result


def jsonify(data, pretty=True):
    import json
    dic = json.loads(data) if isinstance(data, bytes) else data
    return json.dumps(dic, indent=2 if pretty else None)
