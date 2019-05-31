import string
import random

grocery = 'raw/Clinical_notes.txt'

# splits at ','
print(grocery.rsplit('/'))
lst = grocery.rsplit('/')
print(lst[len(lst)-1])

print(len(grocery))



def randomString(istr):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(len(istr)))



print(randomString('test'))
