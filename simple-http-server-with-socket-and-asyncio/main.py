import asyncio
from server import Server
from app import Application, Response


app = Application()

index_html = """
<html>
<head>
    <title>Fib</title>
</head>
<body>
    <div>
        <div id="fib">0</div>
        <input type="number" id="number" />
        <button onclick="sendValue()">Calculate</button>
    </div>
    <script>
        function sendValue() {
            const value = parseInt(document.getElementById("number").value);
            console.log({value});
            fetch("/fib", {
                "method": "POST",
                "headers": {
                    "content-type": "application/json",
                },
                "body": JSON.stringify({
                    "value": value,
                })
            }).then(response => {
                document.getElementById("fib").innerHTML = response.value; 
            }).catch(e => console.error(e));
        } 
    </script>
</body>
</html>
"""

@app.get("/")
async def homepage(request):
    return Response(index_html, 200, {"content-type": "text/html"})


@app.post("/fib")
async def greet(request):
    data = request.json
    a, b = 0, 1
    for i in range(data["value"]):
        a = a + b
        b = a - b

    return Response({"value": a}, 201, {"content-type": "application/json"})


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    s = Server(app)
    loop.create_task(s.run())
    loop.run_forever()
