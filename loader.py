## Reads the input
"""
Input: 
    - The first line contains one integer 1 <= C <= 10^5 - the number of potential clients
    - 2 X C rows containing the clients preferred ingredients_like_dislike_number in the following format:
        - First line contains integer 1 <= L <= 5, followed by names of ingredients_like_dislike_number a client likes, delimited by spaces
        - Second line contains integer 1<= D <= 5, followed by names of ingredients_like_dislike_number a client dislikes, delimited by spaces
"""

import os
import numpy as np
from collections import defaultdict

def to_index(v, num_elem):
    tmp = np.zeros(num_elem, dtype=np.int32)
    for elem in v:
        tmp[elem] = 1
    return tmp.tolist()

class Loader:
    def __init__(self, path):
        if not os.path.exists(path):
            raise Exception("Path does not exist")
        with open(path) as f:
            self.num_clients = int(f.readline().strip())
            self.clients_list = []
            self.ingredients_like_dislike_number = defaultdict(lambda: [0,0])
            self.inverted_index = defaultdict(lambda: [[], []])
            for c in range(self.num_clients):
                like_tmp = f.readline().strip().split(" ")
                L = int(like_tmp[0])
                liked = like_tmp[1::]
                for ing in liked:
                    self.ingredients_like_dislike_number[ing][0] +=1
                    self.inverted_index[ing][0].append(c)
                
                dislike_tmp = f.readline().strip().split(" ")
                D = int(dislike_tmp[0])
                disliked = dislike_tmp[1::]
                for ing in disliked:
                    self.ingredients_like_dislike_number[ing][1] +=1
                    self.inverted_index[ing][1].append(c)
                
                self.clients_list.append({"liked":liked, "disliked":disliked, "L":L, "D":D})
        self.num_ingredienti = len(self.ingredients_like_dislike_number.keys())
        self.ingredient_index = {x:idx for idx,x in enumerate(self.ingredients_like_dislike_number.keys())}


    def sparse_rappresentation(self):
        sparse_liked_client_list = [{"liked":[self.ingredient_index[ing] for ing in client["liked"]], "disliked":[self.ingredient_index[ing] for ing in client["disliked"]]} for client in self.clients_list]
        return sparse_liked_client_list

    def binary_rappresentation(self):
        binary = [{"liked":to_index([self.ingredient_index[ing] for ing in client["liked"]], self.num_ingredienti), "disliked":to_index([self.ingredient_index[ing] for ing in client["disliked"]], self.num_ingredienti)} for client in self.clients_list]
        return binary
                
    def print(self, verbose=False):
        print(f"num_ingredienti: {self.num_ingredienti}")
        print(f"num_clients: {self.num_clients}")
        print(self.ingredients_like_dislike_number)
        print(self.inverted_index)
        if verbose: 
            print(self.clients_list)
        

if __name__ == "__main__":
    load = Loader("./dataset/a_an_example.in.txt")
    load.print(verbose=True)

    print(load.ingredient_index)
    print(load.sparse_rappresentation())
