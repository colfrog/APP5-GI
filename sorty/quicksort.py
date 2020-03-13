from sorty import sorty

class quicksort(sorty):
    def sort(self, a, low = 0, high = None):
        if len(a) < 2:
            return a

        if high is None:
            high = len(a) - 1

        if high <= low:
            return a

        index = self.partition(a, low, high)
        self.sort(a, low, index - 1)
        self.sort(a, index + 1, high)

    def partition(self, a, low, high):
        pivot = low
        i = low
        j = high

        while i < j:
            while a[i] <= a[pivot] and i < high:
                i += 1
            while a[j] > a[pivot]:
                j -= 1

            if i < j:
                self.swap(a, i, j)

        self.swap(a, pivot, j)
        return j
