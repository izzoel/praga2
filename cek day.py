from datetime import datetime

# If today is Friday (0 = Mon, 1 = Tue, 2 = Wen ...)
# if datetime.today().weekday() == 4:
#
if  datetime(2023, 5, 19).weekday() == 4:
    print("Yes, Today is Friday")
else:
    print("Nope...")