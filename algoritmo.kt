// Función con retorno correcto
fun duplicar(x: Int): Int {
    return x * 2
}

// Función sin retorno (Unit)
fun mostrarMensaje(msg: String) {
    println("Mensaje: " + msg)
}

fun main() {
    var nombre = "Kotlin"
    val edad = 10
    val activo = true
    val promedio = 8.75

    println("Bienvenido " + nombre)
    println("Edad + 2 = " + (edad + 2))
    println("Promedio x 2 = " + (promedio * 2))
    println("Estado: " + activo)

    val numeros = listOf(1, 2, 3, 4)
    for (num in numeros) {
        println("Número: " + num)
    }

    val resultado = duplicar(5)
    println("Duplicado: " + resultado)

    mostrarMensaje("Hola desde función")
}
