from machine import Pin, I2C, ADC
#from ssd1306 import SSD1306_I2C
import network, usocket, utime, ntptime

from actuation import Actuate
actuate = Actuate()

from pickup import Status 
status = Status()

from weather import Weather
w = Weather()

i2c = I2C(1, scl = Pin(22), sda = Pin(21), freq = 115200)
address = 9

battery = ADC(Pin(34))
battery.atten(ADC.ATTN_11DB)

# user data
ssid = "Potato_Wi-Fi5"
pw = "123412341234"

#pic_url = "https://media3.giphy.com/media/8PfIEUgJLI591tvUOu/giphy.gif?cid=ecf05e47v5fpz39jcefe7m389thkztntakj4hw59p2kkm3ex&rid=giphy.gif&ct=g"
pic_url = "https://cdn.dribbble.com/users/2530132/screenshots/5188235/005.gif"
fh_image = "https://i.imgur.com/0qO6hWN.png?1"
web_query_delay = 600000
timezone_hour = 2 # timezone offset (hours)
alarm = [7, 30, 8, 30, 0] # alarm[hour, minute, enabled(1=True)]
p_time=0
battery_level = 1
ye=0
current_status=1
eng = 1
force_stop = False
weather_time = 0
weather_allow = False
battery_time = 0
battery_value = battery.read()
battery_level = (0.125 * battery_value - 400)/100
            
# connect to wifi
print("Connecting to WiFi...")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, pw)
while not wifi.isconnected():
    pass
print("Connected.")

# setup web server
s = usocket.socket()
s.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
s.bind(("", 80)) # listen port 80
s.setblocking(False) # set to non-blocking mode
s.settimeout(1)
s.listen(1) # allow 1 client
print("Web server is now online at", ssid, "IP:", wifi.ifconfig()[0])

weather_status = w.current_weather()

