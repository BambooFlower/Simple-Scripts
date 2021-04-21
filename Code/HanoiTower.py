# Recursive Python function to solve the tower of Hanoi

# source, destination and auxiliary are the name of the rods
  
def TowerOfHanoi(n , source, destination, auxiliary):
    if n==1:
        print("Move disk 1 from source",source,"to destination",destination)
        return
    TowerOfHanoi(n-1, source, auxiliary, destination)
    print("Move disk",n,"from source",source,"to destination",destination)
    TowerOfHanoi(n-1, auxiliary, destination, source)
          
# Example:
# n = 4
# TowerOfHanoi(n,'A','B','C') 
