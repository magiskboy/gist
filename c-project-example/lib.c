#include "lib.h"

int fib(int n) {
    // hello world
    if (n < 2) return n;
    return fib(n-1) + fib(n-2);
}
