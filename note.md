# SockPerf Note

## Code

### Go Through
#### ticks_os.h
improving the function in ticks.h in windows system. using QueryPerformanceFrequency() and QueryPerformanceCounter() for max accuracy.

**TSC** means timestamp count

* os_gettimeoftsc()
nano second is the time unit.
return how many nano second system has run.

In Linux system, they use **rdtsc** function. 
[A discussion on stackoverflow](http://stackoverflow.com/questions/8602336/getting-cpu-cycles-using-rdtsc-why-does-the-value-of-rdtsc-always-increase) said there are some problem to use it:
1. CPU frquency could change in modern CPU
2. it's not a thread safe method
3. In multi core CPU, it will reture different values


* 