import platform
import ctypes
import os

# load the shared library DLL 
if platform.system() == 'Linux': 
	qrnglibso =  os.path.join(os.getcwd(), 'libqrnglib.so') 
	qrnglibhdlr = ctypes.CDLL(qrnglibso)
else: 
	qrnglibdll  = os.path.join(os.getcwd(), 'qrnglib.dll')
	qrnglibhdlr = ctypes.WinDLL(qrnglibdll)

# Define the argument and return types for functions 
# that have a different return type
qrnglibhdlr.qrng_urand.argtypes = []
qrnglibhdlr.qrng_urand.restype = ctypes.c_double

def qrng_init():
    return qrnglibhdlr.qrng_init()

def qrng_rand(): 
    return qrnglibhdlr.qrng_rand()

def qrng_urand(): 
    return qrnglibhdlr.qrng_urand()

def qrng_get(cnt): 
    ret_len = ctypes.c_uint32(0)
    
    data_buf = (ctypes.c_ubyte * cnt)()
    ptr_cast = ctypes.cast(data_buf, ctypes.c_char_p) 
    ret = qrnglibhdlr.qrng_get( ptr_cast, ctypes.sizeof(data_buf), ctypes.byref(ret_len)) 
        
    return ret, data_buf[:]

def qrng_get_status():
    return qrnglibhdlr.qrng_get_status()
    
def qrng_shuffle(x):	
    int_class = int
    for i in reversed(range(1, len(x))):
        # swap current element with a different member in the list
        j = int_class(qrng_urand() * (i+1))
        x[i], x[j] = x[j], x[i]
        

