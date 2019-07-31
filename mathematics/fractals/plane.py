
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


def _plane_fractal_plot(Z, N, horizon, xrange, yrange,
                        width, height, dpi, cmap, gamma):
    with np.errstate(invalid='ignore'):
        z = np.nan_to_num(N + 1 - np.log(np.log(abs(Z))) / np.log(2)
                          + np.log(np.log(horizon)) / np.log(2))

    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    ax.imshow(z, cmap=cmap, origin='lower', norm=colors.PowerNorm(gamma),
              extent=[*xrange, *yrange])
    ax.set_xticks([])
    ax.set_yticks([])


def julia(func, xrange=(-5, 5), yrange=(-5, 5), Nx=100, Ny=100,
          max_iterations=1<<8, horizon=2.0**40, width=10, height=10,
          dpi=72, cmap='hot', gamma=0.3):
    """
    Find the points in the Julia set of a given a function func.

    :param func:
    :param xrange:
    :param yrange:
    :return:
    """
    x, y = np.meshgrid(np.linspace(*xrange, Nx), np.linspace(*yrange, Ny))
    Z = x + 1j*y

    counts = np.zeros(Z.shape)

    for i in range(max_iterations):
        I = np.less(abs(Z), horizon)
        Z[I] = func(Z[I])
        counts[I] = i
    counts[counts == max_iterations - 1] = 0

    _plane_fractal_plot(Z, counts, horizon, xrange, yrange, width, height, dpi,
                        cmap, gamma)


def mandel(xrange=(-2, 0.5), yrange=(-1.25, 1.25), Nx=100, Ny=100,
           max_iterations=1<<8, horizon=2.0**40, width=10, height=10,
           dpi=72, cmap='hot', gamma=0.3):
    """
    Create a plot of the Mandelbrot set.

    :param xrange:
    :param yrange:
    :param Nx:
    :param Ny:
    :param max_iterations:
    :param horizon:
    :return:
    """

    x, y = np.meshgrid(np.linspace(*xrange, Nx), np.linspace(*yrange, Ny))
    C = x + 1j * y
    counts = np.zeros(C.shape, dtype=int)
    Z = np.zeros(C.shape, np.complex64)

    for i in range(max_iterations):
        I = np.less(abs(Z), horizon)
        Z[I] = Z[I] ** 2 + C[I]
        counts[I] = i
    counts[counts == max_iterations -1] = 0

    _plane_fractal_plot(Z, counts, horizon, xrange, yrange, width, height, dpi,
                        cmap, gamma)
