# Christopher Sloggett
# CS-441-AI
import numpy as np

# The function in question
def f(x, y):
    return 5*x**2 + 40*x + y**2 - 12*y + 127

# Gradient itself, which is the derivative of the function
def gradient(x, y):
    df_dx = 10*x + 40
    df_dy = 2*y - 12
    return np.array([df_dx, df_dy])

# Gradient Descent algorithm
def gradient_descent(learn_rate, steps, x_init, y_init):
    x, y = x_init, y_init
    for step in range(steps):
        grad = gradient(x, y)
        x -= learn_rate * grad[0]
        y -= learn_rate * grad[1]
        if step % 100 == 0:  # Log every 100 steps
            print(f"Step {step}: x={x:.4f}, y={y:.4f}, f(x, y)={f(x, y):.4f}")
    return x, y, f(x, y)

# Function to run experiments with the learning rate, number of steps and trials
def run_experiments(learn_rate, steps, trials):
    best_result = None
    for trial in range(trials):
        x_init = np.random.uniform(-10, 10)
        y_init = np.random.uniform(-10, 10)
        print(f"\nTrial {trial + 1} with learn_rate={learn_rate}: Initial x={x_init:.4f}, y={y_init:.4f}")
        x, y, value = gradient_descent(learn_rate, steps, x_init, y_init)
        if best_result is None or value < best_result[2]:
            best_result = (x, y, value)
    return best_result

# Parameters
learn_rates = [0.1, 0.01, 0.001]
steps = 500
trials = 10

# Run and report results
for learn_rate in learn_rates:
    print(f"\nRunning experiments with learn_rate={learn_rate}")
    best_x, best_y, best_value = run_experiments(learn_rate, steps, trials)
    print(f"\nBest result for learn_rate={learn_rate}: x={best_x:.4f}, y={best_y:.4f}, f(x, y)={best_value:.4f}")

# I found that the learning rate affects the convergence of the gradient descent algorithm
# where a learning rate larger than 0.1 can cause a faster convergence and overshoot the minimum
# A smaller learning rate may converge faster but can overshoot the minimum. A learaning rate of 
# 0.01 converged the slowest. 