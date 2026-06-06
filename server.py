import socket
import re
import json
import sqlite3
import bcrypt
import os
# 1. Create a socket (AF_INET = IPv4, SOCK_STREAM = TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
            continue
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
            elif data.decode().split('\n')[0].split(' ')[1] == '/favicon.ico':
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
            elif data.decode().split('\n')[0].split(' ')[1] == '/UATS':
                table = sqlite3.connect('data.db')
                cursor = table.cursor()
                cursor.execute("SELECT at FROM users")
                resulte = cursor.fetchall()
                response_body = json.dumps([i[0] for i in resulte]).encode("utf-8")
                headers = (
                    "HTTP/1.1 200 OK\n"
                    "Content-Type: application/json\n"
                    f"Content-Length: {len(response_body)}\n"
                    "Access-Control-Allow-Origin: *\n"
                    "Connection: close\n\n"
                ).encode("utf-8")
                response = headers + response_body
                client_socket.sendall(response)
            elif data.decode().split('\n')[0].split(' ')[1] == '/translate':
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
            elif data.decode().split('\n')[0].split(' ')[1] == '/assets/bell':
                with open(f"assets/bell.json", "rb") as f:
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
            elif data.decode().split('\n')[0].split(' ')[1] == '/assets/bellsound':
                with open(f"assets/bellsound.mp3", "rb") as f:
                    content = f.read()
                    headers = (
                        "HTTP/1.1 200 OK\n"
                        "Content-Type: audio/mpeg\n"
                        f"Content-Length: {len(content)}\n"
                        "Connection: close\n"
                        "\n"
                    ).encode("utf-8")
                    response = headers + content
                    client_socket.sendall(response)
            elif data.decode().split('\n')[0].split(' ')[1] == "/PFP's":
                response_body = json.dumps(os.listdir("assets/PFP's")).encode("utf-8")
                headers = (
                    "HTTP/1.1 200 OK\n"
                    "Content-Type: application/json\n"
                    f"Content-Length: {len(response_body)}\n"
                    "Access-Control-Allow-Origin: *\n"
                    "Connection: close\n\n"
                ).encode("utf-8")
                response = headers + response_body
                client_socket.sendall(response)
            elif re.match(r"(\/assets\/PFP's\/.+)",data.decode().split('\n')[0].split(' ')[1]):
                try:
                    with open(data.decode().split('\n')[0].split(' ')[1][1:], "rb") as f:
                        content = f.read()
                        headers = (
                            "HTTP/1.1 200 OK\n"
                            "Content-Type: image/jpeg\n"
                            f"Content-Length: {len(content)}\n"
                            "Connection: close\n"
                            "\n"
                        ).encode("utf-8")
                        response = headers + content
                        client_socket.sendall(response)
                except Exception:
                    with open("assets/error.png", "rb") as f:
                        content = f.read()
                        headers = (
                            "HTTP/1.1 200 OK\n"
                            "Content-Type: image/jpeg\n"
                            f"Content-Length: {len(content)}\n"
                            "Connection: close\n"
                            "\n"
                        ).encode("utf-8")
                        response = headers + content
                        client_socket.sendall(response)
            elif re.match(r"(\/page\?user=.*)",data.decode().split('\n')[0].split(' ')[1]):
                with open("page.html", "rb") as f:
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
            elif re.match(r"(\/post\?id=.*)",data.decode().split('\n')[0].split(' ')[1]):
                with open("post.html", "rb") as f:
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
            elif re.match(r"(\/posts\/\d+)",data.decode().split('\n')[0].split(' ')[1]):
                table = sqlite3.connect('data.db')
                cursor = table.cursor()
                cursor.execute('SELECT at, content FROM posts WHERE id = ?', (data.decode().split('\n')[0].split(' ')[1].split("/")[2],))
                posts = cursor.fetchall()
                response_body = json.dumps(list(posts[0])).encode("utf-8")
                headers = (
                    "HTTP/1.1 200 OK\n"
                    "Content-Type: application/json\n"
                    f"Content-Length: {len(response_body)}\n"
                    "Access-Control-Allow-Origin: *\n"
                    "Connection: close\n\n"
                ).encode("utf-8")
                response = headers + response_body
                client_socket.sendall(response)
            elif re.match(r"\/userdata\/.*",data.decode().split('\n')[0].split(' ')[1]):
                try:
                    table = sqlite3.connect('data.db')
                    cursor = table.cursor()
                    cursor.execute("SELECT pfp, name, at, description FROM users WHERE at = ?", (data.decode().split('\n')[0].split(' ')[1].split("/")[2],))
                    resulte = cursor.fetchall()
                    cursor.execute('SELECT following FROM users')
                    followers = len([i for i in cursor.fetchall() if data.decode().split('\n')[0].split(' ')[1].split("/")[2] in json.loads(i[0])])
                    cursor.execute('SELECT * FROM posts WHERE at = ?', (data.decode().split('\n')[0].split(' ')[1].split("/")[2],))
                    posts = cursor.fetchall()
                    cursor.execute('SELECT following FROM users WHERE at = ?', (data.decode().split('\n')[0].split(' ')[1].split("/")[2],))
                    following = cursor.fetchall()
                    response_body = json.dumps(list(resulte[0])+[followers]+[posts]+[json.loads(following[0][0])]).encode("utf-8")
                    headers = (
                        "HTTP/1.1 200 OK\n"
                        "Content-Type: application/json\n"
                        f"Content-Length: {len(response_body)}\n"
                        "Access-Control-Allow-Origin: *\n"
                        "Connection: close\n\n"
                    ).encode("utf-8")
                    response = headers + response_body
                    client_socket.sendall(response)
                except IndexError:
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
            elif re.match(r"\/usershort\/.*",data.decode().split('\n')[0].split(' ')[1]):
                table = sqlite3.connect('data.db')
                cursor = table.cursor()
                cursor.execute("SELECT pfp, name FROM users WHERE at = ?", (data.decode().split('\n')[0].split(' ')[1].split("/")[2],))
                response_body = json.dumps(list(resulte[0])).encode("utf-8")
                headers = (
                    "HTTP/1.1 200 OK\n"
                    "Content-Type: application/json\n"
                    f"Content-Length: {len(response_body)}\n"
                    "Access-Control-Allow-Origin: *\n"
                    "Connection: close\n\n"
                ).encode("utf-8")
                response = headers + response_body
                client_socket.sendall(response)
            elif re.match(r"(\/.+)",data.decode().split('\n')[0].split(' ')[1]):
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
                    with open("assets/bell.json","r") as f:
                        counters = json.loads(f.readlines()[0])[1].encode("utf-8")
                    table = sqlite3.connect('data.db')
                    cursor = table.cursor()
                    cursor.execute("INSERT INTO users (at, name, password, following, pfp, description, notifications, notificated) VALUES (?,?,?,?,?,?,?,?)", (action['name'], action['name'], bcrypt.hashpw(action['password'].encode("utf-8"), counters), "[]", "standart.png", None, "[]", "[]"))
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
                with open("assets/bell.json","r") as f:
                    counters = json.loads(f.readlines()[0])[1].encode("utf-8")
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
                    
                table.commit()
                
                if bcrypt.hashpw(action["password"].encode("utf-8"), counters) == resulte[0][0]:
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
            if action["action"] == "post/post":
                table = sqlite3.connect('data.db')
                cursor = table.cursor()
                cursor.execute("INSERT INTO posts (at, content) VALUES (?,?)", (action["AT"],action["content"]))
                table.commit()
                response_body = {"status": 1, "error": "None"}
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
            if action['action'] == "user/follow":
                table = sqlite3.connect('data.db')
                cursor = table.cursor()
                cursor.execute("SELECT following FROM users WHERE at = ?", (action["AT"],))
                result = json.loads(cursor.fetchall()[0][0])
                if action["who"] in result:
                    result.remove(action["who"])
                else:
                    result.append(action["who"])
                cursor.execute("UPDATE users SET following = ? WHERE at = ?", (json.dumps(result), action["AT"]))
                table.commit()
                response_body = {"status": 1, "error": "None"}
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
            if action['action'] == "post/delete":
                table = sqlite3.connect('data.db')
                cursor = table.cursor()
                cursor.execute("DELETE FROM posts WHERE id = ?", (action["id"],))
                table.commit()
                if cursor.rowcount == 0:
                    response_body = {"status": 0, "error": "n/p"}
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
                else:
                    response_body = {"status": 1, "error": "None"}
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
            if action["action"] == "post/edit":
                table = sqlite3.connect('data.db')
                cursor = table.cursor()
                cursor.execute("UPDATE posts SET content = ? WHERE id = ?", (action["content"],action["id"]))
                table.commit()
                response_body = {"status": 1, "error": "None"}
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
            if action["action"] == "user/update status":
                table = sqlite3.connect('data.db')
                cursor = table.cursor()
                cursor.execute("UPDATE users SET pfp = ?, name = ?, description = ? WHERE at = ?", (action["pfp"],action["name"], action["description"], action["at"]))
                table.commit()
                response_body = {"status": 1, "error": "None"}
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
                    
        # 6. Close the connection
        client_socket.close()
    except Exception as e:
        print(type(e).__qualname__ + str(e))
        server_socket.close()
        try:
            table.close()
        except NameError:
            pass
        break
