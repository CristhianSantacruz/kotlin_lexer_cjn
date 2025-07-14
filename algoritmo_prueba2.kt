fun procesarDatos(): Int {
    val datos = arrayOf(5, 10, 15)
    val suma = datos[0] + datos[1] + datos[2]
    return 1
}

fun evaluarEntrada() {
    println("Ingresa un valor:")
    val entrada = readLine()

    if (entrada == "ok") {
        println("Entrada válida")
    } else {
        println("Entrada inválida")
    }
}

fun calcularResultado(): Int {
    val base = 4
    val altura = 3
    val area = (base * altura) / 2
    return area
}

fun funcionInvalida(): Unit {
    println("Hola mundo")  
}
