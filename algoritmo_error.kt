fun obtenerEdad(nombre: String): Int {
    val edad = 30

    if (nombre == "Lucia") {
        return "treinta"
    }

    return edad
}

fun main() {
    val resultado = obtenerEdad("Lucia")
    println("Edad reportada: " + resultado)
}
