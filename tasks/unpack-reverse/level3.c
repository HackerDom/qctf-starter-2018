
#include <stdio.h>
#include <string.h>

static char encryptedFlag[] = { 0xd6, 0xc4, 0xd3, 0xc1, 0xfc, 0xbf, 0xe6, 0xb4, 0xe1, 0xb4, 0xbe, 0xe1, 0xe5, 0xb7, 0xbe, 0xe3, 0xbf, 0xbf, 0xb4, 0xe3, 0xe4, 0xe6, 0xb4, 0xb5, 0xe5, 0xb6, 0xb2, 0xb7, 0xe3, 0xe6, 0xb1, 0xb4, 0xb5, 0xb7, 0xb5, 0xe4, 0xe1, 0xfa };

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
