
#include <stdio.h>
#include <string.h>

static char encryptedFlag[] = { 0xd6, 0xc4, 0xd3, 0xc1, 0xfc, 0xbf, 0xe1, 0xb6, 0xb7, 0xe4, 0xe4, 0xb1, 0xe5, 0xb4, 0xbf, 0xb2, 0xe1, 0xe3, 0xb5, 0xb7, 0xe6, 0xbf, 0xbf, 0xe6, 0xb0, 0xbf, 0xb3, 0xb3, 0xe6, 0xb4, 0xb4, 0xe2, 0xe6, 0xb4, 0xbf, 0xbf, 0xb5, 0xfa };

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
