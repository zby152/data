;;;;;kernel/kernel.asm line 171

[SECTION .data]

AvaLinearAddress       dd  0x8000_0000
BitMap:    times   32  db  0xff
            times   32  db  0x00
BitMapLen equ $ - $$

global alloc_pages
global free_pages
global AllocAndFree


free_pages:
	
	push ebx         ; save eax and ebx
	push eax

	mov ebx, cr3
	and ebx, 0xfffff000
	and eax, 0xffc00000	
	shr eax, 20      ; 20 = 22 -2 
	add ebx, eax
	mov edx, [ebx]
	and edx, 0xfffffff8
	mov [ebx], edx
	
	mov ebx, [ebx]
			
	mov eax, [esp]
	add esp, 4 
	and ebx,0xfffff000
	and eax,0x003ff000
	shr eax,10
	add ebx, eax


	mov ecx, [esp]          
	add esp,4
.free_pte:
	mov eax, [ebx]
	and eax, 0xfffffff8	
    mov edx, eax			    ; eax:映射的物理地址
	shr edx, 12               ;edx:第edx个页面（由于物理地址开始为0x00000000）
	btr [BitMap], edx         ;改变位图，设置为0，空闲
	mov [ebx], eax
	add ebx,32
	loop .free_pte

	ret 

alloc_pages:

    mov ecx,eax

    ;计算总共需要分配的物理内存大小，并将其存储在 ebx 寄存器中。
    mov ebx,4096    ;page number * page size
    mul ebx

    mov ebx,[es:AvaLinearAddress]
    add [es:AvaLinearAddress],eax

    ;ebx存的是AvaLinearAddress 指定的线性地址对应的地址
    push ebx
    mov eax,ebx
    mov ebx,cr3
    and ebx,0xfffff000
    and eax,0xffc00000
    shr eax,20
    add ebx,eax     ;ebx中是PDE中的地址
    mov edx,ebx     ;edx->missing PDE address页目录项（PDE）的地址
    mov ebx,[ebx]   ;PTE 地址 
    ;test p flag 检查 PDE 中的 P 标志位
    test ebx,0x0000_0001
    jnz .pde_exist

    mov ebx,cr3
    mov ebx,[ebx]   ;first page table address
    and ebx,0xfffff000
    shl eax,10
    add ebx,eax     ;这里会直接变为页表的位置
    or ebx,0x0000_0007
    mov [edx],ebx

.pde_exist:
    mov eax,[esp]

    and ebx,0xfffff000
    and eax,0x003ff000
    shr eax,10
    add ebx,eax

.change_pte:
    call alloc_a_4k_page
    test eax,eax
    jz .allocation_failed   ;分配失败

    or eax,0x0000_0007
    mov [ebx],eax
    add ebx,4
    loop .change_pte
.allocation_failed:
    pop ebx
    ret


alloc_a_4k_page:

    push ds
    push es
    xor eax,eax

.search:
    bts [BitMap],eax

    jnc .find
    inc eax
    cmp eax,BitMapLen*8
    jl .search

    mov eax,0
    ret

.find:

    shl eax,12

    pop es
    pop ds
    ret


AllocAndFree:
	xchg	bx,bx
	mov	eax,4
	call	alloc_pages
	
	xchg	bx,bx
	mov	eax,ebx
	mov	ebx,4

	call	free_pages
	xchg	bx,bx
	ret
