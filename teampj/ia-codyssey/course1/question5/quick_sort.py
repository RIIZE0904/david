def quick_sort(arr) -> list:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)

def main():
    script = input("Enter numbers (e.g. 3 9 1 4 2): ")
    try:
        array = list(map(float, script.split()))
    except ValueError:
        print("Invalid input.")
        return

    sorted_array = quick_sort(array)
    print(f"Min: {sorted_array[0]}, Max: {sorted_array[-1]}")

if __name__ == "__main__":
    main()