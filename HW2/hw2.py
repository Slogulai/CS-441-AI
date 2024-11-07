import numpy as np

# Define the function and its gradient
def f(x, y):
    return 5*x**2 + 40*x + y**2 - 12*y + 127

def gradient(x, y):
    df_dx = 10*x + 40
    df_dy = 2*y - 12
    return np.array([df_dx, df_dy])

# Gradient Descent algorithm
def gradient_descent(eta, steps, x_init, y_init):
    x, y = x_init, y_init
    for _ in range(steps):
        grad = gradient(x, y)
        x -= eta * grad[0]
        y -= eta * grad[1]
    return x, y, f(x, y)

# Run experiments
def run_experiments(eta, steps, trials):
    best_result = None
    for _ in range(trials):
        x_init = np.random.uniform(-10, 10)
        y_init = np.random.uniform(-10, 10)
        x, y, value = gradient_descent(eta, steps, x_init, y_init)
        if best_result is None or value < best_result[2]:
            best_result = (x, y, value)
    return best_result

# Parameters
etas = [0.1, 0.01, 0.001]
steps = 500
trials = 10

for eta in etas:
    best_x, best_y, best_value = run_experiments(eta, steps, trials)
    print(f"Best result for eta={eta}: x={best_x:.4f}, y={best_y:.4f}, f(x, y)={best_value:.4f}")
