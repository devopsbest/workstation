import arrow

a = arrow.now()
b = arrow.utcnow()
print(a)
print(b)
# result:
# 2018-09-13T00:12:26.560750+08:00
# 2018-09-12T16:12:26.561425+00:00

# 将时间戳转化为arrow对象    arrow.get(timestamp)
print(arrow.get(1519534533))
# 结果：2018-02-25T04:55:33+00:00
# 将字符串转换为arrow对象  arrow.get(string[,format_string])
arrow.get('2018-02-24 12:30:45', 'YYYY-MM-DD HH:mm:ss')

print(a.datetime)
print(a.timestamp)
print(a.tzinfo)
print(a.datetime.hour)
print(a.datetime.day)
print(a.datetime.month)
print(a.date().day)
print(a.date().month)
print(a.date().year)

# 时间推移    a.shift(**kwargs)
# shift方法获取某个时间之前或之后的时间,关键字参数为years,months,weeks,days,hours，seconds，microseconds

result = a.shift(days=-1)
result2 = a.shift(months=-1)
print(result2)

# 格式化输出    a.format([format_string])
print(a.format())
print(a.format('YYYY-MM-DD HH:mm:ss ZZ'))
