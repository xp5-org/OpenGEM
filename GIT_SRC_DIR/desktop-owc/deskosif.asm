; OpenWatcom (wasm) port of DESKOSIF.AS, large model.
; Hooks INT 10h/16h/21h so a launched program gets canned keystrokes.
; The Pacific long-arithmetic helpers (cxc33, cxd33, cxm33) and the unused
; chrin/chrout are dropped; Watcom has its own runtime for those.
; Handlers run with the caller's DS, so all own data is reached via CS:.
.8086
.model large
public takekey_, givekey_, takevid_, givevid_, takedos_, givedos_

KEYENTRY equ 16h
VIDENTRY equ 10h
DOSENTRY equ 21h

.code
dossav  dw 0,0
keysav  dw 0,0
vidsav  dw 0,0
keycnt  dw 0
f10cnt  dw 0
keytab  dw 1c0dh
        dw 314eh
        dw 1c0dh
        dw 0,0,0,0,0

inttake:
    push es
    mov  ah,35h
    int  21h
    mov  cs:[bp+2],es
    mov  cs:[bp],bx
    pop  es
intset:
    push ds
    mov  bx,cs
    mov  ds,bx
    mov  ah,25h
    int  21h
    pop  ds
    ret

intgive:
    push ds
    mov  dx,cs:[bp]
    mov  ds,cs:[bp+2]
    mov  ah,25h
    int  21h
    pop  ds
    ret

keycod:
    cmp  ah,00h
    jz   dinkey
    cmp  ah,01h
    jz   dinkey
    jmp  dword ptr cs:keysav

vidcod:
    iret

clrky:
    mov  ah,al
    cmp  ah,0
    jg   chkhi
    iret
chkhi:
    cmp  ah,0ah
    jle  doscod
    iret

doscod:
    cmp  ah,01h
    jz   dinkey
    cmp  ah,02h
    jz   doutstr
    cmp  ah,06h
    jz   ddirio
    cmp  ah,07h
    jz   ddirio
    cmp  ah,08h
    jz   dofunc8
    cmp  ah,09h
    jz   doutstr
    cmp  ah,0ah
    jz   dofunc10
    cmp  ah,0bh
    jz   csj
    cmp  ah,0ch
    jz   clrky
    jmp  dword ptr cs:dossav

csj:
    jmp  csout

ddirio:
    cmp  dl,0ffh
    jnz  doutstr
dinkey:
    push bx
    mov  ax,cs:keycnt
    mov  bx,offset keytab
    add  bx,ax
    inc  ax
    inc  ax
    mov  cs:keycnt,ax
    mov  ax,cs:[bx]
    pop  bx
    cmp  ax,0
    jnz  doutstr
    mov  cs:keycnt,ax
    jmp  dinkey
doutstr:
    sti
    retf 2

dofunc8:
    inc  word ptr cs:f10cnt
    cmp  word ptr cs:f10cnt,3
    jl   dof8
    mov  ax,4c00h
    jmp  dword ptr cs:dossav
dof8:
    jmp  dinkey

dofunc10:
    inc  word ptr cs:f10cnt
    cmp  word ptr cs:f10cnt,3
    jl   dof10
    mov  ax,4c00h
    jmp  dword ptr cs:dossav
dof10:
    push bx
    mov  bx,dx
    inc  bx
    mov  byte ptr ds:[bx],1
    inc  bx
    mov  byte ptr ds:[bx],4eh
    inc  bx
    mov  byte ptr ds:[bx],0dh
    pop  bx
    jmp  doutstr

csout:
    mov  al,0ffh
    iret

takekey_ proc far
    mov  word ptr cs:keycnt,0
    mov  word ptr cs:f10cnt,0
    cli
    push bp
    mov  al,KEYENTRY
    mov  bp,offset keysav
    mov  dx,offset keycod
    call inttake
    pop  bp
    sti
    ret
takekey_ endp

givekey_ proc far
    cli
    push bp
    mov  al,KEYENTRY
    mov  bp,offset keysav
    call intgive
    pop  bp
    sti
    mov  ax,cs:f10cnt
    ret
givekey_ endp

takevid_ proc far
    cli
    push bp
    mov  al,VIDENTRY
    mov  bp,offset vidsav
    mov  dx,offset vidcod
    call inttake
    pop  bp
    sti
    ret
takevid_ endp

givevid_ proc far
    cli
    push bp
    mov  al,VIDENTRY
    mov  bp,offset vidsav
    call intgive
    pop  bp
    sti
    ret
givevid_ endp

takedos_ proc far
    cli
    push bp
    mov  al,DOSENTRY
    mov  bp,offset dossav
    mov  dx,offset doscod
    call inttake
    pop  bp
    sti
    ret
takedos_ endp

givedos_ proc far
    cli
    push bp
    mov  al,DOSENTRY
    mov  bp,offset dossav
    call intgive
    pop  bp
    sti
    ret
givedos_ endp
end
