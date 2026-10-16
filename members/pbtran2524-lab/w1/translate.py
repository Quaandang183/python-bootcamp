def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a

if __name__ == "__main__":
    try:
        raw_input = input("Enter two integers a and b (separated by a space): ").strip()
        num_a, num_b = map(int, raw_input.split())
        
        result = gcd(num_a, num_b)
        print(f"The greatest common divisor GCD({num_a}, {num_b}) is: {result}")
    except ValueError:
        print("Error: Please enter two valid integers!")