import pickle

with open("noun_counts", "rb") as file:
    a = pickle.load(file)[:10]

print(a)
print(len(a))

# for i in range(1, 11):
#     data = "%d번째 줄입니다.\n" % i
#     print(data)