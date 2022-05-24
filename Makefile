#Adrian Bedford, 22973676
#Oliver Lynch, 22989775

all: rake-c.c 
	gcc -g -Wall -Werror -pedantic -o rake-c rake-c.c

clean: 
	$(RM) rake-c$<