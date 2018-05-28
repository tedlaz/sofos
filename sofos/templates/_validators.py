
def validate_afm(value):
    result = len(value) == 9
    if result:
        return result, 'value %s can be AFM' % value
    return False, 'value %s is not an afm' % value
