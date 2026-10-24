
def insertion_sort(arr):
    n=len(arr)
    for i in range (1, n):
        key = arr[i]
        j=i-1

        while (j>=0 and arr[j]>key):
            arr[j+1] = arr[j]
            j-=1
        arr[j+1] = key
    return arr

arr = list(map(int, input("Nhập các số (cách nhau bởi khoảng trắng): ").split()))

insertion_sort(arr)
print("Mảng sau khi sắp xếp:", arr)