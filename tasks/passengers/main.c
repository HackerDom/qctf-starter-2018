#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <zconf.h>
#include <fcntl.h>


const int MAX_LEN  = 0xfffff;
const int PASS_LEN = 50;
const int IN_LEN   = 50;
const int AGE_LEN  = 25;

int GLOBAL_COUNT = 0;
int PASS_NUMBER  = 0;


struct passenger {
    int id;
    unsigned char is_frozen;
    unsigned char is_captain;

    unsigned char age;
    unsigned char is_crewman;
    unsigned char token[7];

    unsigned char country[100];
    unsigned char first_name[100];
    unsigned char last_name [100];

    void (*on_unfreeze_ptr)(struct passenger*);
    void (*on_freeze_ptr)(struct passenger*);
    void (*info_ptr)(struct passenger*);
};

struct passenger *ship[50];
struct passenger *applier;


char* concat(char s1[], const char s2[]) {
    int i, j;
    char s3[MAX_LEN];

    if (sizeof(s1) + sizeof(s2) > MAX_LEN)
        return (char *) s1;

    for (i = 0; s1[i] != '\x00'; i++) {
        s3[i] = s1[i];
    }
    for (j = 0; s2[j] != '\x00'; j++, i++) {
        s3[i] = s2[j];
    }
    s3[i] = '\x00';
    char *s = &s3[0];
    return s;
}


void on_unfreeze(struct passenger *pass) {
    printf("\n[+] The passenger is unfrozen!\n");
    printf("============================\n");
    pass_info(pass);
    printf("============================\n");
    printf("\n");
}


void on_freeze(struct passenger *pass) {
    printf("\n[+] The passenger is frozen!\n");
    printf("============================\n");
    pass_info(pass);
    printf("============================\n");
    printf("\n");
}


void info(struct passenger *pass) {
    printf("[*] The passenger's information:\n");
    pass_info(pass);
    printf("\n");
}


void pass_info(struct passenger *pass) {
    char buf[MAX_LEN];
    char buf2[MAX_LEN];
    unsigned char age = pass->age;

    sprintf(buf, "%d", (int) age);

    printf("%s\n", strcpy(buf2, concat("    First name: ", pass->first_name)));
    printf("%s\n", strcpy(buf2, concat("    Last name:  ", pass->last_name)));
    printf("%s\n", strcpy(buf2, concat("    Age:        ", buf)));
}


struct passenger* create_passenger(char *first_name, char *last_name, char *country, long age) {
    struct passenger *passng = malloc(2 * sizeof(struct passenger));

    passng->id         = GLOBAL_COUNT++;
    passng->is_frozen  = 0;
    passng->is_captain = 0;

    passng->on_freeze_ptr   = on_freeze;
    passng->on_unfreeze_ptr = on_unfreeze;
    passng->info_ptr          = info;

    strcpy(passng->first_name, first_name);
    strcpy(passng->last_name,  last_name);
    strcpy(passng->country,    country);

    memset(passng->token, 0, 7);
    passng->is_crewman = 0;

    long *_age = (long *) &passng->age;
    *_age = age;

    return passng;
}


struct passenger set_captain(struct passenger pass) {
    pass.is_captain = 1;
    return pass;
}


struct passenger* raise2crewman(struct passenger *pass, char *token) {
    int len = strlen(token);

    if (len >= 7)
        token[6] = '\x00';

    pass->is_crewman = 1;
    strcpy(pass->token, token);
    return pass;
}


int add_passenger(struct passenger *pass) {
    if (PASS_LEN <= PASS_NUMBER) {
        return 1;
    }
    ship[PASS_NUMBER] = pass;
    PASS_NUMBER++;
    return 0;
}


void init_ship() {
    add_passenger(raise2crewman(create_passenger("John",   "Smith",   "ENG", 39), "rim96z"));
    add_passenger(raise2crewman(create_passenger("Maria",  "Garcia",  "ENG", 24), "tjqb2v"));
    add_passenger(raise2crewman(create_passenger("Konata", "Izumi",   "JAP", 18), "99iap3"));
    add_passenger(raise2crewman(create_passenger("Dmitry", "Sokolov", "RUS", 32), "nv7btm"));
    add_passenger(raise2crewman(create_passenger("Lucas",  "Aris",    "FRA", 23), "th4a80"));
}


