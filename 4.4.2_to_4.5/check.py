import hmac,hashlib
print(hmac.new(b"Adele", b"Miller", hashlib.md5).hexdigest())
      
