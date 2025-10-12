from datetime import datetime

print("Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class CovidDataAnalyzer:
    def __init__(self, num):
        self._num = num

covid = CovidDataAnalyzer(10)
covid2 = CovidDataAnalyzer(20)

print(f"{hex(id(covid))}  {hex(id(covid2))}")

print(help(CovidDataAnalyzer))