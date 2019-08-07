import hashlib
import json
import requests

import sys


def mine_proof(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 4 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    new_proof = 0
    while validate_proof(last_proof, new_proof) is False:
        new_proof += 1

    return new_proof


def validate_proof(last_proof, new_proof):
    """
    Validates the Proof: Does hash(last_proof, proof) contain 6
    leading zeroes?
    """
    guess = f'{last_proof}{new_proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        last_proof = requests.get('http://localhost:5000/last_proof').json()['last_proof']
        print('last_proof', last_proof)

        # look for the next proof
        new_proof = mine_proof(last_proof)

        #POST new_proof to the server
        post_response = requests.post('http://localhost:5000/mine', json = {'proof': new_proof})

        print('post_response:', post_response.status_code)
        print(post_response.json())

        if post_response.status_code == 200:
            continue
        else:
            print(post_response.content)
            break
