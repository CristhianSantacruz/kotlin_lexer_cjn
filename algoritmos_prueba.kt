fun mostrarMensaje(nombre: String) {
    println("Bienvenido " + nombre)
}

fun main() {
    val listaNombres = listOf("Ana", "Luis", "Pedro")

    for (nombre in listaNombres) {
        mostrarMensaje(nombre)
    }

    val numero = 1

    when (numero) {
        1 {
            println("Es uno")
        }
        2 {
            println("Es dos")
        }
        else {
            println("Otro número")
        }
    }
}