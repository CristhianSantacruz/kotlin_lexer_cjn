fun main() {
    val numeros = listOf(13, 45, 2, 9, 33, 58, 76, 101, 20)

    if (numeros.isEmpty()) {
        println("La lista está vacía.")
    } else {
        val sumaTotal = numeros.sum()
        println("La suma total es: $sumaTotal")

        if (sumaTotal % 2 == 0) {
            println("La suma es par.")
        } else {
            println("La suma es impar.")
        }

        val mayoresA30 = numeros.filter { it > 30 }
        println("Numeros mayores a 30: $mayoresA30")

        if (numeros.contains(33)) {
            println("33 está en la lista.")
        } else {
            println("33 no esta en la lista.")
        }
    }
}