//void __input_string(char *str, int size) {
//    char c;
//    char arr[MAX_LEN];
//    int cur_size = 0;
//
//    if (size >= MAX_LEN)
//        return;
//
//    while (c = getchar()) {
//        arr[cur_size++] = c;
//        if (cur_size >= MAX_LEN)
//            break;
//        if (c == '\n')
//            break;
//    }
//    arr[(cur_size < size) ? (cur_size-1) : (size-1)] = '\x00';
//    strcpy(str, arr);
//    return;
//}


void input_string(char *str, int size) {
    fgets(str, size, stdin);
    str[strlen(str) - 1] = 0;
}


int input_choice() {
    int choice;
    char buf[100];

    input_string(buf, sizeof(buf));
    int sscanf_res = sscanf(buf, "%d", &choice);

    if ((sscanf_res == 0) | (sscanf_res == EOF)) {
        choice = -1;
    }
    return choice;
}


long parse_long(char *s) {
    long l = 0;
    int i = 0;
    for (int i = 0; i < strlen(s); i++) {
        int b = (*(s + i) - '0');
        if (b >= 0 && b < 10)
            l = l * 10 + b;
        else
            return -1;
    }
    return l;
}


void header() {
    printf("============ WELCOME TO OUR SHiP ============\n");
}


int input_age(long *rage) {
    char age[MAX_LEN];

    input_string(age, AGE_LEN);
    *rage = parse_long(age);

    if (*rage <= 18) {
        printf("[-] Invalid age, try again!\n\n");
        return 0;
    } else return 1;
}


struct passenger* apply() {
    long rage = 0;
    char firstname[MAX_LEN], lastname[MAX_LEN], country[MAX_LEN];

    printf("\nThank you for applying!\nPlease, full the fields below:\n");
    printf("============================\n");
    printf("     First name [50]: ");
    input_string(firstname, IN_LEN);

    printf("     Last name [50]: ");
    input_string(lastname, IN_LEN);

    printf("     Country [50]: ");
    input_string(country, IN_LEN);

    printf("     Age: ");
    if (!input_age(&rage)) return NULL;

    struct passenger *pass = create_passenger(firstname, lastname, country, rage);
    add_passenger(pass);

    printf("[+] Done!\n");
    return pass;
}


void show_list() {
    print_file_content("./applicants");
}


int crewman_enter(struct passenger *pass) {
    printf("\n[*] Entering as a member of the ship crew...\n");
    printf("[*] Checking is running...\n");
    sleep(2);
    if (pass->is_crewman == 1) {
        for (int i = 0; i < PASS_NUMBER; i++) {
            if (ship[i]->is_crewman && !strcmp(ship[i]->token, pass->token))
                printf("[+] Done. Welcome!\n");
                return 1;
        }
    }
    printf("[-] Invalid credentials.\n");
    return 0;
}


void crew_list() {
    char buf[MAX_LEN];
    for (int i = 0; i < PASS_NUMBER; i++) {
        sprintf(buf, "%d", (int) ship[i]->age);
        printf("============================\n");
        printf("%s\n", concat("    * First Name: ", ship[i]->first_name));
        printf("%s\n", concat("    * Last Name:  ", ship[i]->last_name));
        printf("%s\n", concat("    * Country:    ", ship[i]->country));
        printf("%s\n", concat("    * Age:        ", buf));
        printf("%s\n", concat("    * Token:      ", ship[i]->token));
    }
    printf("============================\n\n");
}


void ship_info() {
    printf("[-] This function isn\'t implemented yet\n");
}


struct passenger* find_passenger(int id) {
    for (int i = 0; i < PASS_NUMBER; i++)
        if (ship[i]->id == id) {
            return ship[i];
        }
    return NULL;
}


void freeze(int performer_id, int object_id) {
    struct passenger *pass_ptr = find_passenger(object_id);
    if (pass_ptr == NULL) {
        printf("[-] Invalid id for this operation.\n");
        return;
    }

    if (pass_ptr->is_frozen) {
        printf("[-] Passenger is already frozen.\n");
        return;
    }

    pass_ptr->is_frozen = 1;
    pass_ptr->on_freeze_ptr(pass_ptr);
}


