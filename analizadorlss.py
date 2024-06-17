from flask import Flask, request, render_template_string
import re
import ply.lex as lex

app = Flask(__name__)

# Actualización de tokens para el analizador léxico
tokens = {
    'PR': r'\b(Inicio|cadena|proceso|si|ver|Fin)\b',
    'ID': r'\b[a-zA-Z_][a-zA-Z_0-9]*\b',
    'NUM': r'\b\d+\b',
    'SYM': r'[;{}()\[\]=<>!+-/*]',
    'ERR': r'.'
}

# Lista de nombres de tokens. Debe incluir al menos un token.



def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


# Plantilla HTML para mostrar resultados
html_template = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    body {
      font-family: 'Roboto', sans-serif;
      background-color: #f5f5f5;
      margin: 0;
      padding: 20px;
      color: #333;
    }
    h1, h2 {
      text-align: center;
      color: #4CAF50;
      margin-bottom: 20px;
    }
    form {
      background-color: #fff;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      max-width: 800px;
      margin: 0 auto 20px auto;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    textarea {
      width: 100%;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-family: 'Roboto', sans-serif;
      font-size: 16px;
    }
    input[type="submit"] {
      background-color: #4CAF50;
      color: white;
      padding: 14px 20px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      transition: background-color 0.3s ease;
      font-size: 16px;
    }
    input[type="submit"]:hover {
      background-color: #45a049;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    table, th, td {
      border: 1px solid #ddd;
    }
    th, td {
      padding: 12px;
      text-align: left;
    }
    th {
      background-color: #4CAF50;
      color: white;
    }
    tr:nth-child(even) {
      background-color: #f2f2f2;
    }
    tr:hover {
      background-color: #ddd;
    }
    .container {
      max-width: 800px;
      margin: 0 auto;
    }
  </style>
  <title>Analizador</title>
</head>
<body>
  <div class="container">
    <h1>Analizador</h1>
    <form method="post">
      <textarea name="code" rows="10" cols="50">{{ code }}</textarea><br>
      <input type="submit" value="Analizar">
    </form>
    <div>
      <h2>Analizador Léxico</h2>
      <table>
        <tr>
          <th>Tokens</th><th>PR</th><th>ID</th><th>Números</th><th>Símbolos</th><th>Error</th>
        </tr>
        {% for row in lexical %}
        <tr>
          <td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>{{ row[2] }}</td><td>{{ row[3] }}</td><td>{{ row[4] }}</td><td>{{ row[5] }}</td>
        </tr>
        {% endfor %}
        <tr>
          <td>Total</td><td>{{ total['PR'] }}</td><td>{{ total['ID'] }}</td><td>{{ total['NUM'] }}</td><td>{{ total['SYM'] }}</td><td>{{ total['ERR'] }}</td>
        </tr>
      </table>
    </div>
    <div>
      <h2>Analizador Sintáctico y Semántico</h2>
      <table>
        <tr>
          <th>Sintáctico</th><th>Semántico</th>
        </tr>
        <tr>
          <td>{{ syntactic }}</td><td>{{ semantic }}</td>
        </tr>
      </table>
    </div>
  </div>
</body>
</html>
'''

def analyze_lexical(code):
    results = {'PR': 0, 'ID': 0, 'NUM': 0, 'SYM': 0, 'ERR': 0}
    rows = []
    for line in code.split('\n'):
        row = [''] * 6
        for token_name, token_pattern in tokens.items():
            for match in re.findall(token_pattern, line):
                results[token_name] += 1
                row[list(tokens.keys()).index(token_name)] = 'x'
        rows.append(row)
    return rows, results

# Mejoras en el análisis sintáctico y semántico



def analyze_syntactic(code):
  corrected_code = code
  errors = []

  # Verificar la estructura de "Inicio" y "Fin"
  if not code.startswith("Inicio;"):
    errors.append("El código debe comenzar con 'Inicio;'.")
  if not code.endswith("Fin;"):
    errors.append("El código debe terminar con 'Fin;'.")

  # Verificar la estructura de bloques y sentencias
  if "proceso;" not in code:
    errors.append("Falta la declaración de 'proceso;'.")
  if "si (" in code and not re.search(r"si\s*\(.+\)\s*\{", code):
    errors.append("Estructura incorrecta de 'si'. Debe ser 'si (condición) {'.")
  if "{" in code and "}" not in code:
    errors.append("Falta cerrar un bloque con '}'.")
  if "}" in code and "{" not in code:
    errors.append("Falta abrir un bloque con '{'.")

  # Dividir el código en líneas y verificar el punto y coma
  lines = code.split('\n')
  for i, line in enumerate(lines):
    # Ignorar líneas que no requieren punto y coma
    if line.strip() and not line.strip().endswith(';') and not line.strip().endswith('{') and not line.strip().endswith('}') and "si (" not in line and "Inicio;" not in line and "Fin;" not in line:
      errors.append(f"Falta punto y coma al final de la línea {i + 1}.")

  if not errors:
    return "Sintaxis correcta", corrected_code
  else:
    return " ".join(errors), corrected_code
  
  
  corrected_code = code
  errors = []

  # Verificar la estructura de "Inicio" y "Fin"
  if not code.startswith("Inicio;"):
    errors.append("El código debe comenzar con 'Inicio;'.")
  if not code.endswith("Fin;"):
    errors.append("El código debe terminar con 'Fin;'.")

  # Verificar la estructura de bloques y sentencias
  if "proceso;" not in code:
    errors.append("Falta la declaración de 'proceso;'.")
  if "si (" in code and not re.search(r"si\s*\(.+\)\s*\{", code):
    errors.append("Estructura incorrecta de 'si'. Debe ser 'si (condición) {'.")
  if "{" in code and "}" not in code:
    errors.append("Falta cerrar un bloque con '}'.")
  if "}" in code and "{" not in code:
    errors.append("Falta abrir un bloque con '{'.")

  if not errors:
    return "Sintaxis correcta", corrected_code
  else:
    return " ".join(errors), corrected_code

def analyze_semantic(code):
  errors = []
  corrected_code = code
  declared_variables = set()  # Paso 1: Registro de variables declaradas

  # Identificar y almacenar los tipos de las variables
  for var_declaration in re.findall(r"\b(cadena|entero)\s+(\w+)\s*=", code):
    _, var_name = var_declaration
    declared_variables.add(var_name)  # Almacenar variables declaradas

  # Verificar la asignación correcta de valores a variables
  # (Código existente)

  # Verificar comparaciones lógicas
  logical_checks = re.findall(r"si\s*\((.+)\)", code)
  for check in logical_checks:
    match = re.search(r"(\w+)\s*(==|!=|>|<|>=|<=)\s*(\w+|\".*\"|\d+)", check)
    if match:
      left_var, _, right_var = match.groups()
      # Verificar si las variables han sido declaradas
      if left_var not in declared_variables and not left_var.isdigit():
        errors.append(f"Error semántico: La variable '{left_var}' no ha sido declarada.")
      if right_var not in declared_variables and not right_var.replace('"', '').isdigit() and not right_var.startswith('"'):
        errors.append(f"Error semántico: La variable '{right_var}' no ha sido declarada.")
    else:
      errors.append(f"Error semántico en la condición 'si ({check})'. Formato incorrecto de comparación.")

  if not errors:
    return "Uso correcto de las estructuras semánticas", corrected_code
  else:
    return " ".join(errors), corrected_code

@app.route('/', methods=['GET', 'POST'])
def index():
    code = ''
    lexical_results = []
    total_results = {'PR': 0, 'ID': 0, 'NUM': 0, 'SYM': 0, 'ERR': 0}
    syntactic_result = ''
    semantic_result = ''
    corrected_code = ''
    if request.method == 'POST':
        code = request.form['code']
        lexical_results, total_results = analyze_lexical(code)
        syntactic_result, corrected_code = analyze_syntactic(code)
        semantic_result, corrected_code = analyze_semantic(corrected_code)
    return render_template_string(html_template, code=code, lexical=lexical_results, total=total_results, syntactic=syntactic_result, semantic=semantic_result, corrected_code=corrected_code)

if __name__ == '__main__':
    app.run(debug=True)