# Come prima euristica implementiamo un algoritmo di euristica greedy

# Calcoliamo il numero di like e dislike per ogni ingrediente e ordiniamo gli ingredienti in base alla differenza.

import numpy as np
from loader import Loader
from solver import calculate_score

paths = [
    'dataset/a_an_example.in.txt',
    'dataset/b_basic.in.txt',
    'dataset/c_coarse.in.txt',
    'dataset/d_difficult.in.txt',
    'dataset/e_elaborate.in.txt',
]
def solve(path, iteration=100):
    loader = Loader(path)

    sorted_ingredients = [(ingr, like_dislike[0] - like_dislike[1]) for ingr, like_dislike in loader.ingredients_like_dislike_number.items()]
    sorted_ingredients = sorted(sorted_ingredients, key=lambda x: x[1], reverse=True)

    # Aggiungiamo alla soluzione gli ingredienti "Gratis" cioe' gli ingredienti che non hanno dislike
    base_solution = set()
    for ingr in loader.ingredients_like_dislike_number.items():
        if ingr[1][1] == 0:
            base_solution.add(ingr[0])
    
    # Calcolo randomicamente il threshold tra 1 e max(like_num - dislike-num)
    max_threshold = max(sorted_ingredients, key=lambda x: x[1])[1]
    min_threshold = min(sorted_ingredients, key=lambda x: x[1])[1]
    best_sol = (0, [])
    
    for it in range(iteration):
        threshold = np.random.randint(min_threshold, max_threshold)
        solution = base_solution.copy()
        # Aggiungo gli ingredienti con una soglia
        for ingr in sorted_ingredients:
            if ingr[1] >= threshold:
                solution.add(ingr[0])
        score = calculate_score(solution, loader.clients_list)
        if score >= best_sol[0]:
            best_sol = (score, list(solution.copy()))
                
    print(f"{best_sol}")
    
if __name__ == "__main__":
    for path in paths:
        solve(path, 100)