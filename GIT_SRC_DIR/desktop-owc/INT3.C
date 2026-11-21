void debugbreak(void)
{
	_asm { int 3 }
}
unsigned getcs(void);
#pragma aux getcs = "mov ax,cs" value [ax];
