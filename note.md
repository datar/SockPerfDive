SockPerf Note
=========================

## Code

### ticks_os.h
Improving the function in ticks.h in windows system. using `QueryPerformanceFrequency()` and `QueryPerformanceCounter()` for max accuracy.

**TSC** means timestamp count

#### `os_gettimeoftsc()`
nano second is the time unit.
return how many nano second system has run.

In Linux system, they use **rdtsc** function. 
[A discussion on stackoverflow](http://stackoverflow.com/questions/8602336/getting-cpu-cycles-using-rdtsc-why-does-the-value-of-rdtsc-always-increase) said there are some problem to use it:

1. CPU frquency could change in modern CPU
2. it's not a thread safe method
3. In multi core CPU, it will reture different values


#### `os_ts_gettimeofclock()`
get system timestamp and transfer it to a strct timespec. return this struct.

#### `os_gettimeofclock()`
transfer a timespec struct to nanosecond count

**I don't know why they need these two functions `os_gettimeofclock()` and `os_ts_gettimeofclock()`. These functions just do what os_gettimeoftsc() does.**


### ticks.h