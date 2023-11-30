import math
import matplotlib.pyplot as plt

def burdens(x: float):
    return ((x+1)*(x+1)) - (0.5 * math.pow(math.e, x))

def burdens_line(_y: float, t:float):
    return (_y - t*t) + 1

def wikipedia(x: float):
    return math.pow(math.e,x)

def wikipedia_line(_y: float, t: float):
    return _y

def chapra(t: float):
    return -0.5*t**4 + 4*t**3 - 10*t**2 + 8.5*t + 1

def chapra_line(_y: float, t: float):
    return -2*(t*t*t) + 12*t*t - 20*t + 8.5

def euler(_y0:float, _t:float, _step_size:float, _function: callable):
    return _y0 + _step_size * _function(_y0,_t)

def runge_kutta(_y0:float, _t:float, _step_size:float, _function: callable):
    k1 = _function(_y0, _t)
    k2 = _function(_y0 + _step_size*(k1/2), _t + _step_size/2)
    k3 = _function(_y0 + _step_size*(k2/2), _t + _step_size/2)
    k4 = _function(_y0 + _step_size*k3, _t + _step_size)
    return _y0 + (_step_size/6) * (k1 + 2*k2 + 2*k3 + k4)

def simple_step(_method: callable, _a: float, _b: float, _steps: int, _y0: float, _function: callable, _real_func: callable =None):
    h = (_b-_a)/_steps
    w = _y0
    t = _a
    x = [t]
    y = [w]
    real_y = None
    if _real_func is not None:
        real_y = [w]

    for i in range(1,_steps+1):
        w = _method(w,t,h,_function)
        t = _a + i * h
        x.append(t)
        y.append(w)
        if _real_func is not None:
            real_y.append(_real_func(t))
    
    return x,y,real_y
if __name__ == "__main__":
    # x,y,real = euler(0, 2, 4, 0.5, burdens_line, burdens)
    # x,y,real = euler(0,4,4,1,wikipedia_line, wikipedia)
    x,y,real = simple_step(runge_kutta,0,2,8,1,burdens_line, burdens)
    x2,y2,real2 = simple_step(euler,0,2,8,1,burdens_line, burdens)
    plt.plot(x, y, "red")
    plt.plot(x2,y2, "green")
    if real:
        plt.plot(x,real, "blue")
    plt.show()  