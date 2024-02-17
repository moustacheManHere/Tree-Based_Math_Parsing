class MergeSort:
    def sort(self, arr, dic=False):
        if len(arr) > 1:
            mid = len(arr) // 2

            left_arr = arr[:mid]
            right_arr = arr[mid:]

            if dic:
                self.sort(left_arr, True)
                self.sort(right_arr, True)
            else:
                self.sort(left_arr)
                self.sort(right_arr)

            if dic:
                self.merge(arr, left_arr, right_arr, True)
            else:
                self.merge(arr, left_arr, right_arr)
        return arr

    def merge(self, arr, left, right, dic=False):
        i = j = k = 0

        if dic:
            while i < len(left) and j < len(right):
                if left[i][1] == right[j][1]:
                    if left[i][0] < right[j][0]:
                        arr[k] = left[i]
                        i += 1
                    else:
                        arr[k] = right[j]
                        j += 1

                elif left[i][1] is None:
                    arr[k] = left[i]
                    i += 1

                elif right[j][1] is None:
                    arr[k] = right[j]
                    j += 1

                elif left[i][1] < right[j][1]:
                    arr[k] = left[i]
                    i += 1

                elif left[i][1] > right[j][1]:
                    arr[k] = right[j]
                    j += 1

                k += 1
        else:
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1