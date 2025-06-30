// PRUEBA DE TIPOS DE DATOS
// =============================
// Correcto
val edad: Int = 20    
// Incorrecto: tipo incompatible                 
val edadTexto: Int = "veintecinco"     

// Correcto
val activo: Boolean = true     
// Incorrecto: tipo no válido (String)         
val activoTexto: Boolean = "true"      

// PRUEBA DE RETORNO DE FUNCIONES
// =============================
// Correcto
fun obtenerNombre(): String {
    return "Carlos"                    
}

// Incorrecto: se esperaba un Int
fun obtenerEdad(): Int {
    return "veinticinco"              
}

// Correcto: sin retorno explícito
fun saludar() {                        
    println("Hola")
}

// Incorrecto: función sin retorno no debe devolver valor
fun despedir(): Unit {
    return "Adiós"                    
}