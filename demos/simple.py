from teechart import TeeChart

try:
    chart = TeeChart("teechart.dll")
    result = chart.render("sales,1500", 600)
except Exception as e:
    print("Error:", e)