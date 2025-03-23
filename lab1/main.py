import numpy as np
import matplotlib.pyplot as plt

# Параметры
a = 2
n_values = np.arange(100, 100000, 100)
epsilon_values = [0.1, 0.01, 0.001, 0.0001]
radii = [a/(k+1) for k in range(1, 6)]

# Функция для расчета истинной вероятности
def true_probability(r, a):
    return (np.pi * r**2) / (4 * a**2)

# Функция для генерации точек и расчета доли попавших в круг
def estimate_probability(r, a, n):
    x = np.random.uniform(-a, a, n)
    y = np.random.uniform(-a, a, n)
    inside = (x**2 + y**2) <= r**2
    return np.mean(inside)

# Создаем фигуру и оси для 5 графиков в строке
fig, axes = plt.subplots(1, 5, figsize=(20, 4))  # 1 строка, 5 столбцов

# Построение графиков для каждого значения радиуса
for i, r in enumerate(radii):
    p = true_probability(r, a)
    p_hat = [estimate_probability(r, a, n) for n in n_values]
    epsilon = [abs(ph - p) for ph in p_hat]
    
    # График p̂(n)
    axes[i].plot(n_values, p_hat, label=f'$\hat{{p}}(n)$ for r={r:.2f}')
    axes[i].axhline(y=p, color='r', linestyle='--', label=f'True p={p:.4f}')
    axes[i].set_xlabel('Number of points n')
    axes[i].set_ylabel('$\hat{p}(n)$')
    axes[i].legend()
    axes[i].set_title(f'Estimation of p for r={r:.2f}')

plt.tight_layout()  # Автоматическая настройка расстояний между графиками
plt.show()

# Аналогично для графиков ошибок ε(n)
fig, axes = plt.subplots(1, 5, figsize=(20, 4))

for i, r in enumerate(radii):
    p = true_probability(r, a)
    p_hat = [estimate_probability(r, a, n) for n in n_values]
    epsilon = [abs(ph - p) for ph in p_hat]
    
    # График ε(n)
    axes[i].plot(n_values, epsilon, label=f'$\epsilon(n)$ for r={r:.2f}')
    axes[i].set_xlabel('Number of points n')
    axes[i].set_ylabel('$\epsilon(n)$')
    axes[i].legend()
    axes[i].set_title(f'Error $\epsilon(n)$ for r={r:.2f}')

plt.tight_layout()
plt.show()

# Создаем фигуру для объединенного графика
plt.figure(figsize=(10, 6))

# Для каждого значения радиуса вычисляем N(ε) и строим график
for r in radii:
    p = true_probability(r, a)
    N_epsilon = []
    for epsilon in epsilon_values:
        n = 100
        while True:
            p_hat = estimate_probability(r, a, n)
            if abs(p_hat - p) <= epsilon:
                N_epsilon.append(n)
                break
            n += 100
    
    # Рисуем линию для текущего радиуса
    plt.plot(epsilon_values, N_epsilon, marker='o', label=f'r={r:.2f}')

# Настройки графика
plt.xlabel('ε (Точность)')
plt.ylabel('N(ε) (Количество точек)')
plt.title('Зависимость N(ε) от точности ε для разных радиусов')
plt.legend(title='Радиус r')
plt.grid(True)
plt.xscale('log')  # Логарифмическая шкала для оси X
plt.yscale('log')  # Логарифмическая шкала для оси Y
plt.show()
