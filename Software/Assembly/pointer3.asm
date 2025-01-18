// i=0
// while(i<5)
// 	  memory[base+i] = -1
// 	  i++

@i
M=0
(LOOP)
	@i		// if i > R1 terminate loop
	D=M
	@R1
	D=D-M
	@END
	D;JGE
	
	@i
	D=M
	@R0
	D=D+M
	A=D
	M=-1
	
	@i		//increment i
	M=M+1
	
	@LOOP
	0;JMP
(END)
@END
0;JMP