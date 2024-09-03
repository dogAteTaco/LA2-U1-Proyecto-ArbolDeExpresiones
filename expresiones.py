import sys
import tree_drawer

numbers = '123456789'
operators = '-+/*^'

# Clase de nodo para el arbol
class Node:
	def __init__(self, value, left_node = None, right_node = None):
		self.value = value
		self.left = left_node
		self.right = right_node
	def __str__(self):
		return f'({self.value}, {self.left},  {self.right})'
# Valida que solo se encuentren caracteres aceptables dentro de la ecuacion
def validateCharacters(expression):
	for character in expression:
		# Concatena los caracteres validos primero para comprobar que no hay caracteres invalidos
		if character not in numbers+operators+'()[]':
			# Regresa verdadero si encuentra que contiene algun caracter inválido
			return True, character
	return False, None

# Encuentra la posicion y el operando con menos valor dentro de la expresion
def find_less_weight(expression):
	operator_index = -1
	position = -1
	# recorre por numero de indice toda la expresión
	for character_index, current_character in enumerate(expression):
		# recorre los operadores en cuanto a peso uno a uno
		for i, operator in enumerate(operators):
			# compara si el caracter en la expresion es el operador actualmente en el ciclo
			if current_character == operator:
				# Si todavia no se a definido ninguna posicion de operador se toma el que sea
				if operator_index == -1:
					operator_index = i
					position = character_index
					# Si el primer operator que encuentra es la suma automaticamente acaba la búsqueda
					if operator_index == 0:
						return position,operator_index
				# Si ya habia uno se compara para ver si es un operador de menor peso
				elif operator_index> i:
					operator_index = i
					position = character_index
	# Se regresa la posicion en la expresion y el indice del operador
	# Si no se encontro ningun operador significa que la expresion no contiene operadores
	return position,operator_index

# Encuentra el parentesis más interno
def find_innermost_expression(expression):
    stack = []
    
    for i, char in enumerate(expression):
        if char in '([':
            stack.append(i)
        elif char in ')]':
            start_index = stack.pop()
            if not stack or expression[stack[-1]] in '([':
                # Regresa la expresion más interna 
                return expression[start_index + 1: i]
	# Si no encuentra parentesis en la expresion dada regresa None
    return None

# Busca si existe una expresion en parentesis dentro de la expresion dada
def find_parenthesis_expression(expression):
	stack = []
	innermost_expression = None
	start_index = -1
	end_index = -1
	for i, char in enumerate(expression):
		if char in '([':
			stack.append(i)  # Push the index of the opening bracket onto the stack
		elif char in ')]':
			start_index = stack.pop()  # Pop the last opening bracket index
			if not stack:  # If the stack is empty, this is the innermost expression
				innermost_expression = expression[start_index + 1: i]
				end_index = i
    
	return innermost_expression, start_index, end_index

# Verifica que el numero de parentesis y llaves, así como su orden sean correctos
def is_balanced(expression):
	# Se utiliza una pila para mantener el orden de los parentesis y llaves
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

def build_tree(expression):
    if not expression:
        return None

    # Find the position and index of the operator with the least weight
    position, index = find_less_weight(expression)
    
    # If no operator is found, return a leaf node with the operand
    if position == -1:
        return Node(expression)
    
    # Create a node for the operator
    root = Node(expression[position])
    
    # Recursively build the left and right subtrees
    root.left = build_tree(expression[:position])
    root.right = build_tree(expression[position + 1:])
    
    return root



def print_tree(node, level=0):
    if node is not None:
        print_tree(node.right, level + 1)
        print(' ' * 4 * level + '->', node.value)
        print_tree(node.left, level + 1)

def validate_expression():
	# Realiza las validaciones
	if found_invalid:
		print(f'Caracter inválido encontrado en la expresión. Caracter encontrado: {invalid_character}')
		sys.exit()
	else:
		print('Expresión válidos contra caracteres inválidos.')
		
	expression_is_balanced = is_balanced(expression)

	if expression_is_balanced:
		print('La ecuación esta balanceada.')
	else:
		print('La ecuación no esta balanceada. Revise los parentesis y llaves de su ecuación')
		sys.exit()
# Se declara la expresion a evaluar
expression = '2*4-1(5[7+3]+2)'
expression = '2*4^5-6/32-78'
found_invalid, invalid_character = validateCharacters(expression)

print(find_less_weight(expression))
less_weight_index, operator_index = find_less_weight(expression)

root_node = Node(operators[operator_index])
print(f'Nodo raiz: {root_node}')

current_left = root_node.left
current_right = root_node.right
current_node = root_node

inner_expression = expression[0:less_weight_index]
while current_left != None:
	inner_expression = expression[0:less_weight_index]
	print(f'current inner expression: {inner_expression}')
	while inner_expression != None:
		inner_expression, start_index, end_index = find_parenthesis_expression(inner_expression)
		print(f'{inner_expression}')
		current_left = inner_expression

print(root_node)

tree_root = build_tree(expression)

print("Expression Tree:")
print_tree(tree_root)
# tree_drawer.plot_tree(tree_root)

tree_drawer.show_tree(tree_root)
