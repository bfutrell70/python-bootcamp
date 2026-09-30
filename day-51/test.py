import speedtest

st = speedtest.Speedtest(secure=True)

ds = int(st.download())
us = int(st.upload())
print(ds)
print(us)

# print(st.results)