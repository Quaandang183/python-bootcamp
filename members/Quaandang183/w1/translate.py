def binary_search(a: list[int], key: int) -> int:
    lo = 0
    hi = len(a) - 1
    
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        
        if a[mid] == key:
            return mid
        if a[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1
            
    return -1

"""
Difference from C++:
In Python, the division operator '/' always returns a float. To perform integer division (like in C++), we must use the floor division operator '//'.
"""