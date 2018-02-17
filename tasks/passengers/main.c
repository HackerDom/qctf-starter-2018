// gcc main.c -o main -no-pie

#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <zconf.h>
#include <fcntl.h>


const int MAX_LEN   = 0xfffff;
const int PASS_LEN  = 50;
const int INPUT_LEN = 50;
const int AGE_LEN   = 25;

int PASSENGERS_COUNT = 0;
int PASSANGER_NUMBER = 0;


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


char* concat(const char s1[], const char s2[]) {
    char *buf = malloc(strlen(s1) + strlen(s2));
    strcpy(buf, s1);
    strcat(buf, s2);
    return buf;
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
    printf("    First name: %s\n", pass->first_name);
    printf("    Last name:  %s\n", pass->last_name);
    printf("    Age:        %d\n", pass->age);
}


struct passenger* create_passenger(char *first_name, char *last_name, char *country, long age) {
    struct passenger *passng = malloc(sizeof(struct passenger));

    passng->id         = PASSENGERS_COUNT++;
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


struct passenger* set_crewman_privilege(struct passenger *pass, char *token) {
    int len = strlen(token);

    if (len >= 7)
        token[6] = '\x00';

    pass->is_crewman = 1;
    strcpy(pass->token, token);
    return pass;
}


int add_passenger(struct passenger *pass) {
    if (PASS_LEN <= PASSANGER_NUMBER) {
        return 1;
    }
    ship[PASSANGER_NUMBER] = pass;
    PASSANGER_NUMBER++;
    return 0;
}


void init_ship() {
    add_passenger(set_crewman_privilege(create_passenger("John", "Smith", "ENG", 39), "rim96z"));
    add_passenger(set_crewman_privilege(create_passenger("Maria", "Garcia", "ENG", 24), "tjqb2v"));
    add_passenger(set_crewman_privilege(create_passenger("Konata", "Izumi", "JAP", 18), "99iap3"));
    add_passenger(set_crewman_privilege(create_passenger("Dmitry", "Sokolov", "RUS", 32), "nv7btm"));
    add_passenger(set_crewman_privilege(create_passenger("Lucas", "Aris", "FRA", 23), "th4a80"));
}


void input_string(char *str, int size) {
    fgets(str, size, stdin);
    str[strlen(str) - 1] = 0;
}


int input_choice() {
    int choice;
    char buf[100];

    input_string(buf, sizeof(buf));
    int sscanf_res = sscanf(buf, "%d", &choice);

    if ((sscanf_res == 0) || (sscanf_res == EOF)) {
        choice = -1;
    }
    return choice;
}


long parse_long(char *s) {
    char *ptr;
    return strtol(s, &ptr, 10);
}


void header() {
    printf("============ WELCOME TO OUR SHiP ============\n");
}


int input_age(long *real_age) {
    char age[MAX_LEN];

    input_string(age, AGE_LEN);
    *real_age = parse_long(age);

    if (*real_age <= 18) {
        printf("[-] Invalid age, try again!\n\n");
        return 0;
    } else return 1;
}


struct passenger* apply() {
    long real_age = 0;
    char firstname[MAX_LEN], lastname[MAX_LEN], country[MAX_LEN];

    printf("\nThank you for applying!\nPlease, full the fields below:\n");
    printf("============================\n");
    printf("     First name [50]: ");
    input_string(firstname, INPUT_LEN);

    printf("     Last name [50]: ");
    input_string(lastname, INPUT_LEN);

    printf("     Country [50]: ");
    input_string(country, INPUT_LEN);

    printf("     Age: ");
    if (!input_age(&real_age)) return NULL;

    struct passenger *pass = create_passenger(firstname, lastname, country, real_age);
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
        for (int i = 0; i < PASSANGER_NUMBER; i++) {
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
    for (int i = 0; i < PASSANGER_NUMBER; i++) {
        sprintf(buf, "%d", (int) ship[i]->age);
        printf("============================\n");
        printf("    * First Name: %s\n", ship[i]->first_name);
        printf("    * Last Name:  %s\n", ship[i]->last_name);
        printf("    * Country:    %s\n", ship[i]->country);
        printf("    * Age:        %s\n", buf);
        printf("    * Token:      %s\n", ship[i]->token);
    }
    printf("============================\n\n");
}


void ship_info() {
    printf("[-] This function isn\'t implemented yet\n");
}


struct passenger* find_passenger(int id) {
    for (int i = 0; i < PASSANGER_NUMBER; i++)
        if (ship[i]->id == id) {
            return ship[i];
        }
    return NULL;
}


void freeze(int object_id) {
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


void unfreeze(int object_id) {
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
    long real_age;
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
                input_string(buf, sizeof(applier->first_name));
                strcpy(applier->first_name, buf);
                break;
            case 2:
                printf("\nNew last name: ");
                input_string(buf, sizeof(applier->last_name) + 10);
                strcpy(applier->last_name, buf);
                break;
            case 3:
                printf("\nNew country: ");
                input_string(buf, sizeof(applier->country));
                strcpy(applier->country, buf);
                break;
            case 4:
                real_age = 0;
                printf("\nNew age: ");
                if (input_age(&real_age)) {
                    long *age = (long *) &applier->age;
                    *age = real_age;
                }
                break;
            case 5:
                break;
            default:
                printf("[-] Invalid option.\n");
        }
    }
}


void crewman_menu() {
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
                freeze(index);
                break;
            case 4:
                printf("Passenger\'s index: ");
                index = input_choice();
                unfreeze(index);
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
                    crewman_menu();
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
