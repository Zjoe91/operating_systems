.data
int_values: .space 20
max_value: .word 5
n_values: .word 11
even_sum: .word 0
input1: .asciiz "How many values do you want to enter? "
input2: .asciiz " is the maximum amount allowed\n"
input3: .asciiz "Enter value "
print1: .asciiz "The values are "
print2: .asciiz "The sum of even values is "
space: .asciiz " "
line_break: .asciiz "\n"

.text
.globl main

j main

# print subroutines
print_int:
	li $v0, 1
    syscall
    jr $ra

print_string:
    li $v0, 4
    syscall
    jr $ra
    
print_space:
	la $a0, space
    li $v0, 4
    syscall
    jr $ra
    
print_break:
	la $a0, line_break
    li $v0, 4
    syscall
    jr $ra
    
# method to find address of an index
calculate_index:
	la $t4, int_values
	sll $t5, $t5, 2
	add $t4, $t4, $t5
	jr $ra

main:
    lw $t0, n_values
    lw $t1, max_value
    addi $t1, $t1, 1

while_bigger_than_max:
	# print input question
	la $a0, input1
	jal print_string
	
	# ask for n_values
	li $v0, 5
    syscall
    move $t0, $v0
    
	blt $t0, $t1, init_index
    
	# print max_value
	lw $a0, max_value
	jal print_int
	la $a0, input2
	jal print_string
	
	j while_bigger_than_max
	
init_index:
	# initialise iterator for loop
	li $t1, 0
	subi $t0, $t0, 1
    
int_list_loop:
	bgt $t1, $t0, init_value
	
	# print enter value
	la $a0, input3
	jal print_string
	
	# value number
	addi $t2, $t1, 1
	la $a0, ($t2)
	jal print_int
	
	jal print_space
	
	# ask for input
	li $v0, 5
    syscall
    
    # add the value to the list
    move $t5, $t1
    jal calculate_index
    sw $v0, 0($t4)
    
    # incement iterator by one
    addi $t1, $t1, 1
    
    j int_list_loop
    
init_value:
	# initialise iterator for loop
	li $t1, 0
    
even_num_check_loop:
	bgt $t1, $t0, final_print1
	
	# access item in list
	move $t5, $t1
	jal calculate_index
	lw $t2, 0($t4)
	
	# check if the integer is even
	li $t3, 2
	div $t2, $t3
	mfhi $t3
	li $t5, 0
	
	# incement iterator by one
	addi $t1, $t1, 1
	
	beq $t3, $t5, even_num
	
	j even_num_check_loop
	
even_num:
	# add even num to even sum
	lw $t3, even_sum
	add $t3, $t3, $t2
	sw $t3, even_sum
	
	j even_num_check_loop
	
final_print1:
	# print string
	la $a0, print1
	jal print_string
	
	# initialise iterator for loop
	li $t2, 0
	
print_int_loop:
	beq $t2, $t1, final_print2
	
	# access item in list
	move $t5, $t2
	jal calculate_index
	lw $a0, 0($t4)
	jal print_int
	
	jal print_space
	
	# incremetn iterator by one
	addi $t2, $t2, 1
	
	j print_int_loop
	
final_print2:
		
	jal print_break

	# print even sum total
	la $a0, print2
	jal print_string
	
	lw $a0, even_sum
	jal print_int
	
	# gracefully finish the execution of the program
	li $v0, 10
    syscall
	
	
	
