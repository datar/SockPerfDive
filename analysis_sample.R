analysis.sample<-function(x){
  for (msg.size in 16*(1:92)){
    in.file = sprintf("20151230172940_udp_m%d.csv", msg.size)
    data = read.csv(in.file, header = FALSE)
    latency = data$V5/2000
    interval = 0.1
    latency.median = median(latency)
    latency.core.upper = latency.median*(1+interval)
    latency.core.lower = latency.median*(1-interval)
    latency.core = latency[latency<latency.core.upper & latency>latency.core.lower]
    text.exp = sprintf("sample ratio of core area:%f",length(latency.core)/length(latency))
    out.file = sprintf("20151230172940_udp_m%d_latency.jpg", msg.size)
    jpeg(file = out.file)
    hist(latency.core, breaks = 200)
    dev.off()
  }
}