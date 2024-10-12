from dbbase.md import mod
def pdr(t):
    for i in mod:
        t=t.replace(i,f"dbbase_{i}")
    return t
