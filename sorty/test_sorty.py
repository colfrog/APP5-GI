#!/usr/bin/python3
from quicksort import quicksort
from bubblesort import bubblesort
from mergesort import mergesort

def test_sort(sort, a):
    print('Starting sort')
    print(a)
    sort(a)
    print(a)
    print('')

sorts = [bubblesort(), quicksort(), mergesort()]

a_orig = [65, 23, 14, 87, 1]
b_orig = [65, 23, 14, 87, 54, 1]

for sort in sorts:
    a = list(a_orig)
    b = list(b_orig)
    test_sort(sort.sort, a)
    test_sort(sort.sort, b)
