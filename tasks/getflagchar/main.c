
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

    int result = getche() == 'Q' && getche() == 'C' && getche() == 'T' && getche() == 'F' && getche() == '{' && getche() == 'e' && getche() == '5' && getche() == '1' && getche() == 'f' && getche() == '2' && getche() == 'd' && getche() == 'a' && getche() == 'd' && getche() == '8' && getche() == '7' && getche() == '8' && getche() == '7' && getche() == '5' && getche() == 'd' && getche() == '7' && getche() == '6' && getche() == 'f' && getche() == 'b' && getche() == '0' && getche() == '8' && getche() == '1' && getche() == 'f' && getche() == '2' && getche() == 'b' && getche() == '4' && getche() == '6' && getche() == '7' && getche() == '5' && getche() == '3' && getche() == '5' && getche() == 'e' && getche() == 'f' && getche() == '}';

    putchar('\n');

    if (result){
        puts("Ok!");
    } else {
        puts("Fail!");
    }
    return 0;
}
