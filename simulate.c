#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

int main(int argc, char** argv){

    const int sims = atoi(argv[1]);                 // Number of total simulations
    const int timeout = atoi(argv[2]);              // Number of parallel threads
    char access_key_id[100], access_key_secret[100];
    strcpy(access_key_id, argv[3]);
    strcpy(access_key_secret, argv[4]);
    int i = 0;

    // Execute simulations in parallel
    #pragma omp parallel for
    for (i = 0; i < sims; i++) {
        char func[400] = "python gameloop.py ";
        char sim_char[5], timeout_char[5];

        sprintf(sim_char, "%d", i);
        sprintf(timeout_char, "%d", timeout);

        strcat(func, sim_char);
        strcat(func, " ");
        strcat(func, timeout_char);
        strcat(func, " ");
        strcat(func, access_key_id);
        strcat(func, " ");
        strcat(func, access_key_secret);

        system(func);
    }

    return 0;

}