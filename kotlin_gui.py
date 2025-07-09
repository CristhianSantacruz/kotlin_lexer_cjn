# Primer avance Kotlin CJN GUI

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import threading
import os

COLOR_PRINCIPAL = "#9435f2"
COLOR_BACKGROUND = "#f2f2f2"
COLOR_INTEPRETE = "#d9d9d9"





class KotlinAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        img = Image.open("image/logo_kotlin.png")
        img = img.resize((50, 50))
        self.logo = ImageTk.PhotoImage(img)
        self.setup_ui()
        self.setup_styles()
        
    def setup_ui(self):
        self.root.title("KOTLIN CJN")
        self.root.geometry("1350x900")
        self.root.configure(bg="#f0f0f0")
        header_frame = tk.Frame(self.root, bg=COLOR_INTEPRETE, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame, 
            text="KOTLIN CJN", 
            font=("Arial", 44, "bold"), 
            fg="black",
            image=self.logo,
            compound=tk.LEFT,
            bg=COLOR_INTEPRETE
        )
        header_label.pack(expand=True)

        divider = tk.Frame(self.root, bg="black", height=2)
        divider.pack(fill=tk.X)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=COLOR_BACKGROUND)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para código y resultado
        content_frame = tk.Frame(main_frame, bg=COLOR_INTEPRETE)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo - Editor de código
        left_panel = tk.Frame(content_frame, bg=COLOR_INTEPRETE)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        
        
        
      
        editor_frame = tk.Frame(left_panel, bg="white", relief=tk.SUNKEN, bd=1)
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        
        self.line_numbers = tk.Text(
            editor_frame,
            width=4,
            padx=5,
            pady=5,
            bg="#f8f8f8",
            fg="#666666",
            state=tk.DISABLED,
            font=("Consolas", 10)
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Editor de código
        self.code_editor = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.NONE,
            font=("Consolas", 11),
            bg=COLOR_INTEPRETE,
            fg="#333333",
            insertbackground="#333333",
            selectbackground="#3399ff",
            selectforeground="white",
            padx=5,
            pady=5
        )
        self.code_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Vincular eventos para actualizar números de línea
        self.code_editor.bind('<KeyRelease>', self.update_line_numbers)
        self.code_editor.bind('<Button-1>', self.update_line_numbers)
        self.code_editor.bind('<MouseWheel>', self.update_line_numbers)
        
        # Panel derecho - Resultados
        right_panel = tk.Frame(content_frame, bg="#f0f0f0", width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        right_panel.pack_propagate(False)
        
        # Notebook para pestañas de resultados
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=(0, 0), pady=(0, 10))
        
        # Pestaña de Tokens
        tokens_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tokens_frame, text="🔤 Tokens")
        
        self.tokens_output = scrolledtext.ScrolledText(
            tokens_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="white",
            fg="#333333",
            state=tk.DISABLED
        )
        self.tokens_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña de Errores
        errors_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(errors_frame, text="⚠️ Errores")
        
        self.errors_output = scrolledtext.ScrolledText(
            errors_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#fff5f5",
            fg="#d32f2f",
            state=tk.DISABLED
        )
        self.errors_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña de AST
        ast_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(ast_frame, text="🌳 AST")
        
        self.ast_output = scrolledtext.ScrolledText(
            ast_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="white",
            fg="#333333",
            state=tk.DISABLED
        )
        self.ast_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña de Ejecución
        execution_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(execution_frame, text="▶️ Ejecución")
        
        self.execution_output = scrolledtext.ScrolledText(
            execution_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg=COLOR_INTEPRETE,
            fg="#000000",
            state=tk.DISABLED
        )
        self.execution_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
     
        button_frame = tk.Frame(right_panel, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=(0, 0))
        
      
        self.run_btn = tk.Button(
            button_frame,
            text="ANALIZAR",
            command=self.run_analysis,
            bg=COLOR_PRINCIPAL,
            fg="white",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT,
            borderwidth=0
        )
        self.run_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        self.clear_btn = tk.Button(
                button_frame,
                text="LIMPIAR",
                command=self.clear_all,
                bg=COLOR_BACKGROUND,
                fg="black",
                font=("Arial", 12, "bold"),
                padx=30,
                pady=10,
                cursor="hand2",
                relief=tk.FLAT,
                borderwidth=0
            )
        self.clear_btn.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
       
        
 
        self.status_bar = tk.Label(
            self.root,
            text="Listo para analizar código Kotlin",
            bg="#e0e0e0",
            fg="#333333",
            font=("Arial", 9),
            anchor=tk.W,
            padx=10,
            pady=5
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        
        self.set_example_code()
        self.update_line_numbers()
        

        
    def setup_styles(self):
        """Configurar estilos adicionales"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores del notebook
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', padding=[20, 8])
        
    def update_line_numbers(self, event=None):
        """Actualizar números de línea"""
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        
        lines = self.code_editor.get(1.0, tk.END).split('\n')
        line_numbers = '\n'.join(str(i) for i in range(1, len(lines)))
        
        self.line_numbers.insert(1.0, line_numbers)
        self.line_numbers.config(state=tk.DISABLED)
        
    def set_example_code(self):
        """Establecer código de ejemplo"""
        example_code = """fun main() {
   
}"""
        self.code_editor.insert(1.0, example_code)
        
    def clear_all(self):
        """Limpiar todo el contenido"""
        self.code_editor.delete(1.0, tk.END)
        self.clear_outputs()
        self.update_line_numbers()
        self.status_bar.config(text="Contenido limpiado")
        
    def clear_outputs(self):
        """Limpiar todas las salidas"""
        outputs = [self.tokens_output, self.errors_output, self.ast_output, self.execution_output]
        for output in outputs:
            output.config(state=tk.NORMAL)
            output.delete(1.0, tk.END)
            output.config(state=tk.DISABLED)
            
    def run_analysis(self):
        """Ejecutar análisis en hilo separado"""
        def analysis_thread():
            try:
                self.run_btn.config(state=tk.DISABLED)
                self.status_bar.config(text="Analizando código...")
                
                code = self.code_editor.get(1.0, tk.END).strip()
                
                if not code:
                    messagebox.showwarning("Advertencia", "Por favor ingresa código para analizar")
                    return
                
                self.clear_outputs()
                
               
                self.run_lexical_analysis(code)
                self.run_syntax_semantic_analysis(code)
                
                self.status_bar.config(text="Análisis completado")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error durante el análisis: {str(e)}")
                self.status_bar.config(text="Error en el análisis")
            finally:
                self.run_btn.config(state=tk.NORMAL)
                
        threading.Thread(target=analysis_thread, daemon=True).start()
        
    def run_lexical_analysis(self, code):
        """Ejecutar análisis léxico"""
        try:
            # Simulación del análisis léxico (hasta que se conecten los módulos)
            self.tokens_output.config(state=tk.NORMAL)
            self.tokens_output.insert(tk.END, "=== ANÁLISIS LÉXICO ===\n\n")
            self.tokens_output.insert(tk.END, "Módulo lexer aún no conectado.\n")
            self.tokens_output.insert(tk.END, "Código a analizar:\n")
            self.tokens_output.insert(tk.END, code[:200] + "..." if len(code) > 200 else code)
            self.tokens_output.config(state=tk.DISABLED)
            
        except Exception as e:
            self.tokens_output.config(state=tk.NORMAL)
            self.tokens_output.insert(tk.END, f"Error en análisis léxico: {str(e)}")
            self.tokens_output.config(state=tk.DISABLED)
            
    def run_syntax_semantic_analysis(self, code):
        """Ejecutar análisis sintáctico y semántico"""
        try:
            # Simulación del análisis sintáctico/semántico
            self.errors_output.config(state=tk.NORMAL)
            self.errors_output.insert(tk.END, "=== ANÁLISIS SINTÁCTICO Y SEMÁNTICO ===\n\n")
            self.errors_output.insert(tk.END, "Módulos parser aún no conectados.\n")
            self.errors_output.insert(tk.END, "Interfaz funcionando correctamente")
            self.errors_output.config(state=tk.DISABLED)
            
            # AST simulado
            self.ast_output.config(state=tk.NORMAL)
            self.ast_output.insert(tk.END, "=== ÁRBOL SINTÁCTICO ABSTRACTO ===\n\n")
            self.ast_output.insert(tk.END, "AST se generará cuando se conecte el parser")
            self.ast_output.config(state=tk.DISABLED)
            
            # Ejecución simulada
            self.execution_output.config(state=tk.NORMAL)
            self.execution_output.insert(tk.END, "=== SALIDA DE EJECUCIÓN ===\n\n")
            self.execution_output.insert(tk.END, "Esperando conexión con el intérprete...")
            self.execution_output.config(state=tk.DISABLED)
            
        except Exception as e:
            self.errors_output.config(state=tk.NORMAL)
            self.errors_output.insert(tk.END, f"Error en análisis sintáctico/semántico: {str(e)}")
            self.errors_output.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = KotlinAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()