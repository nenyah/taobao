from cityid import city_id

# for key, value in city_id.items():
#     if len(key) < 3:
#         print(f'{key}:{value}')

city_id = sorted(city_id.items(), key=lambda d: len(d[0]))
print(city_id)
# print(sorted(city_id.keys(), lambda x: len(x)))
