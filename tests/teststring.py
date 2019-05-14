
grocery = 'raw/Clinical_notes.txt'

# splits at ','
print(grocery.rsplit('/'))
lst = grocery.rsplit('/')
print(lst[len(lst)-1])