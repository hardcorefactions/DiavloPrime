import os
import json
import hashlib
import requests

from colorama import Fore

dbs = os.listdir("dbs")
allData = []

def bruteforce(hash, salt):
    if len(hash) == 64:
        for password in words:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash == hash:
                return password
    elif len(hash) == 86 or len(hash) == 85:
        parts = hash.split("$")
        salt1 = parts[2]
        hash1 = parts[3]
        for word in words:
            var2 = hashlib.sha256(word.encode()).hexdigest()
            final = hashlib.sha256((var2 + salt1).encode()).hexdigest()
            if final == hash1:
                return word
    elif len(hash) == 128:
        for word in words:
            var2 = hashlib.sha512(word.encode()).hexdigest()
            final = hashlib.sha512((var2 + salt).encode()).hexdigest()
            if final == hash:
                return word
    elif "SHA256" in hash:
        parts = hash.split("$")
        salt = parts[1]
        wow = parts[2]
        for word in words:
            word_hash = hashlib.sha256(hashlib.sha256(word.encode()).hexdigest().encode() + salt.encode()).hexdigest()
            if word_hash == wow:
                return word
    elif "SHA512" in hash:
        parts = hash.split("$")
        salt = parts[1]
        wow = parts[2]
        for word in words:
            passenc = hashlib.sha512(word.encode()).hexdigest()
            word_hash = hashlib.sha512((passenc + salt).encode()).hexdigest()
            if word_hash == wow:
                return word
    return hash

for db in dbs:
    if db.split(".")[-1] == "json":
        with open("dbs/"+db, encoding='latin-1') as f:
            loaded = json.loads(f.read())
            allData.append({
                "server": db.replace(".json", ""),
                "data": loaded
            })

words = []
wordlist = ""

if not os.path.isfile("DiavloWordlist.txt"):
    print("Si no sabes sobre wordlists. Simplemente dale a enter. Se te descargara una sola.")
    wordlist = input("Inserta el nombre de la wordlist » ")
    if wordlist == "":
        wordlist = "DiavloWordlist.txt"
        open("DiavloWordlist.txt","wb").write(requests.get("https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt").content)
else:
    wordlist = "DiavloWordlist.txt"

with open(wordlist, "r", encoding='latin-1') as f:
    lines = f.read().split("\n")
    for line in lines:
        words.append(line)

while True:
    dataFound = []
    nickname = input("Nombre de usuario » ")
    for server in allData:
        for data in server["data"]:
            if data['name'] == nickname:
                hash, salt = "", ""
                hash = data["password"]
                if "salt" in data:
                    if not data["password"] == "null":
                        salt = data["salt"]
                        print(f"{Fore.BLUE}[ENCONTRADO] {Fore.YELLOW}=> {Fore.GREEN}{server['server']} {Fore.BLUE}| {Fore.GREEN}{nickname} {Fore.BLUE}| {Fore.GREEN}{data['password']} {Fore.BLUE}| {Fore.GREEN}{data['salt']}")
                else:
                    print(f"{Fore.BLUE}[ENCONTRADO] {Fore.YELLOW}=> {Fore.GREEN}{server['server']} {Fore.BLUE}| {Fore.GREEN}{nickname} {Fore.BLUE}| {Fore.GREEN}{data['password']}")
                tryBrute = bruteforce(hash, salt)
                if tryBrute != hash:
                    print(f"{Fore.RED}[DESENCRIPTADO] {Fore.YELLOW}=> {Fore.GREEN}{hash} {Fore.BLUE}| {Fore.GREEN}{tryBrute}")
    print(Fore.RESET, end='')