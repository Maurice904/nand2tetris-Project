class VMTranslator:

    def vm_push(segment, offset):
        offset = int(offset)
        string = "invalid"

        if segment == "static":
            index = 16 + offset
            string = f"@{index}\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D"

        elif segment == "local":
            string = f"@LCL\nD=M\n@{offset}\nA=D+A\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D"

        elif segment == "argument":
           string = f"@ARG\nD=M\n@{offset}\nA=D+A\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D"

        elif segment == "this":
            string = f"@THIS\nD=M\n@{offset}\nA=D+A\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D"

        elif segment == "that":
            string = f"@THAT\nD=M\n@{offset}\nA=D+A\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D"

        elif segment == "constant":
            string = f"@{offset}\nD=A\n@SP\nAM=M+1\nA=A-1\nM=D"

        elif segment == "pointer":
            index = 3 + offset
            string = f"@{index}\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D"

        elif segment == "temp":
            index = 5 + offset
            string = f"@{index}\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D"

        
        return string

    def vm_pop(segment, offset):
        offset = int(offset)
        string = "@SP\nAM=M-1\nD=M\n"

        if segment == "static":
            index = 16 + offset
            string += f"@{index}\nM=D"

        elif segment == "local":
            index = ""
            while offset > 0:
                index += "A=A+1\n"
                offset -= 1
            string += f"@LCL\nA=M\n{index}M=D"

        elif segment == "argument":
            index = ""
            while offset > 0:
                index += "A=A+1\n"
                offset -= 1
            string += f"@ARG\nA=M\n{index}M=D"
            
        

        elif segment == "this":
            index = ""
            while offset > 0:
                index += "A=A+1\n"
                offset -= 1
            string += f"@THIS\nA=M\n{index}M=D"
        

        elif segment == "that":
            index = ""
            while offset > 0:
                index += "A=A+1\n"
                offset -= 1
            string += f"@THAT\nA=M\n{index}M=D"

        elif segment == "pointer":
            index = 3 + offset
            string += f"@{index}\nM=D"
        

        elif segment == "temp":
            index = 5 + offset
            string += f"@{index}\nM=D"
        
        return string

    def vm_add():
        string = f"@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D"
        return string

    def vm_sub():
        string = f"@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D"
        return string

    def vm_neg():
        string = f"@SP\nA=M-1\nM=-M"
        return string

    def vm_eq():
        string ="@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n@labelTrue\nD;JEQ\nD=0\n@labelFalse\n0;JMP\n(labelTrue)\nD=-1\n(labelFalse)\n@SP\nA=M\nM=D\n@SP\nM=M+1"
        return string

    def vm_gt():
        string ="@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n@labelTrue\nD;JGT\nD=0\n@labelFalse\n0;JMP\n(labelTrue)\nD=-1\n(labelFalse)\n@SP\nA=M\nM=D\n@SP\nM=M+1"
        return string

    def vm_lt():
        string ="@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n@labelTrue\nD;JLT\nD=0\n@labelFalse\n0;JMP\n(labelTrue)\nD=-1\n(labelFalse)\n@SP\nA=M\nM=D\n@SP\nM=M+1"
        return string

    def vm_and():
        string ="@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D"
        return string

    def vm_or():
        string ="@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D"
        return string

    def vm_not():
        string = "@SP\nA=M-1\nM=!M"
        return string

    def vm_label(label):
      
        string = f"({label})"
        return string

    def vm_goto(label):
    
        string = f"@{label}\n0;JMP"
        return string

    def vm_if(label):
     
        string = f"@SP\nAM=M-1\nD=M\n@False\nD;JEQ\n@{label}\n0;JMP\n(False)"
        return string

    def vm_function(function_name, n_vars):
        string = f"({function_name})\n"
        while n_vars > 0:
            if n_vars > 1:
                string += VMTranslator.vm_push("constant","0") + "\n"
            else:
                string += VMTranslator.vm_push("constant","0")
            n_vars -= 1
        return string

    def vm_call(function_name, n_args):
        # push return address
        # push LCL
        # push ThIS
        # push THAT
        # arg = SP-5-n_args
        # LCL = SP
        # goto function_name
        # (return address)
        
        push_return = f"@{function_name}.return\nD=A\n@SP\nAM=M+1\nA=A-1\nM=D"
        push_LCL = "@LCL\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D"
        push_arg = "@ARG\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D"
        push_THIS = "@3\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D"
        push_THAT = "@4\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D"
        set_arg = f"@SP\nD=M\n@5\nD=D-A\n@{n_args}\nD=D-A\n@ARG\nM=D"
        set_LCL = "@SP\nD=M\n@LCL\nM=D"
        goto = VMTranslator.vm_goto(function_name)
        label = VMTranslator.vm_label(f'{function_name}.return')
        string = f"{push_return}\n{push_LCL}\n{push_arg}\n{push_THIS}\n{push_THAT}\n{set_arg}\n{set_LCL}\n{goto}\n{label}"
        return string

    def vm_return():
        # end = LCL
        # return address = LCL - 5
        # arg = pop()
        # sp = arg + 1
        #  that = end - 1
        # this = end - 2
        # arg = end - 3
        # lcl = end -4
        # goto return address

        store_end = "@LCL\nD=M\n@5\nM=D"
        store_return = "@5\nD=M\n@5\nA=D-A\nD=M\n@6\nM=D"
        return_arg = VMTranslator.vm_pop("argument","0")
        set_sp = "@ARG\nD=M+1\n@SP\nM=D"
        set_that = "@5\nD=M\nA=D-1\nD=M\n@THAT\nM=D"
        set_this = "@5\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D"
        set_arg = "@5\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D"
        set_lcl = "@5\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D"
        goto = "@6\nA=M\n0;JMP"
        string = f"{store_end}\n{store_return}\n{return_arg}\n{set_sp}\n{set_that}\n{set_this}\n{set_arg}\n{set_lcl}\n{goto}"
        return string

