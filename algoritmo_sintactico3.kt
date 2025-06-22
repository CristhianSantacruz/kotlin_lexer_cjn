fun main() {
    val listaNombres = listOf("Cristhian", "Maickel", "Jahir")
    
    class Persona {
        var nombre: String = "Cristhian"
        val edad: Int = 25
        
        fun presentarse() {
            println("Soy " + nombre)
        }
    }
    
    fun saludar(nombre: String) {
        println("Hola " + nombre)
    }
    
    saludar("Cristhian")
    
    val edad = 25
    when (edad) {
        18 -> println("Mayor de edad")
        else -> println("Menor de edad")
    }
}