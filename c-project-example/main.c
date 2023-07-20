#include <stdio.h>
#include "lib.h"

int main() {
    int n;
    scanf("%d", &n);
    int v = fib(n);
    printf("%d\n", v);
    return 0;
}
