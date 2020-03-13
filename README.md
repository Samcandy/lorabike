# lorabike
本專案為 Lora 後端伺服器，實作從 Taifatech LoRa Gateway 接收 LoRa Device 資料，並透過 base64 解碼並使用 AES 解密後串接至前端伺服器，實作架構如圖。
![image](https://github.com/Samcandy/lorabike/blob/v2.0/img/Architecture.png)

## 環境準備
<p> python Version 3.7 </p>
<p> nodejs Version 12.16.1 </p>
### 相依套件安裝
`$ pip install -r requirements.txt`
### redis 安裝
`$ pip install lib/redis-2.10.6-py2.py3-none-any.whl`
### 解密模組
`$ npm install lib/lora-packet`
