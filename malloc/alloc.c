/**
 * Malloc
 * CS 241 - Spring 2020
 */
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>


typedef struct meta_data{
	size_t size;
	struct meta_data * next;
    struct meta_data* prev;
	bool isAlloc; // false if free and true if allocated
} meta_data; 

static meta_data* head = NULL;
static meta_data* tail = NULL;
static meta_data* last = NULL;
static int full = 0;
meta_data* findSpace(size_t);
void split(meta_data*, size_t);

meta_data* findSpace(size_t size){//implementing next best fit 
    meta_data* p = last; 
    if(full){
        return NULL;
    }
    while (p){
        if ( p->size >= size && !(p->isAlloc)) {
                if(p->size <= 1.5*size  || p->size - size <= 512) {
                    last = p->next;
                    return p;
                }
                else {
                    split(p, size);
                    last = p->next;
                    return p;
                }
            } 
        p = p->next;
    }
    p = head;
    while (p != last){
        if(p){
            if ( p->size >= size && !(p->isAlloc)) {
                    if((p->size <= 1.5*size + sizeof(meta_data))|| p->size - size <= 512){
                        last = p->next;
                        return p;
                    }
                    else {
                        split(p, size);
                        last = p->next;
                        return p;
                    }
                } 
            p = p->next;
        }
    }
    full = 1;
    return NULL;
}

void split(meta_data* ptr, size_t size){
    size_t new_size = size + sizeof(meta_data);
	size_t remaining = ptr->size - new_size;
    char * newBlock = (char*)ptr + size + sizeof(meta_data);
    meta_data * split = (meta_data *) newBlock;
    split->isAlloc = false;
    split->size = remaining;
    split->prev = ptr;
    if(ptr->next)
        ptr->next->prev = split;
    else
        tail = split;
    split->next = ptr->next;
    ptr->next = split;
    ptr->size = size;	
    full = 0;
    last = split;
}

/**
 * Allocate space for array in memory
 *
 * Allocates a block of memory for an array of num elements, each of them size
 * bytes long, and initializes all its bits to zero. The effective result is
 * the allocation of an zero-initialized memory block of (num * size) bytes.
 *
 * @param num
 *    Number of elements to be allocated.
 * @param size
 *    Size of elements.
 *
 * @return
 *    A pointer to the memory block allocated by the function.
 *
 *    The type of this pointer is always void*, which can be cast to the
 *    desired type of data pointer in order to be dereferenceable.
 *
 *    If the function failed to allocate the requested block of memory, a
 *    NULL pointer is returned.
 *
 * @see http://www.cplusplus.com/reference/clibrary/cstdlib/calloc/
 */
void *calloc(size_t num, size_t size) {
    // implement calloc!
    size_t total = num * size;
	void * ret = malloc(total);
	if (ret) {
        memset(ret, 0, total);
    }

	return ret;
}

/**
 * Allocate memory block
 *
 * Allocates a block of size bytes of memory, returning a pointer to the
 * beginning of the block.  The content of the newly allocated block of
 * memory is not initialized, remaining with indeterminate values.
 *
 * @param size
 *    Size of the memory block, in bytes.
 *
 * @return
 *    On success, a pointer to the memory block allocated by the function.
 *
 *    The type of this pointer is always void*, which can be cast to the
 *    desired type of data pointer in order to be dereferenceable.
 *
 *    If the function failed to allocate the requested block of memory,
 *    a null pointer is returned.
 *
 * @see http://www.cplusplus.com/reference/clibrary/cstdlib/malloc/
 */
void* malloc(size_t size) {
    // implement malloc
    if(size == 0) return NULL;
    meta_data* newdata = findSpace(size);

    if (!newdata) {
        newdata = sbrk(size + sizeof(meta_data));
        // fprintf(stderr, "%p",(void*) newdata);
        // fprintf(stderr, "%p", (void*)(-1));
        // fprintf(stderr, "printed sbrk");
        newdata -> size = size; 
        newdata -> isAlloc = true;

        newdata->next = NULL;
        if (tail) {
            tail->next = newdata;
        }

        newdata->prev = tail;
        tail = newdata;

        if (head == NULL) {
            head = newdata;
        }
    }
    last = newdata->next;
    newdata->isAlloc = true;
    return (char*)newdata+sizeof(meta_data);
}

