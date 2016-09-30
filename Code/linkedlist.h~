#include<stdio.h>
#include<stdlib.h>

struct node {
	void *data;

	struct node *next;
};

typedef struct node node;

struct list {
	node* head;
	int64_t* length;
}

void push(node** head_ref, void *new_data, size_t data_size)
{
    // Allocate memory for node
    node* new_node = ( node*)malloc(sizeof( node));
 
    new_node->data  = malloc(data_size);
    new_node->next = (*head_ref);
 
    // Copy contents of new_data to newly allocated memory.
    // Assumption: char takes 1 byte.
    int i;
    for (i=0; i<data_size; i++)
        *(char *)(new_node->data + i) = *(char *)(new_data + i);
 
    // Change head pointer as new node is added at the beginning
    (*head_ref)    = new_node;
}

void append( node** curr_ref, void *new_data, size_t data_size)
{
    if (curr_ref->next == null) {
    	node* new_node = (node*) malloc(sizeof(node));
	int i;
        for (i=0; i<data_size; i++) {
		*(char *)(new_node->data + i) = *(char *)(new_data + i);
	}
	curr_ref->next = new_node;
    }
    else {
	append(&(curr_ref->next), new_data, data_size);
    }
}

void pop(node**curr_ref) {
    if (curr_ref->next == null) {
	   printf("Can't pop on last node.");
    }
    if ((curr_ref->next)->next == null) {
	    node* output = curr_ref->next;
	    curr_ref->next = null;
	    return output;
    }
    pop(&(curr_ref->node));
}

