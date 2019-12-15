def is_pass(key):
    skey = str(key)
    if len(skey) != 6:
        return(False)
    if list(skey) != sorted(skey):
        return(False)
    for i in range(0, len(skey) - 1):
        if skey[i] == skey[i + 1]:
            return(True)
    return(False)


def get_solution(min, max):
    return(len(list(filter(is_pass, range(min, max)))))

if __name__ == '__main__':
    print(get_solution(372304,847060))
