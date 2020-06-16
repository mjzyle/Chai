#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

int main(int argc, char** argv){

    // Setup the neural network model and save before starting any simulations
    system("python -c \"import ai_controller; ai_controller.setup_model();\"");

    const int threads = 4;              // Number of parallel threads
    const int sims = 100;               // Number of total simulations

    // Execute simulations in parallel
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