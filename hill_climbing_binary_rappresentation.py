import numpy as np

from solver import calculate_score_binary, binary_union, binary_disjunction, check_binary_client
import copy
from loader import Loader
# L'idea di questa soluzione e' utilizzare un algoritmo euristico migliorativo
# La MOSSA per questo algoritmo e' la seguente
#     1) scegli cliente casuale a cui non piace la pizza corrente
#     2) Aggiungi ingredienti che piacciono e rimuovo gli ingredienti che non gli piacciono
#     3) se lo score eguaglia o migliora la soluzione migliore aggiorno gli ingredienti altrimenti ripeto la mossa casuale

def solve(path, iteration=1_000_000, verbose=False, checkpoint=None, max_no_improvement=10_000):
    loader = Loader(path)
    best_sol = [0, np.zeros(loader.num_ingredienti, dtype=np.int8).tolist()]
    
    # good_clients = []
    bad_clients = loader.sparse_rappresentation()
    no_improvement = 0
    
    for it in range(iteration):
        if len(bad_clients) == 0:
            break
        unsatisfied_client = np.random.choice(bad_clients)
        temp_sol = copy.deepcopy(best_sol)
        temp_sol[1] = binary_union(temp_sol[1], unsatisfied_client['liked'])
        temp_sol[1] = binary_disjunction(temp_sol[1], unsatisfied_client['disliked'])
        temp_sol[0], tmp_good, tmp_bad = calculate_score_binary(temp_sol[1], loader.sparse_rappresentation(), return_good_and_bad=True)
        if temp_sol[0] >= best_sol[0]:
            if temp_sol[0] > best_sol[0]:
                no_improvement = 0
            else:
                no_improvement += 1
            best_sol = temp_sol
            # good_clients = tmp_good
            bad_clients = tmp_bad
        else:
            no_improvement += 1
        if no_improvement >= max_no_improvement:
            print("max no improvement")
            break
        if verbose:
            print(f"iteration {it}: {best_sol[0]}, no_improvement: {no_improvement}")
        if checkpoint:
            with open(checkpoint, 'w') as f:
                f.write(f"{best_sol[0]} {best_sol[1]}")
            
    return it, best_sol
            
if __name__ == "__main__":
    paths = [
        # ('dataset/a_an_example.in.txt', 'hill_climbing_sol/a.binary.out'),
        # ('dataset/b_basic.in.txt', 'hill_climbing_sol/b.binary.out'),
        # ('dataset/c_coarse.in.txt', 'hill_climbing_sol/c.binary.out'),
        # ('dataset/d_difficult.in.txt', 'hill_climbing_sol/d.binary.out'),
        ('dataset/e_elaborate.in.txt', 'hill_climbing_sol/e.binary.out'),
    ]
    for path,out in paths:
        it, res = solve(path, verbose=True, checkpoint=out)
        with open(out, 'w') as f:
            f.write(f'str(it) str(res)')