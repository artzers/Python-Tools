from mpi4py import MPI 
 
import numpy as np 
 
comm = MPI.COMM_WORLD 
 
rank = comm.Get_rank() 
 
size = comm.Get_size() 
 
if rank == 0: 
 
    data = range(10) 
 
    comm.send(data, dest=1, tag=11) 
 
    print("process {} send {}...".format(rank, data)) 
 
else: 
 
    data = comm.recv(source=0, tag=11) 
 
    print("process {} recv {}...".format(rank, data))  

