## Reads the input
"""
Input: 
    - The first line contains one integer 1 <= C <= 10^5 - the number of potential clients
    - 2 X C rows containing the clients preferred ingredients in the following format:
        - First line contains integer 1 <= L <= 5, followed by names of ingredients a client likes, delimited by spaces
        - Second line contains integer 1<= D <= 5, followed by names of ingredients a client dislikes, delimited by spaces
"""

import os 

class Loader:
    def __init__(self, path):
        if not os.path.exists(path):
            raise Exception("Path does not exist")
        with open(path) as f:
            self.num_clients = int(f.readline().strip())
            self.clients_vector = []
            for _ in range(self.num_clients):
                like_tmp = f.readline().strip().split(" ")
                L = like_tmp[0]
                liked = like_tmp[1::]
                
                dislike_tmp = f.readline().strip().split(" ")
                D = dislike_tmp[0]
                disliked = dislike_tmp[1::]
                
                self.clients_vector.append({"liked":liked, "disliked":disliked, "L":L, "D":D})
                
    def print(self):
        print(self.clients_vector)
        

if __name__ == "__main__":
    load = Loader("./dataset/a_an_example.in.txt")
    load.print()

