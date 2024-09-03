numbers = '123456789'
operators = '/*-+'


def validateCharacters(expression):
	for character in expression:
		# Concatena los caracteres validos primero para comprobar que no hay caracteres invalidos
		if character not in numbers+operators+'()[]':
			# Regresa verdadero si encuentra que contiene algun caracter inválido
			return True, character
	return False, None

def is_balanced(expression):
    stack = []
    # Diccionario que contiene los caracteres para abrir y cerrar
    matching_bracket = {')': '(', ']': '['}
    
    for char in expression:
        if char in '([':  # Si es un caracter para abrir lo agrega a la pila
            stack.append(char)
        elif char in ')]':  # Si es un caracter para cerrar 
			# Lo saca de la pila y verifica si es igual a su valor correspondiente en el diccionario
            # En caso de que haya un caracter ] cuando deberia ser ) o viceversa no lo saca de la pila
            # Tambien regresa falso si se encuentra } o ) cuando la pila esta vacía (lo que significa que se abrio nunca parentesis)
            if not stack or stack.pop() != matching_bracket[char]:
                return False
    # Si quedan caracteres dentro de la pila quiere decir que no se encontro un ) o ] correspondiente
    return len(stack) == 0

expression = '5+5([5+3])'
found_invalid, invalid_character = validateCharacters(expression)

if found_invalid:
	print('Caracter inválido encontrado en la expresión. Caracter encontrado: ',invalid_character)
else:
	print('Expresión válidos contra caracteres inválidos.')
	is_balanced = is_balanced(expression)

	if is_balanced:
		print('La ecuación esta balanceada.')
	else:
		print('La ecuación no esta balanceada. Revise los parentesis y llaves de su ecuación')