# webpage to be sent to user
def webpage_en(data):
    html = "<!DOCTYPE html>"
    html += "<html>"
    html += "<head>"
    html += "<title>Robot Lawn Mower Web Console</title>"
    html += "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
    html += "<link rel=\"icon\" href=\"#\">"
    html += "<style>body {background-color: #ffffff;} h1 {color: SaddleBrown; font-size: 20px} h2 {color: Olive;} p {color: #dc143c;} button{display: inline-block; background-color: #e7bd3b; border: noneborder-radius: 4px; color: white; padding: 6px 10px; text-decoration: none; font-size: 4px; margin: 2px; cursor: pointer;} button{background-color: #00FF00;} .button2{background-color: #FF0000;} .button3{background-color: #00FF00;}"
    html += "span {color: #dc143c; font-size: 17px;} span2 {color: #6a0dad; font-size: 15px;}"
    html += "</style>"
    html += "<body><center>"
    html += "<h1>Robot Lawn Mower Web Console</h1>"
    html += "</center></body>"    
    html += "<body><center>"
    html += "<span2>Weather Status : " + weather_status + "</span2>"
    if current_status == 0:
        pic_url = "https://i.imgur.com/FqplPBn.gif"
    if current_status == 1:
        pic_url = "https://i.imgur.com/YDXShcO.gif"
    if current_status == 2:
        pic_url = "https://i.imgur.com/Uf4CAZr.gif"
    html += "<p><img src=\"" + pic_url + "\" width=200px></p>"
    html += "<form methon=\"GET\" action=\"\">"
    html += "<span>Start at (hour/minute) "
    html += "<input type=\"text\" name=\"hour\" size=\"2\" maxlength=\"2\" value=\"" + str(data[0]) + "\">"
    html += " : <input type=\"text\" name=\"minute\" size=\"2\" maxlength=\"2\" value=\"" + str(data[1]) + "\">"
    html += "</span><br>"
    html += "<span2>Stop at (hour/minute) "
    html += "<input type=\"text\" name=\"hour_s\" size=\"2\" maxlength=\"2\" value=\"" + str(data[2]) + "\">"
    html += " : <input type=\"text\" name=\"minute_s\" size=\"2\" maxlength=\"2\" value=\"" + str(data[3]) + "\">"
    html += "<p>Enable: <select name=\"enable\"></span2>"
    if data[4] == 1:
        html += "<option value=\"0\">No</option>"
        html += "<option value=\"1\" selected>Yes</option>"
    else:
        html += "<option value=\"0\" selected>No</option>"
        html += "<option value=\"1\">Yes</option>"
    html += "</select></p>"
    html += "<p><input type=\"submit\" value=\"Update\">"
    html += "</form>"
    html += "<input type=\"button\" value=\"Refresh\" onclick=\"window.location.href=''\"></p>"
    html += "<span><label for=\"disk_d\">Battery Level</label>"
    html += " : <meter id=\"disk_d\" value=\"" + str(battery_level) + "\">100%</meter></span>"
    html += "</center></body>"
    html += """
  <body onload="initClock()">

    <!--digital clock start-->
    <div class="datetime">
      <div class="date">
        <span id="dayname">Day</span>,
        <span id="month">Month</ span>
        <span id="daynum">00</span>,
        <span id="year">Year</span>
      </div>
      <div class="time">
        <span id="hour">00</span> :
        <span id="minutes">00</span> :
        <span id="seconds">00</span>
        <span id="period">AM</span>
      </div>
    </div>
    <!--digital clock end-->

    <script type="text/javascript">
    function updateClock(){
      var now = new Date();
      var dname = now.getDay(),
          mo = now.getMonth(),
          dnum = now.getDate(),
          yr = now.getFullYear(),
          hou = now.getHours(),
          min = now.getMinutes(),
          sec = now.getSeconds(),
          pe = "AM";

          if(hou >= 12){
            pe = "PM";
          }

          Number.prototype.pad = function(digits){
            for(var n = this.toString(); n.length < digits; n = 0 + n);
            return n;
          }

          var months = ["January", "February", "March", "April", "May", "June", "July", "Augest", "September", "October", "November", "December"];
          var week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
          var ids = ["dayname", "month", "daynum", "year", "hour", "minutes", "seconds", "period"];
          var values = [week[dname], months[mo], dnum.pad(2), yr, hou.pad(2), min.pad(2), sec.pad(2), pe];
          for(var i = 0; i < ids.length; i++)
          document.getElementById(ids[i]).firstChild.nodeValue = values[i];
    }

    function initClock(){
      updateClock();
      window.setInterval("updateClock()", 1);
    }
    </script>
  </body>
  <head> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 6px 10px; text-decoration: none; font-size: 20px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> 
 <p><a href="/?ye"><button class="button">STOP</button></a></p>
 <p><a href="/?st"><button class="button">START</button></a></p>
    """
    html += "<span2>en|</span2>"
    html += """<a href="/?de"><text="text">de</button></a>"""
    html += "</html>"
    return html

