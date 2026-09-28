#include <algorithm>
#include <cassert>
#include <iostream>
#include <type_traits>
#include <vector>

template <typename T>
constexpr const T& menor(const T& primero, const T& segundo) {
    return (segundo < primero) ? segundo : primero;
}

template <typename A, typename B>
constexpr std::common_type_t<A, B>
menor_entre_tipos(const A& primero, const B& segundo) {
    return (segundo < primero) ? segundo : primero;
}

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

template <>
class Caja<bool> {
public:
    explicit Caja(bool valor) : valor_(valor) {}

    bool obtener() const {
        return valor_;
    }

    const char* texto() const {
        return valor_ ? "verdadero" : "falso";
    }

private:
    bool valor_;
};

int main() {
    assert(menor(2, 3) == 2);
    assert(menor(6.0, 4.0) == 4.0);
    assert(menor(1.5F, 2.5F) == 1.5F);

    const double menorMixto = menor_entre_tipos(2, 3.0);
    assert(menorMixto == 2.0);

    const Caja<int> cajaEntero(42);
    const Caja<bool> cajaBooleano(true);
    assert(cajaEntero.obtener() == 42);
    assert(cajaBooleano.obtener());
    assert(cajaBooleano.texto()[0] == 'v');

    std::vector<int> valores{4, 1, 3, 2};
    std::sort(valores.begin(), valores.end());
    assert((valores == std::vector<int>{1, 2, 3, 4}));

    std::cout << "menor(2, 3) = " << menor(2, 3) << '\n';
    std::cout << "menor(6.0, 4.0) = " << menor(6.0, 4.0) << '\n';
    std::cout << "menor(1.5f, 2.5f) = " << menor(1.5F, 2.5F) << '\n';
    std::cout << "menor_entre_tipos(2, 3.0) = " << menorMixto << '\n';
    std::cout << "Valores ordenados con std::sort:";
    for (const int valor : valores) {
        std::cout << ' ' << valor;
    }
    std::cout << '\n';
}
