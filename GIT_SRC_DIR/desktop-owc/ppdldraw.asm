; OpenWatcom (wasm) port of PPDSDRAW.AS, large model.
; GEM calls _far_draw with the PARMBLK far pointer in AX:BX. We stash it in
; _drawpar, call the C handler _dr_code (an interrupt function) and return
; its result from _drawret.
.8086
.model large
extrn _dr_code_:far
public __far_draw
public __drawaddr
public __drawpar
public __drawret

.data
align 2
__drawaddr dw offset __far_draw
           dw seg __far_draw
__drawpar  dw 0,0
__drawret  dw 0

.code
__far_draw proc far
    push ds
    push ax
    mov  ax,DGROUP
    mov  ds,ax
    pop  ax
    mov  __drawpar,bx
    mov  __drawpar+2,ax
    pushf
    call far ptr _dr_code_
    mov  ax,__drawret
    pop  ds
    ret
__far_draw endp
end