def webpage_de(data):
    html = "<!DOCTYPE html>"
    html += "<html>"
    html += "<head>"
    html += "<title>Rasenmäher-Webkonsole</title>"
    html += "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
    html += "<link rel=\"icon\" href=\"#\">"
    html += "<style>body {background-color: #ffffff;} h1 {color: SaddleBrown; font-size: 20px} h2 {color: Olive;} p {color: #dc143c;} button{display: inline-block; background-color: #e7bd3b; border: noneborder-radius: 4px; color: white; padding: 6px 10px; text-decoration: none; font-size: 4px; margin: 2px; cursor: pointer;} button{background-color: #00FF00;} .button2{background-color: #FF0000;} .button3{background-color: #00FF00;}"
    html += "span {color: #dc143c; font-size: 17px;} span2 {color: #6a0dad; font-size: 15px;} "
    html += "</style>"
    html += "<body><center>"
    html += "<h1>Rasenmäher-Webkonsole</h1>"
    html += "</center></body>"
    html += "<body><center>"
    html += "<span2>Wetterstatus : " + weather_status_de + "</span2>"
    if current_status == 0:
        pic_url = "https://i.imgur.com/FqplPBn.gif"
    if current_status == 1:
        pic_url = "https://i.imgur.com/YDXShcO.gif"
    if current_status == 2:
        pic_url = "https://i.imgur.com/Uf4CAZr.gif"
    html += "<p><img src=\"" + pic_url + "\" width=200px></p>"
    html += "<form methon=\"GET\" action=\"\">"
    html += "<span>Beginn um (Stunde/Minute) "
    html += "<input type=\"text\" name=\"hour\" size=\"2\" maxlength=\"2\" value=\"" + str(data[0]) + "\">"
    html += " : <input type=\"text\" name=\"minute\" size=\"2\" maxlength=\"2\" value=\"" + str(data[1]) + "\">"
    html += "</span><br>"
    html += "<span2>Stopp um (Stunde/Minute) "
    html += "<input type=\"text\" name=\"hour_s\" size=\"2\" maxlength=\"2\" value=\"" + str(data[2]) + "\">"
    html += " : <input type=\"text\" name=\"minute_s\" size=\"2\" maxlength=\"2\" value=\"" + str(data[3]) + "\">"
    html += "<p>Aktivieren: <select name=\"enable\"></span2>"
    if data[4] == 1:
        html += "<option value=\"0\">Nein</option>"
        html += "<option value=\"1\" selected>Ja</option>"
    else:
        html += "<option value=\"0\" selected>Nein</option>"
        html += "<option value=\"1\">Ja</option>"
    html += "</select></p>"
    html += "<p><input type=\"submit\" value=\"Aktualisieren\">"
    html += "</form>"
    html += "<input type=\"button\" value=\"Neu laden\" onclick=\"window.location.href=''\"></p>"
    html += "<span><label for=\"disk_d\">Batterie Level</label>"
    html += " : <meter id=\"disk_d\" value=\"" + str(battery_level) + "\">100%</meter></span>"
    html += "</center></body>"
    html += """
  <body onload="initClock()">

    <!--digital clock start-->
    <div class="datetime">
      <div class="date">
        <span id="dayname">Tag</span>,
        <span id="month">Monat</ span>
        <span id="daynum">00</span>,
        <span id="year">Jahr</span>
      </div>
      <div class="time">
        <span id="hour">00</span> :
        <span id="minutes">00</span> :
        <span id="seconds">00</span>
        <span id="period">AM</span>
      </div>
    </div>
    <!--digital clock end-->

    <script type="text/javascript">
    function updateClock(){
      var now = new Date();
      var dname = now.getDay(),
          mo = now.getMonth(),
          dnum = now.getDate(),
          yr = now.getFullYear(),
          hou = now.getHours(),
          min = now.getMinutes(),
          sec = now.getSeconds(),
          pe = "AM";

          if(hou >= 12){
            pe = "PM";
          }

          Number.prototype.pad = function(digits){
            for(var n = this.toString(); n.length < digits; n = 0 + n);
            return n;
          }

          var months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
          var week = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];
          var ids = ["dayname", "month", "daynum", "year", "hour", "minutes", "seconds", "period"];
          var values = [week[dname], months[mo], dnum.pad(2), yr, hou.pad(2), min.pad(2), sec.pad(2), pe];
          for(var i = 0; i < ids.length; i++)
          document.getElementById(ids[i]).firstChild.nodeValue = values[i];
    }

    function initClock(){
      updateClock();
      window.setInterval("updateClock()", 1);
    }
    </script>
  </body>
  <head> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 6px 10px; text-decoration: none; font-size: 20px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> 
 <p><a href="/?ye"><button class="button">STOPP</button></a></p>
 <p><a href="/?st"><button class="button">START</button></a></p>
    """
    html += """<a href="/?en"><text="text">en</button></a>"""
    html += "<span2>|de</span2>"
    html += "</html>"
    return html

update_time = utime.ticks_ms() - web_query_delay
clients = []

