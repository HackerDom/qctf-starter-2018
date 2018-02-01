import sys
from string import Template
from subprocess import run

SOURCE = """
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

    int result = $CONDITION;

    putchar('\\n');

    if (result){
        puts("Ok!");
    } else {
        puts("Fail!");
    }
    return 0;
}
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: generator.py <flag> <task_filename>")
        return

    if not sys.platform.startswith('linux'):
        print("Task should be compiled under Linux")
        return

    flag = sys.argv[1]
    task_filename = sys.argv[2]

    condition = " && ".join("getche() == '{}'".format(c) for c in flag)

    with open("main.c", "w") as f:
        f.write(Template(SOURCE).substitute(CONDITION=condition))

    # gcc-multilib required on x64 systems
    run("gcc main.c -m32 -fno-pic -o " + task_filename, shell=True)

if __name__ == '__main__':
    main()
