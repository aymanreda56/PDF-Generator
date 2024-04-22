import math
from time import time


string_to_encrypt = "this is a test string"



p = 213477886823765361825629260361
q = 542293515788603525780567369569










def prime_generator():
    """Generate prime numbers indefinitely."""
    primes = []  # List to store generated prime numbers
    num = 2      # Start with the first prime number
    while True:
        is_prime = True
        for prime in primes:
            if num % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
            yield num
        num += 1


def generate_prime_greater_than(number:int):
    prime_gen = prime_generator()
    returned_number = 1
    while returned_number < number:
        returned_number = next(prime_gen)
    return returned_number



# big_number = 100000000
# start_time = time()
# num = generate_prime_greater_than(100000000)
# end_time = time()

# print(f'Prime number > {100000000} is {num},  elapsed time = {end_time-start_time} seconds')