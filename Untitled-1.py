import datetime
today = datetime.date.today()
data = {'第二个百日计划': datetime.date(2024, 12, 19),
        '2025 新年': datetime.date(2025, 1, 1),
        '蛇年春节': datetime.date(2025, 1, 29),
        '2025 三战上岸': datetime.date(2025, 7, 1),
        '2027 全国高考': datetime.date(2027, 6, 7)
    }
s = '你好，CharonTree\n'
for key, val in data.items():
    s = s + '距离 ' + str(key) + ' 还有 ' + str((val - today).days) + ' 天\n'
s = s + '加油吧！'
print(s)