
#include <stdio.h>
#include <termios.h>

static struct termios old, new;

/* Initialize new terminal i/o settings */
void initTermios(int echo) 
{
    tcgetattr(0, &old); /* grab old terminal i/o settings */
    new = old; /* make new settings same as old settings */
    new.c_lflag &= ~ICANON; /* disable buffered i/o */
    new.c_lflag &= echo ? ECHO : ~ECHO; /* set echo mode */
    tcsetattr(0, TCSANOW, &new); /* use these new terminal i/o settings now */
}

/* Restore old terminal i/o settings */
void resetTermios(void) 
{
      tcsetattr(0, TCSANOW, &old);
}

/* Read 1 character with echo */
char getche(void) 
{
    char ch;
    initTermios(1);
    ch = getchar();
    resetTermios();
    return ch;
}

int main() {
    puts("Welcome to flag scanner! Enter your flag:");

    int result = getche() == 'Q' && getche() == 'C' && getche() == 'T' && getche() == 'F' && getche() == '{' && getche() == 't' && getche() == 'e' && getche() == 's' && getche() == 't' && getche() == '}';

    putchar('\n');

    if (result){
        puts("Ok!");
    } else {
        puts("Fail!");
    }
    return 0;
}
