from itertools import product as P

open("combinations.txt", "w").writelines([''.join(list(i))+'\n' for i in list(P('012', repeat=10))])

