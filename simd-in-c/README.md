## Use Single Instruction Multiple Data in C

```c
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
```

```bash
$ gcc -mavx2 main.c 
$ ./a.out
```


Read more API in [Intel References](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html#expand=91,555&ig_expand=119&cats=Arithmetic&avxnewtechs=AVX2)
