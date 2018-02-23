import sys
from subprocess import run
from pathlib import Path
from string import Template

XOR_KEY = 0x87
OBFUSCATE_SHIFT = 78

MSBUILD_PATH = "%programfiles(x86)%\\MSBuild\\14.0\\Bin\\msbuild.exe"

LEVEL1_SOURCE = """
#include <stdio.h>
#include <windows.h>

unsigned char level2[] = $LEVEL2;

void fail(char* message){
    printf("%s (LastError: %d, errno: %d)", message, (int) GetLastError(), errno);
    exit(1);
}

void deobfuscate(){
    for (int i = 0; i < sizeof(level2); i++){
        level2[i] += $OBFUSCATE_SHIFT;
    }
}

int main() {
    char path[MAX_PATH+1];
    if (!GetTempPath(sizeof(path), path)){
        fail("Cannot get temp directory");
    }

    char filename[MAX_PATH+1];
    if (!GetTempFileName(path, NULL, 0, filename)){
        fail("Cannot get temp filename");
    }

    FILE *f = fopen(filename, "wb");
    if (f == NULL){
        fail("Cannot open temp file");
    }
    deobfuscate();
    fwrite(level2, sizeof(unsigned char), sizeof(level2), f);
    fclose(f);

    system(filename);

    DeleteFile(filename);
    return 0;
}
"""

LEVEL3_SOURCE = """
#include <stdio.h>
#include <string.h>

static char encryptedFlag[] = $ENCRYPTED;

void check() {
    char key = $KEY;

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
"""

def format_array_literal(bytes_):
    return "{{ {} }}".format(", ".join(hex(b) for b in bytes_))

def save_level3_source(path, flag):
    encryptedFlag = bytes(ord(c) ^ XOR_KEY for c in flag)
    Path(path).write_text(
        Template(LEVEL3_SOURCE).substitute(
            ENCRYPTED=format_array_literal(encryptedFlag),
            KEY=hex(XOR_KEY),
            FLAG_LEN=len(flag)))

def obfuscate_level3(binary_path):
    level3_compiled = Path(binary_path).read_bytes()
    level3_obfuscated = bytes(255 - b for b in level3_compiled)
    Path(binary_path).write_bytes(level3_obfuscated)

def substitute_pin(template_path, output_path, pin):
    Path(output_path).write_text(
        Template(Path(template_path).read_text()).substitute(PIN=pin)
    )

def get_obfuscated_level2(binary_path):
    level2_compiled = Path(binary_path).read_bytes()
    return bytes((b - OBFUSCATE_SHIFT + 256) % 256 for b in level2_compiled)

def save_level1_source(path, level2_obfuscated):
    Path(path).write_text(
        Template(LEVEL1_SOURCE).substitute(
            LEVEL2=format_array_literal(level2_obfuscated),
            OBFUSCATE_SHIFT=OBFUSCATE_SHIFT))

def main():
    if len(sys.argv) < 4:
        print("Usage: generator.py <pin> <flag> <task_filename>")
        return

    pin = sys.argv[1]
    flag = sys.argv[2]
    task_filename = sys.argv[3]

    save_level3_source("./level3.c", flag)
    run("gcc ./level3.c -shared -s -std=c99 -m32 -o ./Level2/level3.dll")

    obfuscate_level3("./Level2/level3.dll")
    substitute_pin("./Level2/Program.template.cs", "./Level2/Program.cs", pin)
    run('"{}" ./Level2/Level2.csproj /p:Configuration=Release'.format(MSBUILD_PATH), shell=True)

    save_level1_source("./level1.c", get_obfuscated_level2("./Level2/bin/Release/Level2.exe"))
    run("gcc ./level1.c -std=c99 -m32 -o " + task_filename)

if __name__ == '__main__':
    main()
