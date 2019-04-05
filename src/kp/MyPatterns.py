import PIL
import random
import numpy as np

from .KandinskyTruth import KandinskyTruthInterfce
from .KandinskyUniverse import kandinskyShape, overlaps
from .KandinskyUniverse import SimpleUniverse
from .RandomKandinskyFigure import Random


class TwoSquaresOneRandom(KandinskyTruthInterfce):
    def isfuzzy(self):
        return false

    def humanDescription(self):
        return "contain two squares plus one random shape(square, triangle or circle)"

    def true_kf(self, n=1):
        kfs = []
        i = 0
        randomKFgenerator = Random(self.u, 3, 3)
        while i < n:
            kf = randomKFgenerator.true_kf(1)[0]
            numberSquares = 0
            for s in kf:
                if s.shape == "square":
                    numberSquares = numberSquares + 1
            if numberSquares > 1:
                kfs.append(kf)
                i = i + 1
        return kfs

    def false_kf(self, n=1):
        kfs = []
        i = 0
        randomKFgenerator = Random(self.u, 3, 3)
        while i < n:
            kf = randomKFgenerator.true_kf(1)[0]
            numberSquares = 0
            for s in kf:
                if s.shape == "square":
                    numberSquares = numberSquares + 1
            if numberSquares < 2:
                kfs.append(kf)
                i = i + 1
        return kfs



class MyBase(KandinskyTruthInterfce):
    def _randomobject (self, colors, shapes, minsize = 0.1, maxsize = 0.5):
        o = kandinskyShape()
        o.color = random.choice (colors)
        o.shape = random.choice (shapes)
        o.size  = minsize +  (maxsize-minsize) * random.random ()
        o.x     = o.size/2 + random.random () * (1-o.size )
        o.y     = o.size/2 + random.random () * (1-o.size )
        return o

    # returns a array of shapes
    def  _randomkf(self, min, max, colors, shapes):
        kf = []
        kftemp = []
        n = random.randint (min,max)

        minsize = 0.1
        if n == 3: minsize = 0.2
        if n == 2: minsize = 0.3
        if n == 1: minsize = 0.4
        
        maxsize = 0.6
        if n == 5: maxsize = 0.5
        if n == 6: maxsize = 0.4
        if n == 7: maxsize = 0.3
        if n > 7: 
            m = n-7
            maxsize = 0.2 - m * (0.2)/70.0 

        if maxsize < 0.001: maxsize =  0.001
        if minsize > maxsize: minsize =  maxsize

        # print (n, minsize, maxsize)
        i = 0
        maxtry= 20
        while i<n:
            kftemp = kf
            t = 0
            o = self._randomobject(colors, shapes, minsize, maxsize)
            kftemp = kf[:]
            kftemp.append (o)
            while overlaps (kftemp) and (t < maxtry):
                o = self._randomobject(colors, shapes, minsize, maxsize)
                kftemp = kf[:]
                kftemp.append (o)
                t = t + 1
            if (t < maxtry):
                kf = kftemp[:]
                i = i + 1
            else: 
                maxsize = maxsize*0.95
                minsize = minsize*0.95
        return kf

class AllColors(MyBase):

    def isfuzzy(self):
        return False

    def humanDescription(self):
        return "contain each color at least once"

    def  true_kf (self, n=1):     
        kfs = []
        for i in range(0, n):
            new = self._randomkf(self.min, 
                self.max, 
                SimpleUniverse.kandinsky_colors, 
                SimpleUniverse.kandinsky_shapes)            
            for s in range (len(new)):                
                cidx = s % len(SimpleUniverse.kandinsky_colors)                
                new[s].color = SimpleUniverse.kandinsky_colors[cidx]
            kfs.append(new)        
        return kfs

    def false_kf(self, n=1):
        kfs = []        
        for i in range(0, n):
            colorset = random.sample(SimpleUniverse.kandinsky_colors,2)
            new = self._randomkf(self.min, self.max, colorset, SimpleUniverse.kandinsky_shapes)
            kfs.append(new)
        return kfs  

class AllShapes(MyBase):

    def isfuzzy(self):
        return False

    def humanDescription(self):
        return "contain each shape at least once"

    def  true_kf (self, n=1):     
        kfs = []
        for i in range(0, n):
            new = self._randomkf(self.min, 
                self.max, 
                SimpleUniverse.kandinsky_colors, 
                SimpleUniverse.kandinsky_shapes)            
            for s in range (len(new)):                
                sidx = s % len(SimpleUniverse.kandinsky_shapes)                
                new[s].shape = SimpleUniverse.kandinsky_shapes[sidx]
            kfs.append(new)        
        return kfs  

    def false_kf(self, n=1):
        kfs = []        
        for i in range(0, n):
            shapeset = random.sample(SimpleUniverse.kandinsky_shapes,2)
            new = self._randomkf(self.min, self.max, SimpleUniverse.kandinsky_colors, shapeset)
            kfs.append(new)
        return kfs  

class LeftYellow(MyBase):

    def isfuzzy(self):
        return False

    def humanDescription(self):
        return "leftmost is always yellow"

    def  true_kf (self, n=1):     
        kfs = []
        for i in range(0, n):
            new = self._randomkf(self.min, 
                self.max, 
                SimpleUniverse.kandinsky_colors, 
                SimpleUniverse.kandinsky_shapes)            
            leftmost = np.argmin(list(map(lambda e:e.x, new)))
            new[leftmost].color = 'yellow'
            kfs.append(new)        
        return kfs  

    def false_kf(self, n=1):
        kfs = []        
        for i in range(0, n):            
            new = self._randomkf(self.min, 
                self.max, 
                SimpleUniverse.kandinsky_colors, 
                SimpleUniverse.kandinsky_shapes)
            leftmost = np.argmin(list(map(lambda e:e.x, new)))
            new[leftmost].color = random.choice(['blue', 'red'])
            kfs.append(new)
        return kfs  

class LeftSquare(MyBase):

    def isfuzzy(self):
        return False

    def humanDescription(self):
        return "leftmost is always a square"

    def  true_kf (self, n=1):
        kfs = []
        for i in range(0, n):
            new = self._randomkf(self.min, 
                self.max, 
                SimpleUniverse.kandinsky_colors, 
                SimpleUniverse.kandinsky_shapes)
            leftmost = np.argmin(list(map(lambda e:e.x, new)))
            new[leftmost].shape = 'square'
            kfs.append(new)        
        return kfs  

    def false_kf(self, n=1):
        kfs = []        
        for i in range(0, n):            
            new = self._randomkf(self.min, 
                self.max, 
                SimpleUniverse.kandinsky_colors, 
                SimpleUniverse.kandinsky_shapes)
            leftmost = np.argmin(list(map(lambda e:e.x, new)))
            new[leftmost].shape = random.choice(['circle', 'triangle'])
            kfs.append(new)
        return kfs  