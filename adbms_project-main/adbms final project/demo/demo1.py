from cryptography.fernet import Fernet


user_password=str(input("Enter encrypted Password:"))

key=Fernet.generate_key()
fernet=Fernet(key)
enc_msg=fernet.encrypt(user_password.encode())

print('og string:',user_password)
print('encrypted string:',enc_msg)
#dec_msg=fernet.decrypt(user_password).decode()
#print('decrypted string:',dec_msg)
