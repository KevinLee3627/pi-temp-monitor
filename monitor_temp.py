from gpiozero import CPUTemperature
from tabulate import tabulate
from math import floor
import numpy as np
import plotext as plt
import time

cpu = CPUTemperature()

colors = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKCYAN': '\033[96m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
}

def roundNum(num, digits):
    return floor(num * 10 ** digits) / (10 ** digits)

def CtoF(temp):
    fahrenheit = (temp + 1.8) + 32
    rounded = roundNum(fahrenheit, 3)
    return str(rounded)


def plotTemp(temps, times, tickRate, minutes):
    plt.clear_plot()
    plt.clear_terminal()

    plt.plot(times, temps, line_color='green')
    plt.xlim(times[0], times[0]+(60*minutes))

    plt.xlabel('Time (s)')
    plt.ylabel('Temp (\N{DEGREE SIGN}C)')
    plt.title('CPU Temperature in last 5 minutes')

    plt.axes_color('black')
    plt.canvas_color('black')
    plt.ticks_color('basil')
    plt.frame(True)
    plt.height(40)

    plt.show()
    return

times = [0]
temps = [cpu.temperature]

while True:
    #come up with better variable name for tickRate
    tickRate = 2 #takes data every {tickRate} seconds
    minutes = 5
    numPoints = int(60 / tickRate * minutes)

    if len(temps) > numPoints:
        temps = temps[-numPoints:]
        times = times[-numPoints:]

    temps.append(cpu.temperature)
    times.append(times[-1] + tickRate)
    plotTemp(temps, times, tickRate, minutes)
    
    averageTemp = roundNum(np.average(temps), 3)

    output = f""

    cpuTempColor = ''
    if cpu.temperature < 50:
        cpuTempColor = colors['OKBLUE']
    elif cpu.temperature < 65:
        cpuTempColor = colors['OKCYAN']
    elif cpu.temperature < 80:
        cpuTempColor = colors['OKGREEN']
    else:
        cpuTempColor = colors['FAIL'] + colors['BOLD']

    table = [[
        f"{colors['OKGREEN']}{str(cpu.temperature)}\N{DEGREE SIGN}C / {CtoF(cpu.temperature)}\N{DEGREE SIGN}F\n",
        f"{colors['OKGREEN']}{averageTemp} / {CtoF(averageTemp)}\N{DEGREE SIGN}F\n",
        f"{colors['OKGREEN']}{np.amax(temps)} / {CtoF(np.amax(temps))}\N{DEGREE SIGN}F\n",
        f"{colors['OKGREEN']}{np.amin(temps)} / {CtoF(np.amin(temps))}\N{DEGREE SIGN}F"
    ]]

    headers = [
        f"{cpuTempColor}CPU TEMPERATURE",
        f"{colors['OKGREEN']}Average Temperature (last {minutes} minutes)",
        f"{colors['FAIL']}Peak Temperature (last {minutes} minutes)",
        f"{colors['OKCYAN']}Lowest Temperature (last {minutes} minutes){colors['OKGREEN']}", #OKGREEN at end is to make sure table lines are green, not cyan
    ]

    print('\n')
    print(tabulate(table, headers=headers))

    time.sleep(tickRate)