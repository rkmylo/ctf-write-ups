import sys
import string
import r2pipe

flag = ["*"]*56

charset = string.digits + string.uppercase + string.lowercase + "{}_!"

def continue_to_index(i):
    for x in range(i):
        r2.cmd("dc")

for flag_index in range(len(flag)):
    for c in charset:
        r2 = r2pipe.open("unknown")
        flag[flag_index] = c
        r2.cmd('doo "{}"'.format("".join(flag)))
        r2.cmd("db 0x401C82")
        continue_to_index(flag_index+1)
        rax = int(r2.cmd("dr rax"), 16)
        r2.quit()
        if rax == 0:
            sys.stdout.write("\r"+"".join(flag))
            sys.stdout.flush()
            break

# TUCTF{w3lc0m3_70_7uc7f_4nd_7h4nk_y0u_f0r_p4r71c1p471n6!}
