"""
Core Lexical Analyzer - DFA-based Token Recognition
"""

import re
from enum import Enum
from typing import List, Tuple, Optional
from dataclasses import dataclass

class TokenType(Enum):
    """Define all possible token types"""
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    OPERATOR = "OPERATOR"
    DELIMITER = "DELIMITER"
    STRING = "STRING"
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    INVALID = "INVALID"

@dataclass
class Token:  
    """Token data structure"""
    type: TokenType
    value: str
    position: int
    line: int
    
    def to_dict(self):
        """Convert token to dictionary for JSON serialization"""
        return {
            'type': self.type.value,
            'value':  self.value,
            'line': self.line,
            'position': self.position
        }
    
    def __str__(self):
        return f"<{self.type.value}, '{self.value}', Line:  {self.line}, Pos: {self.position}>"

class DFA:
    """Base DFA class for token recognition"""
    def __init__(self, pattern: str, token_type: TokenType, priority: int):
        self.pattern = re.compile(pattern)
        self.token_type = token_type
        self.priority = priority
    
    def match(self, text: str, position: int) -> Optional[Tuple[str, int]]:
        """
        Try to match pattern starting at position
        Returns (matched_string, end_position) or None
        """
        match = self.pattern.match(text, position)
        if match:
            return (match.group(0), match.end())
        return None

class TokenRecognitionSystem:  
    """Main Token Recognition System using DFA"""
    
    def __init__(self):
        self.dfas: List[DFA] = []
        self.keywords = {
            'if', 'else', 'elif', 'while', 'for', 'return', 'int', 'float', 
            'char', 'void', 'class', 'public', 'private', 'protected',
            'def', 'import', 'from', 'as', 'break', 'continue', 'pass',
            'try', 'except', 'finally', 'raise', 'with', 'lambda', 'yield',
            'struct', 'union', 'enum', 'typedef', 'const', 'static', 'extern',
            'volatile', 'auto', 'register', 'sizeof', 'goto', 'switch', 'case',
            'default', 'do', 'long', 'short', 'signed', 'unsigned', 'double'
        }
        self._initialize_dfas()
    
    def _initialize_dfas(self):
        """Define regular expressions and construct DFAs for each token type"""
        
        dfa_definitions = [
            (r'//[^\n]*', TokenType.COMMENT, 10),
            (r'/\*[\s\S]*?\*/', TokenType.COMMENT, 10),
            (r'#[^\n]*', TokenType.COMMENT, 10),
            (r'"(?:[^"\\]|\\.)*"', TokenType.STRING, 9),
            (r"'(?:[^'\\]|\\.)*'", TokenType.STRING, 9),
            (r'\d+\.\d+(?:[eE][+-]?\d+)?', TokenType.FLOAT, 8),
            (r'\d+[eE][+-]?\d+', TokenType.FLOAT, 8),
            (r'\d+', TokenType.INTEGER, 7),
            (r'(?:\+\+|--|==|!=|<=|>=|&&|\|\||<<|>>|\+=|-=|\*=|/=|%=|&=|\|=|\^=|->|::)', TokenType.OPERATOR, 6),
            (r'[+\-*/%=<>!&|^~]', TokenType.OPERATOR, 5),
            (r'[(){}\[\];,\.:@]', TokenType.DELIMITER, 4),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER, 3),
            (r'[ \t\n\r]+', TokenType.WHITESPACE, 1),
        ]
        
        self.dfas = [DFA(pattern, token_type, priority) 
                     for pattern, token_type, priority in dfa_definitions]
        self.dfas.sort(key=lambda x: x.priority, reverse=True)
    
    def tokenize(self, input_text: str) -> dict:
        """
        Main tokenization method using DFA traversal
        Returns dictionary with tokens and errors
        """
        tokens = []
        position = 0
        line = 1
        line_start = 0
        errors = []
        
        while position < len(input_text):
            matched = False
            best_match = None
            best_dfa = None
            
            for dfa in self.dfas:
                result = dfa.match(input_text, position)
                if result:  
                    matched_text, end_pos = result
                    
                    if not best_match or len(matched_text) > len(best_match[0]):
                        best_match = result
                        best_dfa = dfa
                        break
            
            if best_match:
                matched_text, end_pos = best_match
                token_type = best_dfa.token_type
                
                if token_type == TokenType.IDENTIFIER:  
                    if matched_text in self.keywords:
                        token_type = TokenType.KEYWORD
                
                if token_type != TokenType.WHITESPACE:  
                    token = Token(
                        type=token_type,
                        value=matched_text,
                        position=position - line_start,
                        line=line
                    )
                    tokens.append(token)
                
                line += matched_text.count('\n')
                if '\n' in matched_text:  
                    line_start = position + matched_text.rfind('\n') + 1
                
                position = end_pos
                matched = True
            
            if not matched:
                error_char = input_text[position]
                error_msg = f"Lexical Error at Line {line}, Position {position - line_start}: Invalid character '{error_char}'"
                errors.append(error_msg)
                
                token = Token(
                    type=TokenType.INVALID,
                    value=error_char,
                    position=position - line_start,
                    line=line
                )
                tokens.append(token)
                position += 1
        
        return {
            'tokens': [token.to_dict() for token in tokens],
            'errors':  errors,
            'total_tokens': len(tokens)
        }