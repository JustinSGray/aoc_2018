import string

with open('input.txt') as f:
    data = list(f.read())


def react(data, remove=None):
    i = 1
    N_P = len(data)

    data = list(data)

    if remove is not None:
        remove = remove.lower()

    while i<N_P-1:

        pm1 = data[i-1]
        p = data[i]
        pp1 = data[i+1]

        if remove is not None and p.lower() == remove:
            data.pop(i)
            N_P -= 1
            if i > 0:
                i -= 1
            continue

        pm1_lower = pm1.islower()
        p_lower = p.islower()
        pp1_lower = pp1.islower()

        if pm1_lower != p_lower:
            if pm1.lower() == p.lower():
                data.pop(i-1)
                data.pop(1)
                N_P -= 2
                if i > 0:
                    i -= 1
                continue

        if p_lower != pp1_lower:
            if p.lower() == pp1.lower():
                data.pop(i+1)
                data.pop(i)
                N_P -= 2
                if i > 0:
                    i -= 1
                continue

        i += 1

    return N_P


print('part 1')
size = react(data)
print(size)

print('part 2')
alphabet = string.ascii_lowercase

smallest_letter = None
smallest_len = 1e100

for letter in alphabet:
    size = react(data, letter)

    print(letter, size)

    if size < smallest_len:
        smallest_letter = letter
        smallest_len = size


print('smallest: {}, {}'.format(smallest_letter, smallest_len))


