#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

int main(int argc, char** argv){

    const int threads = 4;
    const int sims = 200;

    #pragma omp parallel for
    for (int i = 0; i < threads; i++) {
        char func[400] = "python gameloop.py ";
        char start[5], end[5];

        sprintf(start, "%d", i*sims/threads);
        sprintf(end, "%d", i*sims/threads + sims/threads);

        strcat(func, start);
        strcat(func, " ");
        strcat(func, end);

        system(func);
    }

    return 0;

}