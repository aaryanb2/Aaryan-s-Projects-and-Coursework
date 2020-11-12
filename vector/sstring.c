/**
 * Vector
 * CS 241 - Spring 2020
 */
#include "sstring.h"
#include "vector.h"

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <assert.h>
#include <string.h>

struct sstring {
    // Anything you want
    char* string;
    int length;
};

sstring *cstr_to_sstring(const char *input) {
    // your code goes here
    assert(input != NULL);
    sstring* s = malloc(sizeof(sstring));
    int i = 0;
    while(input[i]){
        i++;
    }
    s->length = i;
    s->string = malloc(sizeof(char)*i); //doubt
    strcpy(s->string, input);
    return s;
}

char *sstring_to_cstr(sstring *input) {
    // your code goes here
    assert(input != NULL);
    return input->string;
}

int sstring_append(sstring *this, sstring *addition) {
    // your code goes here
    assert(this != NULL);
    assert(addition != NULL);
    int len = this->length + addition->length;
    int i = this->length;
    int j = 0;
    while (i < len)
    {
        this->string[i] = addition->string[j];
        i++;
        j++;
    }
    this->string[i] = '\0';
    this->length = len;
    return -1;
}

vector *sstring_split(sstring *this, char delimiter) {
    // your code goes here
    assert(this != NULL);
    vector* vect = vector_create(string_copy_constructor, string_destructor,
                         string_default_constructor);
    int i = 0;
    int start = 0;
    while(i < this->length){
        if(this->string[i] == delimiter){
            vector_push_back(vect, sstring_slice(this,start,i));
            start = i+1;
        }
        i++;
    }
    vector_push_back(vect, sstring_slice(this,start,i));
    return vect;
}

int sstring_substitute(sstring *this, size_t offset, char *target,
                       char *substitution) {
    // your code goes here
    assert(this != NULL);
    int i = 0;
    while(target[i])
        i++;
    int targLen = i;
    char str[this->length];
    i = offset;
    int j =0;
    int subLoc = 0;
    bool found = false;
    while(i < this->length){
        if(target[j] == this->string[i]){
            j++;
        } else{
            j = 0;
        }
        if( j == targLen){
            found = true;
            subLoc = i - targLen + 1;
            int k = 0;
            while(i < this->length){
                str[k] = this->string[i];
                k++;
                i++;
            }
            str[k] = '\0';
            break;
        }
        i++;
    }
    if (found){
        i = 0;
        while (substitution[i])
        {
            this->string[subLoc] = substitution[i];
            i++;
            subLoc++;
        }
        i = 0;
        while(str[i]){
            this->string[subLoc] = str[i];
            i++;
            subLoc++;
        }
        this->string[subLoc] = '\0';
        this->length = subLoc;
        return 0;
        
    }else
    {
        return -1;
    }
    
}

char *sstring_slice(sstring *this, int start, int end) {
    // your code goes here
    assert(this != NULL);
    char *output = NULL;
    int i = 0;
    while(start < end){
        output[0] = this->string[start];
        start++;
        i++;
    }
    output[i] = '\0';
    return output;
}

void sstring_destroy(sstring *this) {
    // your code goes here
    free(this->string);
    this->string = NULL;
    free(this);
    this = NULL;
}
