import random


def pad_list(*,topad,origin,padelement):
    lo=len(origin)
    lt=len(topad) if topad else 0
    if not topad:
        topad=[]
    
    if lt<lo:
        padding=[padelement for i in range(lo-lt)]
        topad=topad+padding
    return topad


    

def get_list_derangment(n,lst=None):
    
    
    if not lst:
        lst=[i for i in range(n)]
    lst=list(lst)
    
    perm = lst.copy()
    random.shuffle(perm)
    
    roll_amount = random.randint(1, len(perm) - 1)
    perm_rolled = perm[roll_amount:] + perm[0:roll_amount]
    map_to = [None] * len(lst)
    for perm_i, perm_rolled_i in zip(perm, perm_rolled):
      map_to[perm_i] = perm_rolled_i
    return [lst[j] for i, j in enumerate(map_to)]



def get_random_list_derangment(n,init=None):
    if not init:
        init=[i for i in range(n)]
    init=list(init)
    random.seed()
    while True:
        v = init
        for j in range(n - 1, -1, -1):
            p = random.randint(0, j)
            if v[p] == j:
                break
            else:
                v[j], v[p] = v[p], v[j]
        else:
            if v[0] != 0:
                return tuple(v)
            