while True:

    if(utime.time() - 120 >= weather_time):
        weather_status = w.current_weather()
        weather_time = utime.time()
        if (weather_status == "Thunderstorm"):
            weather_status_de = "Gewitter"
            weather_allow = False
            i2c.readfrom_mem(address, 3, 2)
            current_status = 2
        elif (weather_status == "Drizzle"):
            weather_status_de = "Nieselregen"
            weather_allow = False
            i2c.readfrom_mem(address, 3, 2)
            current_status = 2
        elif (weather_status == "Rain"):
            weather_status_de = "Regen"
            weather_allow = False
            i2c.readfrom_mem(address, 3, 2)
            current_status = 2
        elif (weather_status == "Snow"):
            weather_status_de = "Schnee"
            weather_allow = False
            i2c.readfrom_mem(address, 3, 2)
            current_status = 2
        elif (weather_status == "Atmosphere"):
            weather_status_de = "Atmosphäre"
            weather_allow = False
            i2c.readfrom_mem(address, 3, 2)
            current_status = 2
        elif (weather_status == "Clear"):
            weather_status_de = "Klar"
            weather_allow = True
        elif (weather_status == "Clouds"):
            weather_status_de = "Wolken"
            weather_allow = True

    try:
        # listen to new clients
        client, addr = s.accept()
        print("New client connected, IP:", addr)
        clients.append(client)
    except:
        pass # no clients to connect now
    
    # if there are clients connected:
    for client in clients:

        # get HTTP response
        request = client.recv(1024)
        request_text = str(request.decode("utf-8"))
        ye = request_text.find("/?ye")
        st = request_text.find("/?st")
        cs = request_text.find("/?cs")
        en = request_text.find("/?en")
        de = request_text.find("/?de")
        para_pos = request_text.find("/?") 
        print(para_pos)
            # extract GET parameters and set the alarm
        para_str = request_text[para_pos + 2:(request_text.find("HTTP/") - 1)]
        para_array = para_str.split('&')
                      
        for i in range(len(para_array)):
            para_array[i] = (para_array[i])[para_array[i].find('=') + 1:]
                   
        try:
            for i in range(5):
                if para_array[i].isdigit():
                    alarm[i] = int(para_array[i])
                else:
                    print("!!! Alarm time set error !!!")
        except:
            None
        
        print("Start schedule has been set to", str(alarm[0]) + ":" + str(alarm[1]))
        if alarm[4] == 1:
            print("Start schedule enabled")
        else:
            print("Start schedule disabled")
        print("Stop schedule has been set to", str(alarm[2]) + ":" + str(alarm[3]))
        
        if ye == 4:
            i2c.readfrom_mem(address, 2, 2)
        
        if st == 4:
            if weather_allow:
                i2c.readfrom_mem(address, 1, 2)
                current_status = 0

        if en == 4:
            eng=1
        if de == 4:
            eng=0           

        # send web page to user
        if eng == 1:
            response = webpage_en(alarm)
        else:
            response = webpage_de(alarm)
            
        print("Sending web page...")
        client.send("HTTP/1.1 200 OK\n")
        client.send("Content-Type: text/html; charset=utf-8\n")
        client.send("Connection: close\n\n")
        client.send(response)
        client.close()
        clients.remove(client)
        print("Client connection ended.")

    # update web clock time
    if utime.ticks_ms() - update_time >= web_query_delay:
        
        try:
            # update system time from NTP server
            ntptime.settime()
            print("NTP server query successful.")
            print("System time updated:", utime.localtime())
            update_time = utime.ticks_ms()
            
        except:
            print("NTP server query failed.")
    
    # display time and alarm status
    local_time_sec = utime.time() + timezone_hour * 3600
    local_time = utime.localtime(local_time_sec)
    time_str = "Alarm: {3:02d}:{4:02d}:{5:02d}".format(*local_time)
    alarm_str = "Time:  {0:02d}:{1:02d}".format(*alarm)
    alarm_str += " [O]" if alarm[4] == 1 else " [X]"
    
    # trigger alarm
    if alarm[4] == 1 and alarm[0] == local_time[3] and alarm[1] == local_time[4]:        
        print("The robot is self starting")
        if (utime.time()%60 == 0) & weather_allow:
            i2c.readfrom_mem(address, 1, 2)
        current_status = 0
        force_stop = False
    
    if alarm[4] == 1 and alarm[2] == local_time[3] and alarm[3] == local_time[4]:
        print("The robot is stopping and going to the charge station")
        i2c.readfrom_mem(address, 3, 2)
        current_status = 2

    if(utime.time() - 300 >= battery_time):
        
        if current_status == 0:
            i2c.readfrom_mem(address, 0, 2)
            utime.sleep(1)
            battery_time = utime.time()
            battery_value = battery.read()
            battery_level = (0.125 * battery_value - 400)/100
            i2c.readfrom_mem(address, 1, 2)
        if (utime.time()%60 == 0) & (battery_level < 5):
            i2c.readfrom_mem(address, 3, 2)
            current_status = 2
    
    status.robot_lifted()