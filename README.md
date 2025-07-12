# KotlinCJN - Analizador Léxico, Sintáctico y Semántico en Python

Este proyecto implementa un **analizador completo (léxico, sintáctico y semántico)** para un lenguaje inspirado en Kotlin, desarrollado con **PLY (Python Lex-Yacc)**. Permite verificar la estructura del código fuente, detectar errores léxicos, sintácticos y semánticos, e incluso ejecutar ciertos fragmentos de código válidos.

---

## 🧑‍💻 Autores

- Cristhian Santacruz Gorozabel
- Noelia Saltos Hernández  
- Jahir Díaz Cedeño  


---

## 📦 Estructura del 
├── kotlin_lexer.py # Analizador léxico (tokens y expresiones regulares)
├── kotlin_parser.py # Parser sintáctico y semántico
├── kotlin_gui.py # Interfaz gráfica (GUI)
├── algoritmo.kt # Archivo de prueba de código Kotlin
├── logs/

---

## 🛠️ Requisitos

- Python 3.x  
- PLY (Python Lex-Yacc)

Instalación de PLY:

pip install ply

## Ejecuta la interfaz gráfica:

python kotlin_gui.py

## Carga el archivo .kt con tu algoritmo (ej. algoritmo.kt), presiona el botón "Analizar" y verás los resultados organizados en pestañas:
-Tokens léxicos
-Errores sintácticos
-Errores semánticos
-AST y salida de ejecución
