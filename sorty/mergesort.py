from sorty import sorty

class mergesort(sorty):
    def sort(self, a):
        if len(a) < 2:
            return a

        mid = len(a)//2
        left = a[:mid]
        right = a[mid:]

        self.sort(left)
        self.sort(right)

        i = j = index = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                a[index] = left[i]
                i += 1
            else:
                a[index] = right[j]
                j += 1
            index += 1

        for elem in left[i:]:
            a[index] = elem

        for elem in right[j:]:
            a[index] = elem