# A quick-and-dirty parser when run as a standalone script.
if __name__ == "__main__":
    import sys
    if(len(sys.argv) > 1):
        with open(sys.argv[1], "r") as a_file:
            for line in a_file:
                tokens = line.strip().lower().split()
                if(len(tokens)==1):
                    if(tokens[0]=='add'):
                        print(VMTranslator.vm_add())
                    elif(tokens[0]=='sub'):
                        print(VMTranslator.vm_sub())
                    elif(tokens[0]=='neg'):
                        print(VMTranslator.vm_neg())
                    elif(tokens[0]=='eq'):
                        print(VMTranslator.vm_eq())
                    elif(tokens[0]=='gt'):
                        print(VMTranslator.vm_gt())
                    elif(tokens[0]=='lt'):
                        print(VMTranslator.vm_lt())
                    elif(tokens[0]=='and'):
                        print(VMTranslator.vm_and())
                    elif(tokens[0]=='or'):
                        print(VMTranslator.vm_or())
                    elif(tokens[0]=='not'):
                        print(VMTranslator.vm_not())
                    elif(tokens[0]=='return'):
                        print(VMTranslator.vm_return())
                elif(len(tokens)==2):
                    if(tokens[0]=='label'):
                        print(VMTranslator.vm_label(tokens[1]))
                    elif(tokens[0]=='goto'):
                        print(VMTranslator.vm_goto(tokens[1]))
                    elif(tokens[0]=='if-goto'):
                        print(VMTranslator.vm_if(tokens[1]))
                elif(len(tokens)==3):
                    if(tokens[0]=='push'):
                        print(VMTranslator.vm_push(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='pop'):
                        print(VMTranslator.vm_pop(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='function'):
                        print(VMTranslator.vm_function(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='call'):
                        print(VMTranslator.vm_call(tokens[1],int(tokens[2])))

        