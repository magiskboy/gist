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
