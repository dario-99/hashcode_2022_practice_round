import numpy as np

from solver import calculate_score
import copy
from loader import Loader

# L'idea di questa soluzione e' utilizzare un algoritmo euristico migliorativo
# La MOSSA per questo algoritmo e' la seguente
#     1) scegli cliente casuale a cui non piace la pizza corrente
#     2) Aggiungi ingredienti che piacciono e rimuovo gli ingredienti che non gli piacciono
#     3) se lo score eguaglia o migliora la soluzione migliore aggiorno gli ingredienti altrimenti ripeto la mossa casuale

def solve(path, iteration=1_000_000, verbose=False, checkpoint=None):
    loader = Loader(path)
    best_sol = [0, set()]
    
    good_clients = []
    bad_clients = loader.clients_list
    
    no_improvement = 0
    
    for it in range(iteration):
        unsatisfied_client = np.random.choice(bad_clients)
        temp_sol = copy.deepcopy(best_sol)
        for liked in unsatisfied_client['liked']:
            temp_sol[1].add(liked)
        for disliked in unsatisfied_client['disliked']:
            temp_sol[1].discard(disliked)
        temp_sol[0],tmp_good, tmp_bad = calculate_score(list(temp_sol[1]), loader.clients_list, return_good_and_bad=True)
        if temp_sol[0] >= best_sol[0]:
            if temp_sol[0] > best_sol[0]:
                no_improvement = 0
            best_sol = temp_sol
            good_clients = tmp_good
            bad_clients = tmp_bad
        else:
            no_improvement += 1
            if no_improvement >= 100:
                break
        if len(bad_clients) == 0:
            break
        if verbose:
            print(f"iteration {it}: {best_sol[0]}, no_improvement: {no_improvement}")
        if checkpoint:
            with open(checkpoint, 'w') as f:
                f.write(str(best_sol))
            
    return best_sol

if __name__ == "__main__":
    paths = [
        # ('dataset/a_an_example.in.txt', 'hill_climbing_sol/a.out'),
        # ('dataset/b_basic.in.txt', 'hill_climbing_sol/b.out'),
        # ('dataset/c_coarse.in.txt', 'hill_climbing_sol/c.out'),
        # ('dataset/d_difficult.in.txt', 'hill_climbing_sol/d.out'),
        ('dataset/e_elaborate.in.txt', 'hill_climbing_sol/e.out'),
    ]
    for path,out in paths:
        res = solve(path, verbose=True, checkpoint=out)
        with open(out, 'w') as f:
            f.write(str(res))