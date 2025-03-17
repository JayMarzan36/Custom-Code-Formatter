import json, re, os

class token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class tokenizer:
    def __init__(self, lang="generic"):
        self.lang = lang
        
        TOKENSPATH = os.path.join(os.path.dirname(__file__), "tokens.json")
        
        tokens = json.load(TOKENSPATH)
        
        self.keywords = tokens.get("lang")
        
        self.tokenSpec = [
            ("number", r"\d+(\.\d+)?"),
            ("string", f'"[^"]*"|\'[^\']*\''),
            ("identifier", r"[a-zA-Z_]\w*"),
            ("operator", r"[+\-*/=<>!]+"),
            ("delimiter", r"[(){}[\],;]"),
            ("whitespace", r"\s+"),
            ("comment", r"//.*|/\*[\s\S]*?\*/")
        ]
        
        self.tokenRegex = re.compile("|".join(f"?P<{name}>{pattern}") for name, pattern in self.tokenSpec)
    
    def tokenize(self, code):
        tokens = []
        
        for match in self.tokenRegex.finditer(code):
            kind = match.lastgroup
            
            value = match.group()
            
            if kind == "whitespace":
                continue
            
            elif kind == "identifier" and value in self.keywords.get(self.lang, set()):
                kind = "keyword"
            
            tokens.append(token(kind, value))
        
        return tokens