// kupialnx
//TODO: Find out if it is possible to combine Paint_WHITE and PAINT_BLACK.

// Creates "pointers" i and j to the address of screens first memory slot.
@SCREEN
D=A
@i
M=D
@j
M=D

(MAIN_LOOP)
    @102
    D=A
    @KBD
    D=D-M
    @PAINT_BLACK
    D;JEQ
    @PAINT_WHITE
    0;JMP

(PAINT_WHITE)
    @SCREEN
    D=A
    @i
    M=D
    // If last position is reached, jump to end.
    @KBD
    D=A
    @j
    D=D-M
    @MAIN_LOOP
    D;JLE

    @j
    A=M
    M=0
    @j
    M=M+1
    @MAIN_LOOP
    0;JMP
    

(PAINT_BLACK)
    @SCREEN
    D=A
    @j
    M=D
    // If last position is reached, jump to the main.
    @KBD
    D=A
    @i
    D=D-M
    @MAIN_LOOP
    D;JLE

    // Take value of the i and use it as address and assign it to -1 (1111111111111111). 
    @i
    A=M
    M=-1
    @i
    M=M+1
    @MAIN_LOOP
    0;JMP
    