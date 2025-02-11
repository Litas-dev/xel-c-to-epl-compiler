
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>

#define PACKAGE "wgram"
#define VERSION "0.1.0"
#define MAXLINE 1024
#define MAXGRAM 32

/* Function Prototypes */
void print_help(int exval);

int main(int argc, char *argv[]) {
    /* Word delimiter for strtok() */
    char delim[] = ".,:;`/\"+-_(){}[]<>*&^%$#@!?~/|\\=1234567890 \t\n";
    char line[MAXLINE];     /* Input buffer */
    char *stray = NULL;     /* Token returned by strtok() */
    char **strarray = NULL; /* Dynamic array to store words */
    int i = 0, strcount = 0;/* Counters */
    int N = 3, pos = 0;     /* N-gram size (default: 3) */
    int opt = 0, word_flag = 0;  /* Flags */
    FILE *fp = stdin;       /* Default input source */

    /* Parse command-line options */
    while ((opt = getopt(argc, argv, "hvn:wf:")) != -1) {
        switch (opt) {
            case 'h':
                print_help(0);
                break;
            case 'v':
                printf("%s version %s\n", PACKAGE, VERSION);
                exit(0);
                break;
            case 'n':
                N = atoi(optarg);
                if (N < 2 || N > MAXGRAM) {
                    fprintf(stderr, "%s: Error - Ngram length `%d` out of range `2-%d`\n",
                            PACKAGE, N, MAXGRAM);
                    return 1;
                }
                break;
            case 'w':
                word_flag = 1;
                break;
            case 'f':
                fp = freopen(optarg, "r", stdin);
                if (!fp) {
                    fprintf(stderr, "%s: Error - Unable to open file `%s`\n", PACKAGE, optarg);
                    return 1;
                }
                break;
            case '?':
                fprintf(stderr, "%s: Error - Unknown option: `%c`\n\n", PACKAGE, optopt);
                print_help(1);
        }
    }

    /* Read input and process tokens */
    while (fgets(line, MAXLINE, fp) != NULL) {
        if (strlen(line) < 2)
            continue;

        stray = strtok(line, delim);
        while (stray != NULL) {
            char **temp = realloc(strarray, (strcount + 1) * sizeof(char *));
            if (!temp) {
                fprintf(stderr, "%s: Error - Memory allocation failed\n", PACKAGE);
                free(strarray);
                return 1;
            }
            strarray = temp;
            
            strarray[strcount] = strdup(stray);
            if (!strarray[strcount]) {
                fprintf(stderr, "%s: Error - Memory allocation for word failed\n", PACKAGE);
                return 1;
            }
            strcount++;
            stray = strtok(NULL, delim);
        }
    }

    /* Print n-grams or raw words */
    if (word_flag == 0) {
        for (i = 0, pos = N; i < strcount; i++, pos--) {
            if (pos == 0) {
                pos = N;
                i -= (N - 1);
                printf("\n");
            }
            printf("%s ", strarray[i]);
        }
        printf("\n");
    } else {
        for (i = 0; i < strcount; i++)
            printf("%s\n", strarray[i]);
    }

    /* Free allocated memory */
    for (i = 0; i < strcount; i++)
        free(strarray[i]);
    free(strarray);

    return 0;
}

/* Print help message */
void print_help(int exval) {
    printf("%s %s - Extract N-grams from text data\n", PACKAGE, VERSION);
    printf("Usage: %s [-h] [-v] [-n INT] [-w] [-f FILE]\n\n", PACKAGE);
    printf(" -h        Show help and exit\n");
    printf(" -v        Show version and exit\n");
    printf(" -n INT    Set n-gram length (default: 3, range: 2-%d)\n", MAXGRAM);
    printf(" -w        Print only extracted words\n");
    printf(" -f FILE   Read input from `FILE` (default: stdin)\n\n");
    exit(exval);
}
