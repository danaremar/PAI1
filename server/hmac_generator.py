from hashlib import sha3_256
import hmac

ENCODING = 'utf-8'

def generate_hmac(hash, token, challenge):
    key = f'{token}&{challenge}'.encode(ENCODING)
    raw = hash.encode(ENCODING)

    hashed = hmac.new(key, raw, sha3_256)

    return hashed.hexdigest()

#Para probar el uso del script
if __name__ == "__main__":
    print(generate_hmac("hola", "tokenn", "challenge?"))