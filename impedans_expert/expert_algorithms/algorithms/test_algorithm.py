import sys
import json
import numpy

numbers = json.loads(sys.argv[1])
results = []
for num_list in numbers:
    number = 0
    for num in num_list:
        number = number + num
    results.append(number)
print(results)
