SockPerf Note
=========================

## Code

### Defs.h
Constants and many magic numbers.

### SockPerf.cpp

This is the entry of sockperf. There are more than 3000 lines in this file. The `main()` function is too long. That's ridiclouce. 

The first parameter after sockperf is **mode** like pingpong server. Each mode has its function, like this
```
static int proc_mode_help( int, int, const char ** );
static int proc_mode_version( int, int, const char ** );
static int proc_mode_under_load( int, int, const char ** );
static int proc_mode_ping_pong( int, int, const char ** );
static int proc_mode_throughput( int, int, const char ** );
static int proc_mode_playback( int, int, const char ** );
static int proc_mode_server( int, int, const char ** );
```

The cmdline `sockperf server` will go into `function proc_mode_server()`. A struct `app_modes` was used to store modes' name, shortname, function. 

The most interest thing is how they project mode name to function. They use a C-style array of struct `app_mode`. And how they check the end of array? They and a magic item whose all memebers are Null. They traversal the array util they get a wholl Null member struct. Sound like they use the C-style string. But why they didn't use some high level data structure like map? They use OOD in many classes.   



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