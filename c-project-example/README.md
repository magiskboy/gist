# Example for compiling and linking in C

We have a program:

```c 
#include <stdio.h>
#include "lib.h"

int main() {
    int n;
    scanf("%d", &n);
    int v = fib(n);
    printf("%d\n", v);
    return 0;
}
```

and 

```c 
#ifndef LIB_H
#define LIB_H

int fib(int);

#endif
```

```c 
#include "lib.h"

int fib(int n) {
    // hello world
    if (n < 2) return n;
    return fib(n-1) + fib(n-2);
}
```

Then create a Makefile

```make
CC := gcc

lib.o: lib.c lib.h
	${CC} -c $< -o $@

main.o: main.c
	${CC} -c $< -o $@

main: main.o lib.o
	${CC} $^ -o $@

all: main

clean:
	rm *.o
```


**Note**

- $@: target
- $<: first input
- $^: all of input
