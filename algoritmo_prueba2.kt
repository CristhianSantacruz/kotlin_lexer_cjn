fun calcular() {
    val numeros = arrayOf(10, 20, 30)
}

fun verificarEdad(nombre: String, edad: Int): Boolean {
    if (edad >= 18 && edad <= 60) {
        println(nombre + " está en edad laboral")
        return true
    } else {
        println(nombre + " no está en edad laboral")
        return false
    }
}