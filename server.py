import socket
import re
import json
import sqlite3
# 1. Create a socket (AF_INET = IPv4, SOCK_STREAM = TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Bind to an address and port
server_socket.bind(('0.0.0.0', 8080))

# 3. Listen for incoming connections
server_socket.listen()
print("Server is listening on 127.0.0.1:8080...")

while True:
    try:
        # 4. Accept a connection
        client_socket, address = server_socket.accept()
        print(f"Connected by {address}")
        
        # 5. Receive and send data
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received: {data.decode()}")
        if re.match(r"GET /",data.decode().split('\n')[0]):
            if data.decode().split('\n')[0].split(' ')[1] == "/":
                with open("index.html", "rb") as f:
                    content = f.read()
                    headers = (
                        "HTTP/1.1 200 OK\n"
                        "Content-Type: text/html; charset=utf-8\n"
                        f"Content-Length: {len(content)}\n"
                        "Connection: close\n"
                        "\n"
                    ).encode("utf-8")
                    response = headers + content
                    client_socket.sendall(response)
            if data.decode().split('\n')[0].split(' ')[1] == '/favicon.ico':
                with open(f"favicon.ico", "rb") as f:
                    content = f.read()
                    headers = (
                        "HTTP/1.1 200 OK\n"
                        "Content-Type: image/x-icon\n"
                        f"Content-Length: {len(content)}\n"
                        "Connection: close\n"
                        "\n"
                    ).encode("utf-8")
                    response = headers + content
                    client_socket.sendall(response)
            if data.decode().split('\n')[0].split(' ')[1] == '/translate':
                print("yes")
                with open(f"translation.json", "rb") as f:
                    content = f.read()
                    headers = (
                        "HTTP/1.1 200 OK\n"
                        "Content-Type: application/json\n"
                        f"Content-Length: {len(content)}\n"
                        "Connection: close\n"
                        "\n"
                    ).encode("utf-8")
                    response = headers + content
                    client_socket.sendall(response)
            if re.match(r"(\/(?!(favicon\.ico)|(translate)).+)",data.decode().split('\n')[0].split(' ')[1]):
                try:
                    with open(f".{data.decode().split('\n')[0].split(' ')[1]}.html", "rb") as f:
                        content = f.read()
                        headers = (
                            "HTTP/1.1 200 OK\n"
                            "Content-Type: text/html; charset=utf-8\n"
                            f"Content-Length: {len(content)}\n"
                            "Connection: close\n"
                            "\n"
                        ).encode("utf-8")
                        response = headers + content
                        client_socket.sendall(response)
                except FileNotFoundError:
                    with open("error.html", "rb") as f:
                        content = f.read()
                        headers = (
                            "HTTP/1.1 200 OK\n"
                            "Content-Type: text/html; charset=utf-8\n"
                            f"Content-Length: {len(content)}\n"
                            "Connection: close\n"
                            "\n"
                        ).encode("utf-8")
                        response = headers + content
                        client_socket.sendall(response)
        elif re.match(r"PUT /",data.decode().split('\n')[0]):
            action = json.loads(data.decode().split('\r\n\r\n')[1])
            if action["action"] == "account/create":
                try:
                    table = sqlite3.connect('data.db')
                    cursor = table.cursor()
                    cursor.execute("INSERT INTO users (at, name, password) VALUES (?,?,?)", (action['name'], action['name'], action['password']))
                    table.commit()
                    
                    response_body = {"status": 1, "error": "None"}
                    response_body = json.dumps(response_body).encode("utf-8")
                    response = (
                        "HTTP/1.1 200 OK\n"
                        "Content-Type: application/json\n"
                        f"Content-Length: {len(response_body)}\n"
                        "Access-Control-Allow-Origin: *\n"
                        "Connection: close\n\n"
                    ).encode("utf-8")
                    
                    client_socket.sendall(response + response_body)
                    client_socket.shutdown(socket.SHUT_WR)
                except sqlite3.IntegrityError as e:
                    if "UNIQUE" in str(e) and "at" in str(e):
                        response_body = {"status": 0, "error": "at-unique"}
                        response_body = json.dumps(response_body)
                        response = (
                            "HTTP/1.1 200 OK\n"
                            "Content-Type: application/json\n"
                            f"Content-Length: {len(response_body)}\n"
                            "Access-Control-Allow-Origin: *\n"
                            "Connection: close\n\n"
                        ).encode("utf-8")
                        client_socket.sendall(response + response_body.encode("utf-8"))
                        client_socket.close()
                        
            if action["action"] == "account/login":
                table = sqlite3.connect('data.db')
                cursor = table.cursor()
                cursor.execute("SELECT password FROM users WHERE at = ?", (action["name"],))
                resulte = cursor.fetchall()
                if resulte == []:
                    response_body = {"status": 0, "error": "n/u"}
                    response_body = json.dumps(response_body)
                    response = (
                        "HTTP/1.1 200 OK\n"
                        "Content-Type: application/json\n"
                        f"Content-Length: {len(response_body)}\n"
                        "Access-Control-Allow-Origin: *\n"
                        "Connection: close\n\n"
                    ).encode("utf-8")
                    client_socket.sendall(response + response_body.encode("utf-8"))
                    client_socket.close()
                    continue
                    
                print(resulte)
                table.commit()
                
                if action["password"] == resulte[0][0]:
                    response_body = {"status": 1, "error": "None"}
                    response_body = json.dumps(response_body).encode("utf-8")
                    response = (
                        "HTTP/1.1 200 OK\n"
                        "Content-Type: application/json\n"
                        f"Content-Length: {len(response_body)}\n"
                        "Access-Control-Allow-Origin: *\n"
                        "Connection: close\n\n"
                    ).encode("utf-8")
                    
                    client_socket.sendall(response + response_body)
                    client_socket.shutdown(socket.SHUT_WR)
                else:
                    response_body = {"status": 0, "error": "w/p"}
                    response_body = json.dumps(response_body)
                    response = (
                        "HTTP/1.1 200 OK\n"
                        "Content-Type: application/json\n"
                        f"Content-Length: {len(response_body)}\n"
                        "Access-Control-Allow-Origin: *\n"
                        "Connection: close\n\n"
                    ).encode("utf-8")
                    client_socket.sendall(response + response_body.encode("utf-8"))
                    client_socket.close()                
                    
        # 6. Close the connection
        client_socket.close()
    except Exception as e:
        print(type(e).__qualname__ + str(e))
        server_socket.close()
        table.close()
        break
