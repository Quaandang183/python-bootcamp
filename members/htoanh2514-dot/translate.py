def sieve_of_eratosthenes(n: int) -> list:
  """Tìm các số nguyên tố từ 2 đến n bằng thuật toán sàng Eratosthenes."""
  if n < 2:
    return []

  is_prime = [True] * (n + 1)
  is_prime[0] = is_prime[1] = False

  for p in range(2, int(n**0.5) + 1):
    if is_prime[p]:
      for i in range(p * p, n + 1, p):
        is_prime[i] = False

  return [p for p in range(2, n + 1) if is_prime[p]]