void unfreeze(int performer_id, int object_id) {
    struct passenger *pass_ptr = find_passenger(object_id);
    if (pass_ptr == NULL) {
        printf("[-] Invalid id for this operation.\n");
        return;
    }

    if (!pass_ptr->is_frozen) {
        printf("[-] Passenger isn\'t frozen.\n");
        return;
    }

    pass_ptr->is_frozen = 0;
    pass_ptr->on_unfreeze_ptr(pass_ptr);
}


void print_file_content(char *filename) {
    char c;
    FILE *fd = fopen(filename, "r");

    if (fd) {
        while ((c = getc(fd)) != EOF)
            putchar(c);
        printf("\n");
        fclose(fd);
        return;
    }
    printf("[-] Error while opening the file!\n");
    return;
}


void print_flag2() {
    print_file_content("./flag2");
}


void update_info() {
    if (applier == NULL) {
        printf("[-] You haven\'t sent your aplication yet.\n");
        return;
    }

    int choice = -1;
    long rage;
    char buf[MAX_LEN];

    while (choice != 5) {
        printf("\n[1] Change first name.\n");
        printf("[2] Change last name.\n");
        printf("[3] Change country.\n");
        printf("[4] Change age.\n");
        printf("[5] Back.\n");
        printf(">> ");

        choice = input_choice();

        switch(choice) {
            case 1:
                printf("\nNew first name: ");
                input_string(buf, IN_LEN);
                strcpy(applier->first_name, buf);
                break;
            case 2:
                printf("\nNew last name: ");
                input_string(buf, 2 * IN_LEN + 10);
                strcpy(applier->last_name, buf);
                break;
            case 3:
                printf("\nNew country: ");
                input_string(buf, IN_LEN);
                strcpy(applier->country, buf);
                break;
            case 4:
                rage = 0;
                printf("\nNew age: ");
                if (input_age(&rage)) {
                    long *age = (long *) &applier->age;
                    *age = rage;
                }
                break;
            case 5:
                break;
            default:
                printf("[-] Invalid option.\n");
        }
    }
}


void crewman_menu(int crewman_id) {
    int choice = -1, index;

    printf("\n\n++++=== WELCOME TO THE CREWMAN TERMINAL ===++++\n");

    while (choice != 6) {
        printf("\n[1] List of members of ship\'s crew.\n");
        printf("[2] Information about the ship.\n");
        printf("[3] Freeze a crewman.\n");
        printf("[4] Unfreeze a crewman.\n");
        printf("[5] Show secret information.\n");
        printf("[6] Back.\n");
        printf(">> ");

        choice = input_choice();
        switch (choice) {
            case 1:
                crew_list();
                break;
            case 2:
                ship_info();
                break;
            case 3:
                printf("Passenger\'s index: ");
                index = input_choice();
                freeze(crewman_id, index);
                break;
            case 4:
                printf("Passenger\'s index: ");
                index = input_choice();
                unfreeze(crewman_id, index);
                break;
            case 5:
                print_file_content("./flag1");
                break;
            case 6:
                printf("\n=== WELCOME TO THE APPLICANT TERMINAL ===\n");
                break;
            default:
                printf("[-] Invalid option.\n");
        }
    }
}


void applicant_menu() {
    int choice = -1, is_applied = 0;

    printf("=== WELCOME TO THE APPLICANT TERMINAL ===\n");

    while (choice != 5) {
        printf("\n[1] Apply for a passenger.\n");
        printf("[2] Show the list of applicants.\n");
        printf("[3] Change information in your application.\n");
        printf("[4] Show you application.\n");
        printf("[5] Exit.\n");

        printf(">> ");
        choice = input_choice();

        switch (choice) {
            case 31337:
                if (crewman_enter(applier))
                    crewman_menu(applier->id);
                break;
            case 1:
                if (is_applied == 1) {
                    printf("[-] You're already applied!\n");
                    break;
                }
                applier = apply();
                if (applier)
                    is_applied = 1;
                break;
            case 2:
                show_list();
                break;
            case 3:
                update_info();
                break;
            case 4:
                if (applier) {
                    applier->info_ptr(applier);
                } else {
                    printf("[-] Please, make an application first.\n");
                }
                break;
            case 5:
                printf("See you later!\n");
                break;
            default:
                printf("[-] Invalid option.\n");
        }
    }
}


int main() {
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);

    init_ship();

    header();

    applicant_menu();

    return 0;
}