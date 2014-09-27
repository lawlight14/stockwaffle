from datetime import date, timedelta

def kstoday():
    tm = date.today()
    fulldate = date(tm.year, tm.month, tm.day)
    tfdate = fulldate + timedelta(hours=9)

    return tfdate

def ksyesterday():
	tm = kstoday()
	tfdate = date(tm.year, tm.month, tm.day-1)

	return tfdate

def ksbmonth():
	tm = kstoday()
	tfdate = date(tm.year, tm.month, 1) + timedelta(hours=-24)

	return tfdate