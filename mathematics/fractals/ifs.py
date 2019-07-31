import numpy as np
from PIL import Image, ImageDraw
import time

from . import api

ROOT3 = np.sqrt(3)


@api(mode="final")
class IFS:
    """
    Iterated function system
    """
    
    def __init__(self, *maps, dimension=2):
        self.maps = maps
        self.dimension = dimension
        
    def __getitem__(self, item):
        return self.maps[item]
    
    def __call__(self, *points):
        return [tuple(m(point) for point in points)
                for m in self.maps]
                
    def apply(self, *figures):
        """
        Apply the map to figures, which consists of a tuple of
        points defining the vertices of a the figure.
        """
        return [f for fig in figures for f in self(*fig)]
        
    def iterate(self, figure, iterations):
        """
        Apply the IFS iteratively to a figure.
        """
        temp = [figure]
        last_time = time.time()
        for i in range(iterations):
            temp = self.apply(*temp)
            print(f"Applied iteration {i}",
                  f"in {time.time() - last_time} seconds",
                  f"({len(temp)} points)"
                  )
        return temp
        
    def __repr__(self):
        return f"IFS({', '.join(map(lambda m: m.__name__, self.maps))})"
        
    def render(self, initial_figure, iterations=1, window=(480, 270), file=None):
        """
        Render the result of the ifs applied iteratively to an initial
        figure.
        """
        figures = self.iterate(initial_figure, iterations)
        
        image = Image.new("RGB", window, "#ffffff")
        draw = ImageDraw.Draw(image)
        
        if self.dimension == 1:
            y = window[1] // 2
            sf = window[0]
            for fig in figures:
                pts = list(map(lambda x: (sf * x, y), fig))
                draw.polygon(pts, fill=0)
        elif self.dimension == 2:
            xsf, ysf = window
            for fig in figures:
                pts = list(map(lambda p: (xsf*p[0], ysf*p[1]/ROOT3), fig))
                draw.polygon(pts, fill="#000000")
        else:
            raise RuntimeError("Cannot plot higher dimensional fractals")
        image.transpose(Image.FLIP_TOP_BOTTOM)
        if file is None:
            image.show()
        else:
            image.save(file, "eps")
        

@api(mode="final")
def cantor_middle_thirds(iterations=2, window=(480, 270), file=None):
    """
    Render the Cantor Middle thirds set.

    :param iterations:
    :param window:
    :param file:
    :return:
    """

    def map1(point):
        return point / 3
        
    def map2(point):
        return (point + 2) / 3
    ifs = IFS(map1, map2, dimension=1)
    ifs.render(
            (0.0, 1.0),
            iterations=iterations,
            window=window,
            file=file
        )


@api(mode="final")
def sierpinski_triangle(iterations=2, window=(480, 270), file=None):
    """
    Render the Sierpinski triangle.

    :param iterations:
    :param window:
    :param file:
    :return:
    """
    def map1(point):
        return point / 2
        
    def map2(point):
        return np.array([point[0] + 1, point[1]]) / 2
        
    def map3(point):
        return np.array([point[0] + 0.5, point[1] + ROOT3]) / 2

    ifs = IFS(map1, map2, map3, dimension=2)
    ifs.render(
            (np.array([0.0, 0.0]),
             np.array([1., 0.0]),
             np.array([.5, ROOT3])),
            iterations=iterations,
            window=window,
            file=file
        )
