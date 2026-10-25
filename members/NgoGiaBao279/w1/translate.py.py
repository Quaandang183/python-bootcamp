"""Insertion sort implementation translated from C++."""


def insertion_sort(arr):
    """Sắp xếp mảng số nguyên theo thứ tự tăng dần bằng thuật toán chèn (Insertion Sort)."""
    n=len(arr)
    for i in range (1, n):
        key = arr[i]
        j=i-1

        while (j>=0 and arr[j]>key):
            arr[j+1] = arr[j]
            j-=1
        arr[j+1] = key
    return arr


if __name__ == "__main__":
    arr = list(map(int, input("Nhập các số (cách nhau bởi khoảng trắng): ").split()))
    insertion_sort(arr)
    print("Mảng sau khi sắp xếp:", arr)