/**
 * Deallocate space in memory
 *
 * A block of memory previously allocated using a call to malloc(),
 * calloc() or realloc() is deallocated, making it available again for
 * further allocations.
 *
 * Notice that this function leaves the value of ptr unchanged, hence
 * it still points to the same (now invalid) location, and not to the
 * null pointer.
 *
 * @param ptr
 *    Pointer to a memory block previously allocated with malloc(),
 *    calloc() or realloc() to be deallocated.  If a null pointer is
 *    passed as argument, no action occurs.
 */
void free(void *ptr) {
    // implement free! need to implement addition of free blocks next to it
    if(!ptr){
        return;
    }
    meta_data* actptr = ((meta_data*)ptr) - 1;
    actptr->isAlloc = false;
    int flagtail = 0;
    full = 0;
    if(actptr->next && !(actptr->next->isAlloc)){
        size_t newsize = actptr->next->size + actptr->size + sizeof(meta_data);
        actptr->size = newsize;
        actptr->next = actptr->next->next;
        if(actptr->next)
            actptr->next->prev = actptr;
        else
        {
            flagtail =1;
            tail = actptr;
        }     
    }
    last = actptr;
    if(actptr->prev ){
        if(!(actptr->prev->isAlloc)){    
        size_t newsize = actptr->prev->size + actptr->size + sizeof(meta_data);
        actptr->prev->size = newsize;
        actptr->prev->next = actptr->next;
        if(actptr->next)
            actptr->next->prev = actptr->prev;
        else
        {
            flagtail = 1;
            tail = actptr->prev;
        }
        last = actptr->prev;      
        }
    }
    // if(flagtail){
    //     meta_data* newt = tail->prev;
    //     newt->next = NULL;
    //     if(!newt->prev)
    //         head
    //     brk(tail);
    //     tail = newt;
    //     last = newt;
    // }
}

/**
 * Reallocate memory block
 *
 * The size of the memory block pointed to by the ptr parameter is changed
 * to the size bytes, expanding or reducing the amount of memory available
 * in the block.
 *
 * The function may move the memory block to a new location, in which case
 * the new location is returned. The content of the memory block is preserved
 * up to the lesser of the new and old sizes, even if the block is moved. If
 * the new size is larger, the value of the newly allocated portion is
 * indeterminate.
 *
 * In case that ptr is NULL, the function behaves exactly as malloc, assigning
 * a new block of size bytes and returning a pointer to the beginning of it.
 *
 * In case that the size is 0, the memory previously allocated in ptr is
 * deallocated as if a call to free was made, and a NULL pointer is returned.
 *
 * @param ptr
 *    Pointer to a memory block previously allocated with malloc(), calloc()
 *    or realloc() to be reallocated.
 *
 *    If this is NULL, a new block is allocated and a pointer to it is
 *    returned by the function.
 *
 * @param size
 *    New size for the memory block, in bytes.
 *
 *    If it is 0 and ptr points to an existing block of memory, the memory
 *    block pointed by ptr is deallocated and a NULL pointer is returned.
 *
 * @return
 *    A pointer to the reallocated memory block, which may be either the
 *    same as the ptr argument or a new location.
 *
 *    The type of this pointer is void*, which can be cast to the desired
 *    type of data pointer in order to be dereferenceable.
 *
 *    If the function failed to allocate the requested block of memory,
 *    a NULL pointer is returned, and the memory block pointed to by
 *    argument ptr is left unchanged.
 *
 * @see http://www.cplusplus.com/reference/clibrary/cstdlib/realloc/
 */
void *realloc(void *ptr, size_t size) {
    // implement realloc!
    if (!ptr) {
        return malloc(size);
    }   
    if (!size) {
        if (ptr){
            free(ptr);
        }
        return NULL;
    }
    meta_data* cur = (meta_data*)((char*)ptr - sizeof(meta_data));
    size_t prevsize = cur->size;
    if(prevsize >= size){
        if(prevsize >= 1.5*size && prevsize - size > 512)
            split(cur, size);
        return ptr;
    }
    void* newalloc = malloc(size);
    if (newalloc == NULL){
        return NULL;
    }
    memmove(newalloc, ptr, prevsize);
    free(ptr); 
    return newalloc;
}
