// kupialnx

@R0
D=M
@i
M=D
(LOOP)
    @i
    D=M
    @END
    D;JLE
    @R1
    D=M
    @R2
    M=D+M
    @i
    M=M-1
    @LOOP
    0;JMP
(END)
    @END
    0;JMP
    
    