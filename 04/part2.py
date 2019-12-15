from itertools import groupby

def is_pass(key):
    skey = str(key)
    if len(skey) != 6:
        return(False)
    if list(skey) != sorted(skey):
        return(False)
    nb_iter = [len(list(group)) for key, group in groupby(sorted(skey))]
    return(2 in nb_iter)


def get_solution(min, max):
    return(len(list(filter(is_pass, range(min, max)))))

if __name__ == '__main__':
    print(get_solution(372304,847060))
