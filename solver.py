from loader import Loader
import numpy as np
from itertools import combinations

def solve(path:str):
    loader = Loader(path)
    solution = set()
    # Add free ingredients
    for ingr in loader.ingredients_like_dislike_number.items():
        if ingr[1][1] == 0:
            solution.add(ingr[0])
    score = len(solution)
    # Check every ingredients
    ingredients = loader.ingredient_index.keys()
    best_score = ('',0)
    for i in range(len(ingredients) + 1):
        for subset in combinations(ingredients, i):
            score = calculate_score(subset, loader.clients_list)
            if best_score[1] < score:
                best_score = (subset, score)
    return best_score
            
def calculate_score(ingredients, clients, return_good_and_bad=False):
    score = 0
    good_clients = []
    bad_clients = []
    for client in clients:
        flag = True
        if not np.all(np.isin(client['liked'], ingredients)):
            flag = False
        if np.any(np.isin(client['disliked'], ingredients)):
            flag = False
        if flag:
            score += 1
            good_clients.append(client)
        else:
            bad_clients.append(client)
            
    if return_good_and_bad:
        return (score, good_clients, bad_clients)
    return score
        
def calculate_score_binary(ingredients, clients, return_good_and_bad=False):
    score = 0
    good_clients = []
    bad_clients = []
    for client in clients:
        if check_binary_client(ingredients, client):
            score += 1
            good_clients.append(client)
        else:
            bad_clients.append(client)
    if return_good_and_bad:
        return (score, good_clients, bad_clients)
    return score


def binary_union(ingredients, to_add):
    for pos in to_add:
        ingredients[pos] = 1
    return ingredients

def binary_disjunction(ingredients, to_remove):
    for pos in to_remove:
        ingredients[pos] = 0
    return ingredients

def check_binary_client(ingredients, client):
    for elem in client['liked']:
        if ingredients[elem] == 0:
            return False
    for elem in client['disliked']:
        if ingredients[elem] == 1:
            return False
    return True

if __name__ == "__main__":
    paths_solution = [
        'optimal_solution/a.out',
        'optimal_solution/b.out',
        'optimal_solution/c.out',
        'optimal_solution/d.out',
        'optimal_solution/e.out',
    ]
    paths = [
        'dataset/a_an_example.in.txt',
        'dataset/b_basic.in.txt',
        'dataset/c_coarse.in.txt',
        'dataset/d_difficult.in.txt',
        'dataset/e_elaborate.in.txt',
    ]
    for sol, prob in zip(paths_solution, paths):
        loader = Loader(prob)
        with open(sol, 'r') as f:
            solution = f.readline().strip().split(' ')
            ingr = solution[1::]
            if len(ingr) != int(solution[0]):
                raise Exception("errore lettura soluzione")
            score = calculate_score(ingr, loader.clients_list)
            print(f"{prob} : {score}")
    