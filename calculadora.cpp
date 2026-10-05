#include <iostream>
#include <stdexcept>
#include <limits>
#include <string>

// ============================================================================
// 1. MODELO (Lógica de Dominio / Ecuación)
// Responsabilidad (Information Holder / Service Provider):
// Realizar las operaciones matemáticas (Suma, Resta, Multiplicación, División)
// y validar las reglas del dominio (ej. división por cero).
// ============================================================================
class Calculadora {
public:
    double sumar(double a, double b) const {
        return a + b;
    }

    double restar(double a, double b) const {
        return a - b;
    }

    double multiplicar(double a, double b) const {
        return a * b;
    }

    double dividir(double a, double b) const {
        if (b == 0.0) {
            throw std::invalid_argument("Error de Dominio: No se puede dividir por cero.");
        }
        return a / b;
    }
};

// ============================================================================
// 2. CONTROLADOR (Patrón GRASP Controller)
// Responsabilidad (Controller / Coordinator):
// Recibir los eventos o solicitudes del sistema desde la Vista/UI,
// coordinar la ejecución invocando la lógica del Modelo y retornar los resultados.
// Desacopla la interfaz de usuario de la lógica de negocio.
// ============================================================================
class CalculadoraController {
private:
    Calculadora modelo; // Referencia o instancia de la lógica del dominio

public:
    CalculadoraController() = default;

    // Métodos delegados que coordinan la ejecución y captura de excepciones
    double procesarSuma(double a, double b) {
        return modelo.sumar(a, b);
    }

    double procesarResta(double a, double b) {
        return modelo.restar(a, b);
    }

    double procesarMultiplicacion(double a, double b) {
        return modelo.multiplicar(a, b);
    }

    double procesarDivision(double a, double b) {
        // El controlador maneja o delega la validación de negocio
        return modelo.dividir(a, b);
    }
};

// ============================================================================
// 3. VISTA (Interfaz de Usuario en Consola)
// Responsabilidad (User Interface):
// Interactuar exclusivamente con el usuario (mostrar menús, leer entradas y 
// mostrar resultados). NO realiza operaciones matemáticas ni conoce la clase Calculadora.
// ============================================================================
class CalculadoraConsoleView {
private:
    CalculadoraController& controlador;

    // Auxiliar para limpiar el buffer de entrada en caso de error
    void limpiarBuffer() {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }

    // Auxiliar para solicitar un número con validación de entrada
    double pedirNumero(const std::string& mensaje) {
        double valor;
        while (true) {
            std::cout << mensaje;
            if (std::cin >> valor) {
                return valor;
            } else {
                std::cout << " Entrada inválida. Por favor, ingrese un número válido.\n";
                limpiarBuffer();
            }
        }
    }

public:
    explicit CalculadoraConsoleView(CalculadoraController& ctrl) : controlador(ctrl) {}

    void iniciar() {
        int opcion = 0;

        do {
            std::cout << "\n====================================\n";
            std::cout << "      CALCULADORA DE CONSOLA        \n";
            std::cout << "====================================\n";
            std::cout << "1. Sumar (+)\n";
            std::cout << "2. Restar (-)\n";
            std::cout << "3. Multiplicar (*)\n";
            std::cout << "4. Dividir (/)\n";
            std::cout << "5. Salir\n";
            std::cout << "Seleccione una opción (1-5): ";

            if (!(std::cin >> opcion)) {
                std::cout << " Opción no válida.\n";
                limpiarBuffer();
                continue;
            }

            if (opcion >= 1 && opcion <= 4) {
                double a = pedirNumero("Ingrese el primer operando: ");
                double b = pedirNumero("Ingrese el segundo operando: ");
                double resultado = 0.0;

                try {
                    // La vista solo le pide al controlador que procese la operación
                    switch (opcion) {
                        case 1:
                            resultado = controlador.procesarSuma(a, b);
                            std::cout << "\n Resultado: " << a << " + " << b << " = " << resultado << "\n";
                            break;
                        case 2:
                            resultado = controlador.procesarResta(a, b);
                            std::cout << "\n Resultado: " << a << " - " << b << " = " << resultado << "\n";
                            break;
                        case 3:
                            resultado = controlador.procesarMultiplicacion(a, b);
                            std::cout << "\n Resultado: " << a << " * " << b << " = " << resultado << "\n";
                            break;
                        case 4:
                            resultado = controlador.procesarDivision(a, b);
                            std::cout << "\n Resultado: " << a << " / " << b << " = " << resultado << "\n";
                            break;
                    }
                } catch (const std::exception& e) {
                    std::cout << "\n Error: " << e.what() << "\n";
                }
            } else if (opcion != 5) {
                std::cout << " Opción fuera de rango. intente de nuevo.\n";
            }

        } while (opcion != 5);

        std::cout << "\n¡Gracias por utilizar la calculadora!\n";
    }
};

// ============================================================================
// PUNTO DE ENTRADA (Main)
// Instancia los componentes y establece el flujo de control
// ============================================================================
int main() {
    CalculadoraController controlador;
    CalculadoraConsoleView vista(controlador);

    // Iniciar la aplicación
    vista.iniciar();

    return 0;
}