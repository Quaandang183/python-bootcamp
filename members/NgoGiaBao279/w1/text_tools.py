
import re
from collections import Counter


def word_count(s):
    s=s.lower()
    clean_txt =re.sub(r'[^\w\s]','',s)
    words = clean_txt.split()

    return Counter(words)

def top_K(s,k):
    counts = word_count(s)
    word_sort = sorted (counts.items(), key=lambda x: (-x[1],x[0]))

    return word_sort[:k]

sample_text = "Hello world! Hello Python, Python is great. Let's learn python."
    
print("Tần suất các từ:")
print(word_count(sample_text))
    
print("\nTop 2 từ xuất hiện nhiều nhất:")
print(top_K(sample_text, 2))


