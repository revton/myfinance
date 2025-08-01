"""
Validador de senha para o sistema de autenticação

Este módulo implementa validação robusta de senhas com políticas de segurança
para garantir que as senhas sejam fortes e seguras.
"""

import re
from typing import List, NamedTuple
from dataclasses import dataclass

@dataclass
class PasswordValidationResult:
    """Resultado da validação de senha"""
    is_valid: bool
    errors: List[str]
    score: int  # 0-100

class PasswordValidator:
    """Validador de senha com políticas de segurança"""
    
    def __init__(self):
        # Senhas comuns que devem ser rejeitadas
        self.common_passwords = {
            'password', '123456', '123456789', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey',
            '1234567890', '1234567', '12345678', '12345678910',
            'password1', 'password12', 'password1234', 'password12345',
            'admin123', 'admin1234', 'admin12345', 'admin123456',
            'user', 'user123', 'user1234', 'user12345', 'user123456',
            'test', 'test123', 'test1234', 'test12345', 'test123456',
            'guest', 'guest123', 'guest1234', 'guest12345', 'guest123456',
            'demo', 'demo123', 'demo1234', 'demo12345', 'demo123456',
            'temp', 'temp123', 'temp1234', 'temp12345', 'temp123456',
            'pass', 'pass123', 'pass1234', 'pass12345', 'pass123456',
            'login', 'login123', 'login1234', 'login12345', 'login123456',
            'welcome123', 'welcome1234', 'welcome12345', 'welcome123456',
            'letmein123', 'letmein1234', 'letmein12345', 'letmein123456',
            'monkey123', 'monkey1234', 'monkey12345', 'monkey123456',
            'qwerty123', 'qwerty1234', 'qwerty12345', 'qwerty123456',
            'abc123456', 'abc1234567', 'abc12345678', 'abc123456789',
            '123456789a', '123456789ab', '123456789abc', '123456789abcd',
            'a123456789', 'ab123456789', 'abc123456789', 'abcd123456789'
        }
        
        # Padrões de informações pessoais
        self.personal_info_patterns = [
            r'\b(joao|maria|jose|ana|pedro|julia|lucas|sophia|gabriel|isabella)\b',
            r'\b(silva|santos|oliveira|souza|rodrigues|ferreira|almeida|pereira|lima|gomes)\b',
            r'\b(brasil|brazil|sao paulo|rio de janeiro|minas gerais|bahia|parana|pernambuco)\b',
            r'\b(1990|1991|1992|1993|1994|1995|1996|1997|1998|1999|2000|2001|2002|2003|2004|2005)\b'
        ]
    
    def validate(self, password: str) -> PasswordValidationResult:
        """
        Valida uma senha de acordo com as políticas de segurança
        
        Args:
            password: Senha a ser validada
            
        Returns:
            PasswordValidationResult com resultado da validação
        """
        errors = []
        score = 0
        
        # Verificar comprimento mínimo
        if len(password) < 8:
            errors.append("A senha deve ter pelo menos 8 caracteres")
        else:
            score += 10
        
        # Verificar comprimento máximo
        if len(password) > 128:
            errors.append("A senha deve ter no máximo 128 caracteres")
        else:
            score += 5
        
        # Verificar letras maiúsculas
        if not any(c.isupper() for c in password):
            errors.append("A senha deve conter pelo menos uma letra maiúscula")
        else:
            score += 10
        
        # Verificar letras minúsculas
        if not any(c.islower() for c in password):
            errors.append("A senha deve conter pelo menos uma letra minúscula")
        else:
            score += 10
        
        # Verificar números
        if not any(c.isdigit() for c in password):
            errors.append("A senha deve conter pelo menos um número")
        else:
            score += 10
        
        # Verificar caracteres especiais
        special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        if not any(c in special_chars for c in password):
            errors.append("A senha deve conter pelo menos um caractere especial")
        else:
            score += 15
        
        # Verificar senhas comuns
        if password.lower() in self.common_passwords:
            errors.append("A senha é muito comum e não é segura")
        else:
            score += 20
        
        # Verificar informações pessoais
        if self._contains_personal_info(password):
            errors.append("A senha não deve conter informações pessoais")
        else:
            score += 10
        
        # Verificar caracteres sequenciais
        if self._has_sequential_chars(password):
            errors.append("A senha não deve conter sequências de caracteres")
        else:
            score += 5
        
        # Verificar caracteres repetidos
        if self._has_repeated_chars(password):
            errors.append("A senha não deve conter muitos caracteres repetidos")
        else:
            score += 5
        
        # Verificar complexidade geral
        if len(set(password)) < len(password) * 0.7:
            errors.append("A senha deve ter boa variedade de caracteres")
        else:
            score += 10
        
        # Ajustar score baseado no comprimento
        if len(password) >= 12:
            score += 10
        elif len(password) >= 10:
            score += 5
        
        # Limitar score máximo
        score = min(score, 100)
        
        return PasswordValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            score=score
        )
    
    def _contains_personal_info(self, password: str) -> bool:
        """Verifica se a senha contém informações pessoais"""
        password_lower = password.lower()
        
        for pattern in self.personal_info_patterns:
            if re.search(pattern, password_lower):
                return True
        
        return False
    
    def _has_sequential_chars(self, password: str) -> bool:
        """Verifica se a senha contém sequências de caracteres"""
        # Sequências numéricas
        numeric_sequences = ['123', '234', '345', '456', '567', '678', '789', '890',
                           '012', '1234', '2345', '3456', '4567', '5678', '6789', '7890']
        
        # Sequências alfabéticas
        alpha_sequences = ['abc', 'bcd', 'cde', 'def', 'efg', 'fgh', 'ghi', 'hij',
                          'ijk', 'jkl', 'klm', 'lmn', 'mno', 'nop', 'opq', 'pqr',
                          'qrs', 'rst', 'stu', 'tuv', 'uvw', 'vwx', 'wxy', 'xyz']
        
        password_lower = password.lower()
        
        for seq in numeric_sequences + alpha_sequences:
            if seq in password_lower:
                return True
        
        return False
    
    def _has_repeated_chars(self, password: str) -> bool:
        """Verifica se a senha contém muitos caracteres repetidos"""
        if len(password) < 4:
            return False
        
        # Verificar repetição de 3 ou mais caracteres consecutivos
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        
        # Verificar se mais de 50% dos caracteres são repetidos
        char_counts = {}
        for char in password:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        max_repetition = max(char_counts.values())
        if max_repetition > len(password) * 0.5:
            return True
        
        return False
    
    def get_strength_description(self, score: int) -> str:
        """Retorna descrição da força da senha baseada no score"""
        if score >= 80:
            return "Muito forte"
        elif score >= 60:
            return "Forte"
        elif score >= 40:
            return "Média"
        elif score >= 20:
            return "Fraca"
        else:
            return "Muito fraca"
    
    def suggest_improvements(self, password: str) -> List[str]:
        """Sugere melhorias para a senha"""
        suggestions = []
        
        if len(password) < 8:
            suggestions.append("Adicione mais caracteres para atingir pelo menos 8")
        
        if not any(c.isupper() for c in password):
            suggestions.append("Adicione pelo menos uma letra maiúscula")
        
        if not any(c.islower() for c in password):
            suggestions.append("Adicione pelo menos uma letra minúscula")
        
        if not any(c.isdigit() for c in password):
            suggestions.append("Adicione pelo menos um número")
        
        special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        if not any(c in special_chars for c in password):
            suggestions.append("Adicione pelo menos um caractere especial")
        
        if len(password) < 12:
            suggestions.append("Considere usar uma senha mais longa (12+ caracteres)")
        
        if self._contains_personal_info(password):
            suggestions.append("Evite usar informações pessoais como nome, data de nascimento, etc.")
        
        if self._has_sequential_chars(password):
            suggestions.append("Evite sequências como '123', 'abc', etc.")
        
        if self._has_repeated_chars(password):
            suggestions.append("Evite repetir caracteres muitas vezes")
        
        return suggestions 