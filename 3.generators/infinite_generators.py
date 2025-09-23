def infinite_chai():
	count = 1
	for _ in range(5):
		yield f"Refill #{count}"
		count +=1
	yield f"Refill {count}"

refill = infinite_chai()
user2 = infinite_chai()

for _ in range(5):	
	print(next(refill))
print(next(refill))
print()
for _ in range(6):
	print(next(user2))