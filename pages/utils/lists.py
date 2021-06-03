def max_len(x):
    maximum = []
    for item in x:
        if isinstance(item, (list, tuple)):
            for c in item:
                maximum.append(len(c))
        if isinstance(item, (int, float)):
            maximum.append(len(str(item)))
        else:
            maximum.append(len(item))
    return max(maximum)
