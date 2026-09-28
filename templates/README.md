# Plantillas de funciones, STL y programación genérica

## Marco teórico

### 1. ¿Qué se entiende por plantillas de funciones?

Una plantilla de función es una descripción parametrizada de una función. En vez de escribir una implementación distinta para cada tipo de dato, se indican uno o más parámetros de tipo y el compilador genera la versión concreta cuando la función se usa con esos tipos. Esto permite reutilizar código conservando la comprobación estática de tipos.

### 2. ¿Qué son las plantillas de funciones? Ejemplo

Son funciones genéricas cuyos tipos se determinan al deducir los argumentos de una llamada o al indicarlos explícitamente. Por ejemplo, esta plantilla intercambia dos valores del mismo tipo:

```cpp
template <typename T>
void intercambiar(T& primero, T& segundo) {
    T temporal = primero;
    primero = segundo;
    segundo = temporal;
}
```

Al llamar `intercambiar(numero1, numero2)`, el compilador deduce `T` a partir de los argumentos. La biblioteca estándar ofrece `std::swap` para esta operación.

### 3. ¿Qué son las plantillas de clases? Ejemplo

Una plantilla de clase permite definir una clase que trabaja con distintos tipos. El tipo se especifica al crear el objeto:

```cpp
template <typename T>
class Caja {
public:
    explicit Caja(T valor) : valor_(valor) {}

    const T& obtener() const {
        return valor_;
    }

private:
    T valor_;
};

Caja<int> cajaDeEntero(42);
Caja<double> cajaDecimal(3.5);
```

En el programa de [`main.cpp`](./main.cpp) se incluye una especialización de `Caja` para `bool`.

### 4. ¿Qué función cumple la especialización de plantillas?

La especialización permite ofrecer una implementación adaptada para un tipo o conjunto de tipos que necesita un tratamiento diferente. La versión general sigue atendiendo los demás tipos. Puede ser total (para una combinación concreta de tipos) o parcial (para una familia de combinaciones, en plantillas de clases y variables).

La especialización debe responder a una necesidad real: por ejemplo, una representación más adecuada o un comportamiento específico. No se debe confundir con la sobrecarga de funciones, que elige entre funciones distintas mediante resolución de sobrecargas.

## STL y programación genérica

La STL (Standard Template Library, integrada en la biblioteca estándar de C++) proporciona contenedores, iteradores y algoritmos genéricos. Por ejemplo, `std::vector<T>` almacena elementos de un tipo y `std::sort` ordena un rango usando iteradores. Estos componentes pueden reutilizarse con diferentes tipos que cumplan los requisitos de sus operaciones.

El ejemplo de `main.cpp` usa `std::vector<int>` y `std::sort`, además de las plantillas escritas para esta práctica.

## Marco práctico

### Función `menor` para dos argumentos del mismo tipo

La plantilla `menor<T>` recibe dos referencias constantes de un único tipo `T`, compara los valores con `<` y devuelve una referencia constante al menor:

```cpp
template <typename T>
constexpr const T& menor(const T& primero, const T& segundo) {
    return (segundo < primero) ? segundo : primero;
}
```

El programa comprueba llamadas con `int`, `double` y `float`, incluidas:

```cpp
menor(2, 3) == 2
menor(6.0, 4.0) == 4.0
```

### Argumentos de tipos diferentes

Con un solo parámetro de plantilla, ambos argumentos deben permitir deducir el mismo `T`. Por eso, `menor(2, 3.0)` no compila: la deducción encuentra `int` para el primer argumento y `double` para el segundo, y no hay un único tipo `T`.

Para aceptar dos tipos se necesitan dos parámetros de plantilla. En el ejemplo se devuelve `std::common_type_t<A, B>`, el tipo común que define la biblioteca estándar para ambos argumentos:

```cpp
template <typename A, typename B>
constexpr std::common_type_t<A, B>
menor_entre_tipos(const A& primero, const B& segundo) {
    return (segundo < primero) ? segundo : primero;
}
```

Por ejemplo, `menor_entre_tipos(2, 3.0)` compila y devuelve un `double`. Este diseño requiere que exista un tipo común para los argumentos y que la comparación entre ellos con `<` sea válida.

### Compilar y ejecutar

Desde esta carpeta, con un compilador compatible con C++17:

```sh
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o templates
./templates
```

En Windows, el ejecutable generado puede iniciarse con `.\templates.exe`. Si se intenta compilar la llamada de tipos distintos usando `menor(2, 3.0)`, la compilación debe fallar por deducción incompatible de `T`; esa llamada se deja fuera del programa para que el ejemplo completo compile.

La salida del programa es:

```text
menor(2, 3) = 2
menor(6.0, 4.0) = 4
menor(1.5f, 2.5f) = 1.5
menor_entre_tipos(2, 3.0) = 2
Valores ordenados con std::sort: 1 2 3 4
```
