fun main() {
    var intentos = 0
    val maxIntentos = 3
    val usuarioRegistrado = "admin"
    val contrasenaRegistrada: String? = "1234"

    while (intentos < maxIntentos) {
        val usuarioIngresado = "admin" // Simulado
        val contrasenaIngresada: String? = "1234"

        if (usuarioIngresado == usuarioRegistrado && contrasenaIngresada == contrasenaRegistrada) {
            println("Acceso concedido")
            mostrarMenu()
            break
        } else {
            println("Credenciales incorrectas")
            intentos += 1
            continue
        }
    }

    if (intentos == maxIntentos) {
        println("Demasiados intentos fallidos. Acceso denegado.")
    }
}

// Menú de operaciones
fun mostrarMenu() {
    val productos = arrayOf("Leche", "Pan", "Huevos")
    val stock = arrayOf(5, 2, 0)

    for (i in productos.indices) {
        val disponible = stock[i]
        val nombre = productos[i]

        // Null safety aplicada (simulada)
        val estado: String? = if (disponible > 0) "Disponible" else null
        val mensaje = estado ?: "Sin stock"

        println("$nombre -> $mensaje")
    }

    // Función con retorno
    val total = calcularTotal(stock)
    println("Total de productos en stock: $total")
}

// Suma de stock total
fun calcularTotal(stock: Array<Int>): Int {
    var suma = 0
    for (cantidad in stock) {
        suma += cantidad
    }
    return suma
}
