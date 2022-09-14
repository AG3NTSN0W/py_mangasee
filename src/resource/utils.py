def to_json(object):
    return list(map(lambda o: o.to_json(), object))