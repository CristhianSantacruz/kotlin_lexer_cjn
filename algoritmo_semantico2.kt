fun main() {
    // =======================================================
    // 3ERA REGLA: Uso de variables antes de ser declaradas
    // =======================================================

    println(x) // Error: variable usada antes de ser declarada

    val x = 10 // Declaración válida de variable

    println(x) // Uso correcto después de la declaración


    // =======================================================
    // 1ERA REGLA: Operaciones entre tipos compatibles
    // =======================================================

    val a = 5         // Int
    val b = 3.5       // Double
    val bandera = true // Boolean

    val sumaCorrecta = a + b       // Int + Double -> válido
    val sumaTexto = "Hola" + "!"   // String + String -> válido
    val sumaInvalida = bandera + a // Boolean + Int -> inválido


    // =======================================================
    // 2DA REGLA: Comparaciones entre tipos compatibles
    // =======================================================

    val comparacionCorrecta = a > 2              // Int > Int(valido)
    val comparacionTexto = "Hola" == "Hola"      // String == String (valido)
    val comparacionInvalida = "Hola" > bandera   // String > Boolean (inválido)

}
