@R0
D=M
@R1
D=D-M
@R0GREATER
D;JGT
@R1
D=M
@R2
M=D
@END
0;JMP
(R0GREATER)
	@R0
	D=M
	@R2
	M=D
(END)
	@END
	0;JMP