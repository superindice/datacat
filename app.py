from flask import Flask, request, jsonify
import json, time

app = Flask(__name__)

def get_real_ip():
    # Render is behind a reverse proxy; X-Forwarded-For holds the client IP
    xff = request.headers.get("X-Forwarded-For", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.remote_addr

@app.route("/collect", methods=["POST", "GET"])
def collect():
    if request.method == "POST":
        specs = request.get_json(silent=True) or {}
    else:
        # also allows a simple GET pixel/beacon trigger
        specs = request.args.to_dict()

    record = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ip": get_real_ip(),
        "user_agent": request.headers.get("User-Agent"),
        "referer": request.headers.get("Referer"),
        "accept_language": request.headers.get("Accept-Language"),
        **specs,
    }
    print(json.dumps(record))          # shows up in Render's log stream
    with open("/tmp/visitors.jsonl", "a") as f:   # /tmp is the only writable dir on Render
        f.write(json.dumps(record) + "\n")
    return jsonify(ok=True), 204

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
<html>
<head>
     <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <title>Datacat</title>
    
    <link rel="icon" href="https://superindice.github.io/datacat/images/favicon.ico">
     <link rel="manifest" href="https://superindice.github.io/datacat/manifest.json" />
     <style>
#dclogo{
    width: 50px;
    margin-top:11px;
    margin-bottom: 30px;
    position: absolute;
    top: 0;

}
body{
   background:linear-gradient(orange,purple) ;
   background-repeat: no-repeat;
   background-attachment: fixed;
   font-family: Arial, Helvetica, sans-serif;


}

#header{
    position: absolute;
    top:0;
    left:65px;


}
#flexs{

    font-family: sans-serif;
}

h3{
    position: relative;
    top:100px;
}
#usr{
    border-radius: 20px;
    border-color: black;
    border-style:solid;
    width: 310px;
    margin-bottom: 30px;
    height:40px;
    font-size: 18px;
    padding-left:10px;

}
#psw{
    border-radius: 20px;
    border-color: black;
    border-style:solid;
    width: 310px;
    margin-bottom: 30px;
    height:40px;
    font-size: 18px;
    padding-left:10px;
}
#sub{
    border-radius: 20px;
    border-color: black;
    border-style:solid;
    width:320px;
    height:40px;
}
#usr-psw{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    align-items: center;
    border-style:solid;
    border-color:black;
    width:310px;
    padding-bottom: 30px;
    padding-left: 30px;
    padding-right: 30px;
    border-radius: 20px;
    margin: 0 auto;   /* <— centers the box horizontally */
    position: relative;
    top: 140px; 
    
   
    
}
#pd{
    font-size: 4rem;
    position:relative;

}
#incorrect{
    background-color: red;
    color:white;
    width:190;
    position: relative;
    top: -20px;
    margin-bottom:20px;
    display: none;
}
#textin{
    font-size:12px;
    padding-left:8px;
    padding-right:8px;

}
     </style>
</head>
<body>
<h1 style='display: flex; flex-direction: colomen; align-items: center;'>PASSWORD is admin, usr is the same, this pg is under dev :)</h1>
    <div id="flexs">
  <h1 id="header">Datacat</h1>  
    <img id="dclogo" src="https://superindice.github.io/datacat/images/dclogo.png">
          <br>
          <div id="usr-psw">
            <h1 id="pd">Login</h1>
            <div id="incorrect"><h4 id="textin">Incorrect Username and/or Password</h4></div>
            <form id="usrform">
          <input id="usr" type="text" placeholder="Username" required>
          <br>
          <input id="psw" type="password" placeholder="Password" required>
          <br>
          <input type="submit" id="sub" value="Login">
      </form>    
</div>
<script>
    var rando = document.getElementById('incorrect')

    document.getElementById('usrform').addEventListener('submit', function(event) {
        // Prevent the default form submission behavior (page reload)
        event.preventDefault();

        // Get the input field's value
        const username = document.getElementById('usr').value;
        const password = document.getElementById('psw').value;
        
        if (username == "admin" && password == "admin"){
                window.location.href = "/home/index.html?accesskey=NJ**kdfi8034JFJpeoi34(*)dfaegdaOUH:OJHI:U;oijf9u090k";
        }
        else{
            rando.style.display = 'block'
        }
    });

  const payload = {
    screen: screen.width + "x" + screen.height,
    window: innerWidth + "x" + innerHeight,
    colorDepth: screen.colorDepth,
    lang: navigator.language,
    platform: navigator.platform,
    cores: navigator.hardwareConcurrency,
    memory: navigator.deviceMemory || null,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    referrer: document.referrer,
    page: location.href
  };
  fetch("https://datacat.onrender.com/collect", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });




</script>
       </body>
       
</html>
    
    
    
    
    """, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)   # Render expects port 10000 by default
