from datetime import datetime

print("Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class CovidDatasetAnalyzer:
    def __init__(self, num):
        self._num = num

covid = CovidDatasetAnalyzer(10)
covid2 = CovidDatasetAnalyzer(20)

print(f"{hex(id(covid))}  {hex(id(covid2))}")

print(help(CovidDatasetAnalyzer))