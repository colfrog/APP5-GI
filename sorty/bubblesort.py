from sorty import sorty

class bubblesort(sorty):
    def sort(self, a):
        for i in range(len(a)):
            for j in range(len(a) - i - 1):
                if a[j] > a[j + 1]:
                    self.swap(a, j, j + 1)
