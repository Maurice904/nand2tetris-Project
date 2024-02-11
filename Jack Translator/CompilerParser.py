from ParseTree import *
import string

class CompilerParser :

    def __init__(self,tokens):
        self.tokens = tokens
        self.index = -1
        self.current = None
        self.next()
        self.char_set = set(string.ascii_letters)
        self.num_set = set("0123456789")
        self.type_set = {"int", "char", "boolean"}
        self.op_term_set = {'+', '-', '*', '/', '&', '<', '>', '='}
        self.unary_op_set = {'-', '~'}
        self.keyword_constant_set = {'true', 'false', 'null', 'this'}
        self.statement_set = {'while', 'if', 'else', 'let', 'do', 'return'}
    

    def compileProgram(self):
 
        if not self.have("keyword", "class"):
            raise ParseException("The program doesn't begin with a class")
        
        return self.compileClass()
    
    
    def compileClass(self):

        class_tree = ParseTree("class", "")
       
        class_tree.addChild(self.mustBe("keyword", "class"))

        class_tree.addChild(self.mustBe("identifier", self.current.getValue()))
        
        class_tree.addChild(self.mustBe("symbol","{"))
        
        while self.have("keyword", "static") or self.have("keyword", "field"):
      
            class_tree.addChild(self.compileClassVarDec())
       
        while self.have("keyword", "function") or self.have("keyword", "constructor") or self.have("keyword", "method"):
            
            class_tree.addChild(self.compileSubroutine())
        
        class_tree.addChild(self.mustBe("symbol", "}"))

        return class_tree 
    

    def compileClassVarDec(self):
        ClassVarDec = ParseTree("classVarDec", "")
        ClassVarDec.addChild(self.current)
        self.next()

        ClassVarDec.addChild(self.mustBe("keyword", self.type_set))
        ClassVarDec.addChild(self.mustBe("identifier", self.char_set))
        while self.current.getValue() == ",":
            self.next()
            ClassVarDec.addChild(self.mustBe("identifier", self.char_set))
        ClassVarDec.addChild(self.mustBe("symbol", ";"))
        
        return ClassVarDec 
    

    def compileSubroutine(self):

        Subroutine = ParseTree('subroutine', "")
        name = self.current.getValue()
        Subroutine.addChild(self.current)
        self.next()
        if name == "constructor":
            Subroutine.addChild(self.mustBe('identifier', self.char_set))
        elif self.have("keyword", "void") or self.have("keyword", self.type_set):
            Subroutine.addChild(self.current)
            self.next()
        
        else:
            raise ParseException("missing type")
 
        Subroutine.addChild(self.mustBe("identifier", self.char_set))
    
        Subroutine.addChild(self.mustBe('symbol', '('))
        Subroutine.addChild(self.compileParameterList())
        Subroutine.addChild(self.mustBe('symbol', ')'))
      
        Subroutine.addChild(self.compileSubroutineBody())
        


        return Subroutine 
    
    
    def compileParameterList(self):
        parameterList = ParseTree('parameterList', "")
    
        if self.current.getValue() == ")":
            return parameterList
        parameterList.addChild(self.mustBe('keyword', self.type_set))
        parameterList.addChild(self.mustBe('identifier', self.char_set))

        while self.current != None and self.have('symbol', ','):
            
            parameterList.addChild(self.current)
            self.next()
        
            if self.have('keyword', self.type_set) or self.have('identifier', self.char_set):
                parameterList.addChild(self.current)
                self.next()
            else:
                raise ParseException
        
            parameterList.addChild(self.mustBe('identifier', self.char_set))
        return parameterList 
    
    
    def compileSubroutineBody(self):
    
        SubroutineBody = ParseTree('subroutineBody', "")
        SubroutineBody.addChild(self.mustBe('symbol', '{'))
        repeat = 100
        while not self.have('symbol', '}') and repeat > 0:
            repeat -= 1
           
            if self.have('keyword', 'var'):
                
                SubroutineBody.addChild(self.compileVarDec())
            elif self.have('keyword', self.statement_set):
             
                SubroutineBody.addChild(self.compileStatements())
            else:
                raise ParseException('wrong item in the function')
        
        SubroutineBody.addChild(self.mustBe('symbol', '}'))
        return SubroutineBody 
    
    
    def compileVarDec(self):
    
        varDec = ParseTree('varDec', "")
        varDec.addChild(self.current)
        self.next()
        if self.current.getType() == 'keyword':
            varDec.addChild(self.mustBe('keyword', self.type_set))
        elif self.current.getType() == 'identifier':
            varDec.addChild(self.mustBe('identifier', self.char_set))
        else:
            raise ParseException('expected type value here')
        
        varDec.addChild(self.mustBe('identifier', self.char_set))
     
        while self.current.getValue() != ";":
            if self.current.getValue() == ',':
                varDec.addChild(self.current)
            else:
                raise ParseException('expected a ,')
            self.next()

            varDec.addChild(self.mustBe("identifier", self.char_set))

        varDec.addChild(self.mustBe('symbol', ';'))
        
        return varDec 
       

    def compileStatements(self):
   
        statements = ParseTree('statements', '')
        while self.current != None and self.current.getValue() in self.statement_set:
           
           
            if self.current.getValue() == "if":
                statements.addChild(self.compileIf())
            
            elif self.current.getValue() == "let":
                statements.addChild(self.compileLet())
            
            elif self.current.getValue() == "while":
                statements.addChild(self.compileWhile())
            
            elif self.current.getValue() == "do":
                statements.addChild(self.compileDo())
            
            elif self.current.getValue() == "return":
                statements.addChild(self.compileReturn())
        

        return statements 
    
    
    def compileLet(self):
   
        letStatement = ParseTree('letStatement', '')
        letStatement.addChild(self.current)
        self.next()

        letStatement.addChild(self.mustBe('identifier', self.char_set))

        if self.current.getValue() != '=':
            letStatement.addChild(self.mustBe('symbol', '['))
            letStatement.addChild(self.compileExpression())
            letStatement.addChild(self.mustBe('symbol', ']'))

        letStatement.addChild(self.mustBe('symbol', '='))
        letStatement.addChild(self.compileExpression())
        letStatement.addChild(self.mustBe('symbol', ';'))

        return letStatement 


    def compileIf(self):
 
        ifStatement = ParseTree('ifStatement', '')
        ifStatement.addChild(self.current)
        self.next()

        ifStatement.addChild(self.mustBe('symbol', '('))
        ifStatement.addChild(self.compileExpression())
        ifStatement.addChild(self.mustBe('symbol', ')'))

        ifStatement.addChild(self.mustBe('symbol', '{'))
        ifStatement.addChild(self.compileStatements())
        ifStatement.addChild(self.mustBe('symbol', '}'))

        if self.current != None and self.current.getValue() == 'else':
            ifStatement.addChild(self.current)
            self.next()

            ifStatement.addChild(self.mustBe('symbol','{'))
            ifStatement.addChild(self.compileStatements())
            ifStatement.addChild(self.mustBe('symbol','}'))

        return ifStatement 

    
    def compileWhile(self):
    
        whileStatement = ParseTree('whileStatement', '')
        whileStatement.addChild(self.current)
        self.next()

        whileStatement.addChild(self.mustBe('symbol','('))
        whileStatement.addChild(self.compileExpression())
        whileStatement.addChild(self.mustBe('symbol',')'))

        whileStatement.addChild(self.mustBe('symbol','{'))
        whileStatement.addChild(self.compileStatements())
        whileStatement.addChild(self.mustBe('symbol','}'))
        return whileStatement


    def compileDo(self):

        doStatement = ParseTree('doStatement','')
        doStatement.addChild(self.current)
        self.next()

        doStatement.addChild(self.compileExpression())
        doStatement.addChild(self.mustBe('symbol',';'))

        return doStatement 


    def compileReturn(self):

        returnStatement = ParseTree('returnStatement','')
        returnStatement.addChild(self.current)
        self.next()

        if self.current.getValue() != ';':
            returnStatement.addChild(self.compileExpression())
        
        returnStatement.addChild(self.mustBe('symbol',';'))

        return returnStatement 


    def compileExpression(self):
     
        expression = ParseTree('expression', '')
     
        if self.current.getValue() == 'skip':
        
            expression.addChild(self.current)
            self.next()
            return expression
        
       
        expression.addChild(self.compileTerm())
        while self.current and self.current.getValue() != ';' and self.current.getValue() != ')' and self.current.getValue() != ',':
            
            expression.addChild(self.mustBe('symbol', self.op_term_set))
            expression.addChild(self.compileTerm())
  
        return expression 


    def compileTerm(self):
        value = self.current.getValue()
       
        term = ParseTree('term', '')

        if value == '"':
            term.addChild(self.mustBe('symbol', '"'))
            term.addChild(self.mustBe('stringConstant', self.char_set))
            term.addChild(self.mustBe('symbol', '"'))
            
        elif value == '(':
            term.addChild(self.mustBe('symbol', '('))
            term.addChild(self.compileExpression())
            term.addChild(self.mustBe('symbol',')'))
    
        

        elif value[0] in self.char_set:

            if value in self.keyword_constant_set:
                term.addChild(self.mustBe('keyword', self.keyword_constant_set))
            else:
                term.addChild(self.mustBe('identifier', self.char_set))
                if self.current.getValue() == '[':
                    term.addChild(self.mustBe('symbol', '['))
                    term.addChild(self.compileExpression())
                    term.addChild(self.mustBe('symbol', ']'))

                elif self.current.getValue() == '.':
                    term.addChild(self.mustBe('symbol', '.'))
                    term.addChild(self.mustBe('identifier', self.char_set))
                    term.addChild(self.mustBe('symbol', '('))
                    term.addChild(self.compileExpressionList())
                    term.addChild(self.mustBe('symbol',')'))

        elif value[0] in self.num_set:
            term.addChild(self.mustBe('integerConstant', self.num_set))
        
        elif value in self.unary_op_set:
            term.addChild(self.mustBe('symbol', self.unary_op_set))
            if self.current.getValue()[0] in self.num_set:
                term.addChild(self.mustBe('integerConstant', self.num_set))
            elif self.current.getValue()[0] in self.char_set:
                term.addChild(self.mustBe('identifier', self.char_set))
            else:
                raise ParseException('expect number or string after unary op term')
            

            
        else:
            raise ParseException('invalid term')
       
        return term 


    def compileExpressionList(self):
      
        expressionList = ParseTree('expressionList', '')
        
        expressionList.addChild(self.compileExpression())

        while self.current and self.current.getValue() != ';' and self.current.getValue() != ')':
            expressionList.addChild(self.mustBe('symbol', ','))
            expressionList.addChild(self.compileExpression())

        return expressionList 


    def next(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current = self.tokens[self.index]
        else:
            self.current = None
        return


    def have(self,expectedType,expectedValue):

        type_ = self.current.getType()
        value = self.current.getValue()
        if type(expectedValue) == set:
            if type_ == expectedType and (value[0] in expectedValue or value in expectedValue):
                return True
        elif type_ == expectedType and value == expectedValue:
            return True
        
        return False


    def mustBe(self,expectedType,expectedValue):
        
        type_ = self.current.getType()
        value = self.current.getValue()
        if type(expectedValue) == set:
            if type_ == expectedType and (value[0] in expectedValue or value in expectedValue):
                prev = self.current
                self.next()
                return prev
        elif type_ == expectedType and value == expectedValue:
            prev = self.current
            self.next()
            return prev
        
        raise ParseException(f"Expected token type: '{expectedType}' and value '{expectedValue}' but found type: '{self.current.getType()}' and value: '{self.current.getValue()}'")
    

if __name__ == "__main__":


    tokens = []
    # tokens.append(Token("keyword","class"))
    # tokens.append(Token("identifier","Test"))
    # tokens.append(Token("symbol","{"))



    # tokens.append(Token("keyword","function"))
    # tokens.append(Token("keyword","void"))
    # tokens.append(Token("identifier","test"))
    # tokens.append(Token("symbol","("))

    # tokens.append(Token("keyword","int"))
    # tokens.append(Token("identifier","a"))

    # tokens.append(Token("symbol",")"))
    # tokens.append(Token("symbol","{"))
    # tokens.append(Token("symbol","}"))

    # tokens.append(Token("symbol","}"))

    # tokens.append(Token("symbol","{"))
    # tokens.append(Token("keyword","var"))
    # tokens.append(Token("keyword","int"))
    # tokens.append(Token("identifier","a"))
    # tokens.append(Token("symbol",";"))
    # tokens.append(Token("symbol","}"))

    # tokens.append(Token("keyword","let"))
    # tokens.append(Token("identifier","a"))
    # tokens.append(Token("symbol","="))
    # tokens.append(Token("keyword","skip"))
    # tokens.append(Token("symbol", ";"))
    # tokens.append(Token("keyword", "do"))
    # tokens.append(Token("keyword", "skip"))
    # tokens.append(Token("symbol", ";"))
    # tokens.append(Token("keyword", "return"))
    # tokens.append(Token("symbol", ";"))

    # tokens.append(Token("keyword","var"))
    # tokens.append(Token("identifier","Test"))
    # tokens.append(Token("identifier","a"))
    # tokens.append(Token('symbol', ';'))

    # if statement test
  
    # tokens.append(Token("keyword", "if"))
    # tokens.append(Token("symbol", "("))
    # tokens.append(Token("keyword", "skip"))
    # tokens.append(Token("symbol", ")"))
    # tokens.append(Token("symbol", "{"))
    # tokens.append(Token("symbol", "}"))
    # tokens.append(Token("keyword", "else"))
    # tokens.append(Token("symbol", "{"))
    # tokens.append(Token("symbol", "}"))


    # tokens.append(Token("keyword", "if"))
    # tokens.append(Token("symbol", "("))
    # tokens.append(Token("keyword", "skip"))
    # tokens.append(Token("symbol", ")"))
    # tokens.append(Token("symbol", "{"))

    # tokens.append(Token("keyword", "if"))
    # tokens.append(Token("symbol", "("))
    # tokens.append(Token("keyword", "skip"))
    # tokens.append(Token("symbol", ")"))
    # tokens.append(Token("symbol", "{"))
    # tokens.append(Token("symbol", "}"))
    # tokens.append(Token("keyword", "else"))
    # tokens.append(Token("symbol", "{"))
    # tokens.append(Token("symbol", "}"))

    # tokens.append(Token("symbol", "}"))
    # tokens.append(Token("keyword", "else"))
    # tokens.append(Token("symbol", "{"))

    # tokens.append(Token("keyword", "if"))
    # tokens.append(Token("symbol", "("))
    # tokens.append(Token("keyword", "skip"))
    # tokens.append(Token("symbol", ")"))
    # tokens.append(Token("symbol", "{"))
    # tokens.append(Token("symbol", "}"))
    # tokens.append(Token("keyword", "else"))
    # tokens.append(Token("symbol", "{"))
    # tokens.append(Token("symbol", "}"))

    # tokens.append(Token("symbol", "}"))

    #while statement test
    # tokens.append(Token("keyword", "while"))
    # tokens.append(Token("symbol", "("))
    # tokens.append(Token("keyword", "skip"))
    # tokens.append(Token("symbol", ")"))
    # tokens.append(Token("symbol", "{"))
    # tokens.append(Token("symbol", "}"))

    # expression test
    # tokens.append(Token("symbol", "("))
    # tokens.append(Token("symbol", "("))
    # tokens.append(Token("identifier", "a"))
    # tokens.append(Token("symbol", "+"))
    # tokens.append(Token("symbol", "("))
    # tokens.append(Token("integerConstant", "1"))
    # tokens.append(Token("symbol", "-"))
    # tokens.append(Token("identifier", "c"))
    # tokens.append(Token("symbol", ")"))
    # tokens.append(Token("symbol", ")"))
    # tokens.append(Token("symbol", ">"))
    # tokens.append(Token("integerConstant", "5"))
    # tokens.append(Token("symbol", ")"))
    # tokens.append(Token("symbol", "="))
    # tokens.append(Token("keyword", "true"))

    # tokens.append(Token("symbol", "("))
    # tokens.append(Token("identifier", "a"))
    # tokens.append(Token("symbol", "+"))
    # tokens.append(Token("identifier", "c"))
    # tokens.append(Token("symbol", ")"))
    # tokens.append(Token("symbol", "="))
    # tokens.append(Token("keyword", "true"))

    tokens.append(Token("identifier", "Main"))
    tokens.append(Token("symbol", "."))
    tokens.append(Token("identifier", "myFunc"))
    tokens.append(Token("symbol", "("))
    tokens.append(Token("integerConstant", "1"))
    tokens.append(Token("symbol", ","))
    tokens.append(Token("stringConstant", "Hello"))
    tokens.append(Token("symbol", ")"))

    

    parser = CompilerParser(tokens)
    try:
        result = parser.compileExpression()
        print(result)
    except ParseException as e:
          print(f"Error Parsing: {e}")
