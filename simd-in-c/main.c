#include <stdio.h>
#include <immintrin.h>

int main() {
    __m256i first = _mm256_set_epi32(10, 20, 30, 40, 50, 60, 70, 80);
    __m256i second = _mm256_set_epi32(5, 5, 5, 5, 5, 5, 5, 5);
    __m256i result = _mm256_add_epi32(first, second);
    int* values = (int*) &result;
    for (int i = 0; i < 8; ++i)  {
        printf("%d\n", values[i]);
    }
    return 0;
}

