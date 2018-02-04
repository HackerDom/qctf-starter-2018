
#include <stdio.h>
#include <string.h>

static char encryptedFlag[] = { 0xd6, 0xc4, 0xd3, 0xc1, 0xfc, 0xf3, 0xe2, 0xf4, 0xf3, 0xfa };

void check() {
    char key = 0x87;

    puts("Enter your flag:");
    char input[sizeof(encryptedFlag)+3];
    fgets(input, sizeof(input), stdin);

    int result = 1;

    if (strlen(input) != sizeof(encryptedFlag) + 1){
        result = 0;
    }

    for (int i = 0; i < sizeof(encryptedFlag); i++) {
        if ((encryptedFlag[i] ^ key) != input[i]){
            result = 0;
        }
    }

    if (result) {
        puts("You are right!");
    } else {
        puts("You are wrong");
    }
}
