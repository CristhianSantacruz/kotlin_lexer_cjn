fun main() {
    // Declaraciones de variables
    val nombre: String = "Carlos"
    var edad: Int = 20
    val activo: Boolean = true
    val notas = listOf(8.5, 9.0, 7.5)
    val arreglo = arrayOf("Lunes", "Martes", "Miércoles")
    val datos = mapOf("clave1" to 1, "clave2" to 2)

    // Comentario de línea
    println("Bienvenido, $nombre") // Saludo personalizado

    /* Comentario de bloque
       Evaluación de edad */
    if (edad >= 18) {
        println("Es mayor de edad")
    } else {
        println("Es menor de edad")
    }

    // Uso de for
    for (nota in notas) {
        println("Nota: $nota")
    }

    // Uso de when
    val dia = "Lunes"
    when (dia) {
        "Lunes" -> println("Inicio de semana")
        "Viernes" -> println("Fin de semana")
        else -> println("Día normal")
    }

    // Uso de operadores
    val promedio = (notas[0] + notas[1] + notas[2]) / 3
    val aprobado = promedio >= 7.0 && activo

    // Impresión de resultados
    println("Promedio: $promedio")
    println("¿Aprobado?: $aprobado")

    // Llamada a función
    mostrarMensaje(nombre, promedio)
}

// Función con parámetros y retorno
fun mostrarMensaje(usuario: String, promedio: Double): String {
    val mensaje = "$usuario, tu promedio es $promedio"
    println(mensaje)
    return mensaje
}
