fun contarClavesImportantes(mapa: Map<String, Int>): Int {
    var contador = 0

    for (clave in mapa.keys) {
        if ((clave.length > 3 && clave != "omit") || mapa[clave]!! > 5) {
            contador = contador + 1
        }
    }

    return contador
}

fun main() {
    val datos = mapOf(
        "edad" to 10,
        "ok" to 2,
        "omit" to 9,
        "nombre" to 1
    )

    val resultado = contarClavesImportantes(datos)
    println("Cantidad de claves importantes: $resultado")
}
