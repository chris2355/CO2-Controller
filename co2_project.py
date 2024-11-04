import schedule
import time
import board
import busio
import adafruit_scd30
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from matplotlib import style
import multiprocessing
from multiprocessing import Process
import csv
from matplotlib.pyplot import figure


i2c = busio.I2C(board.SCL, board.SDA)
scd = adafruit_scd30.SCD30(i2c)

def co2_meter():
    if scd.data_available:
        tempf = scd.temperature * 9/5 + 32
#         print("Data Available!")
        print("CO2:", round(scd.CO2), "PPM")
        print("Temperature:", round(tempf, 2), "degrees F")
        print("Humidity:", round(scd.relative_humidity, 1), "%%rH")
        #print("Pressure:", round(scd.pressure_re, 2), "Bar")
        print("")
#         print("Waiting for new data...")
    else:
        print("FAILED")

def co2_log():
    while True:
        if scd.data_available:
            import datetime
            now = datetime.datetime.now().strftime("%H:%M")
            date = datetime.datetime.now().strftime("%Y_%m_%d")
            print(str(now), "," , round( scd.CO2), "," , round(scd.temperature ), "," , round(scd.relative_humidity), file=open("/home/pi/Desktop/log_files/{}_daily_log.csv".format(date), "a"))
            print("")
            print(str(now))
            print("!!!LOG UPDATED!!!")
            print("!!!LOG UPDATED!!!")
            print("!!!LOG UPDATED!!!")
            print("!!!LOG UPDATED!!!")
            print("")
            break
        else:
            import datetime
            now = datetime.datetime.now().strftime("%H:%M")
            print(str(now))
            print("!!!LOG FAILED!!!")
            print("!!!LOG FAILED!!!")
            print("!!!LOG FAILED!!!")
            print("!!!LOG FAILED!!!")
            
            
def co2_loghourly():
    while True:
        if scd.data_available:
            import datetime
            now = datetime.datetime.now().strftime("%H:%M")
            print(str(now), "," , round( scd.CO2), "," , round(scd.temperature ), "," , round(scd.relative_humidity), file=open("/home/pi/Desktop/hourlylog_files/Hourlylog.csv", "a"))
            print("")
            print(str(now))
            print("!!!LOG UPDATED!!!")
            print("!!!LOG UPDATED!!!")
            print("!!!LOG UPDATED!!!")
            print("!!!LOG UPDATED!!!")
            print("")
            break
        else:
            import datetime
            now = datetime.datetime.now().strftime("%H:%M")
            print(str(now))
            print("!!!LOG FAILED!!!")
            print("!!!LOG FAILED!!!")
            print("!!!LOG FAILED!!!")
            print("!!!LOG FAILED!!!")

def co2_graph():
    import datetime
    now = datetime.datetime.now().strftime("%H:%M")
    date = datetime.datetime.now().strftime("%Y_%m_%d")
    figure(figsize=(25, 7))
    x=[]
    y=[]

    with open("/home/pi/Desktop/log_files/{}_daily_log.csv".format(date), 'r') as csvfile:
        plots= csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(str(row[0]))
            y.append(int(row[1]))
            

    plt.plot(x,y, marker='o')
    plt.xticks(rotation = 90)

    plt.title('Daily CO2 readings')

    plt.xlabel('Time')
    plt.ylabel('CO2_PPM')

    plt.savefig("/home/pi/Desktop/graphs/{}_daily_graph.png".format(date))

def live_graph():
    import livegraph3
    return schedule.CancleJob



schedule.every(2).seconds.do(co2_meter)
# schedule.every().minute.do(co2_loghourly)
# schedule.every().hour.at(":00").do(co2_log)
# schedule.every().hour.at(":10").do(co2_log)
# schedule.every().hour.at(":20").do(co2_log)
# schedule.every().hour.at(":30").do(co2_log)
# schedule.every().hour.at(":40").do(co2_log)
# schedule.every().hour.at(":50").do(co2_log)
# schedule.every().day.at("23:59").do(co2_graph)
# schedule.every().minute.do(live_graph)


while True:
    schedule.run_pending()
    time.sleep(0)