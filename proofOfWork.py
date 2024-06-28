from hashlib import sha256

x = 5
y = 0  # We don't know what y should be yet...

while True:
    hash_result = sha256(f'{x*y}'.encode()).hexdigest()
    if hash_result[-1] == "0":
        break
    y += 1

print(f'The solution is y = {y}')

#Answer should be 21