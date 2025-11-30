import tkinter as tk
from tkinter import messagebox
import socket
import requests
import re

# ------------------ Port Scanner ------------------
def scan_ports():
    target = entry.get()
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"Scanning open ports for: {target}\n\n")

    common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306]

    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            res = sock.connect_ex((target, port))
            if res == 0:
                result_text.insert(tk.END, f"✅ Open Port Found: {port}\n")
            sock.close()
        except:
            pass


# ------------------ HTTP Header Check ------------------
def check_headers():
    target = entry.get()
    result_text.delete("1.0", tk.END)
    try:
        r = requests.get("http://" + target)
        result_text.insert(tk.END, "HTTP Security Header Check:\n\n")

        if "X-Frame-Options" in r.headers:
            result_text.insert(tk.END, "✅ X-Frame-Options Found\n")
        else:
            result_text.insert(tk.END, "❌ Missing X-Frame-Options (Clickjacking Risk)\n")

        if "Content-Security-Policy" in r.headers:
            result_text.insert(tk.END, "✅ CSP Header Found\n")
        else:
            result_text.insert(tk.END, "❌ Missing CSP (XSS Risk)\n")

    except:
        messagebox.showerror("Error", "Website not reachable!")


# ------------------ SQL Injection Test ------------------
def sql_test():
    target = entry.get()
    result_text.delete("1.0", tk.END)

    payload = "' OR '1'='1"
    test_url = f"http://{target}/?id={payload}"

    try:
        r = requests.get(test_url)
        if re.search("sql|mysql|syntax|query", r.text, re.I):
            result_text.insert(tk.END, "❌ SQL Injection Vulnerability Found!\n")
        else:
            result_text.insert(tk.END, "✅ SQL Injection Not Detected\n")
    except:
        messagebox.showerror("Error", "Could not test SQL Injection")


# ------------------ XSS Test ------------------
def xss_test():
    target = entry.get()
    result_text.delete("1.0", tk.END)

    payload = "<script>alert(1)</script>"
    test_url = f"http://{target}/?search={payload}"

    try:
        r = requests.get(test_url)
        if payload in r.text:
            result_text.insert(tk.END, "❌ XSS Vulnerability Found!\n")
        else:
            result_text.insert(tk.END, "✅ XSS Not Detected\n")
    except:
        messagebox.showerror("Error", "Could not test XSS")


# ------------------ GUI Design ------------------
app = tk.Tk()
app.title("VAPT Tool - Basic Version")
app.geometry("700x500")

title = tk.Label(app, text="VAPT TOOL USING PYTHON", font=("Arial", 16, "bold"))
title.pack(pady=10)

entry = tk.Entry(app, width=40)
entry.pack()
entry.insert(0, "example.com")

btn_frame = tk.Frame(app)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Port Scan", width=15, command=scan_ports).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Header Check", width=15, command=check_headers).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="SQL Injection Test", width=18, command=sql_test).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="XSS Test", width=15, command=xss_test).grid(row=0, column=3, padx=5)

result_text = tk.Text(app, height=20, width=85)
result_text.pack(pady=10)

app.mainloop()
