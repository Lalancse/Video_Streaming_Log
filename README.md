# Video_Streaming_Log
<p>
This repository contains two types of video streaming logs, collected under different Adaptive Bitrate (ABR) algorithms — <strong>BOLA</strong> and <strong>Throughput-based</strong> — on the client side. The logs are intended for analysis of video streaming Quality of Experience (QoE) under various <strong>Congestion Control Algorithms (CCAs)</strong> and <strong>network conditions</strong>.
</p>

<h2>Log Categories</h2>

<h3>1. <code>Paper_Video_Streaming_Log</code></h3>
<p>
These logs were used in the research paper and cover experiments conducted with the following Congestion Control Algorithms:
</p>
<ul>
  <li>BBR</li>
  <li>BBRv2</li>
  <li>Cubic</li>
  <li>Reno</li>
</ul>

<p>Each CCA was evaluated under diverse network conditions:</p>

<p><strong>(a) Bandwidth Variations</strong></p>
<ul>
  <li>1 Mbps</li>
  <li>10 Mbps</li>
  <li>20 Mbps</li>
</ul>

<p><strong>(b) Buffer Sizes</strong></p>
<ul>
  <li>10 KB</li>
  <li>100 KB</li>
  <li>1 MB</li>
</ul>

<p><strong>(c) Network Delays</strong></p>
<ul>
  <li>100 ms</li>
  <li>200 ms</li>
  <li>300 ms</li>
</ul>

<p><strong>(d) Packet Loss Rates</strong></p>
<ul>
  <li>0%</li>
  <li>3%</li>
  <li>5%</li>
</ul>

<hr />

<h3>2. <code>Old_Video_Streaming_Log</code></h3>
<p>
These logs were collected in a separate setup using <strong>Mahimahi</strong> to emulate a virtual network environment. The same CCAs — BBR, BBRv2, Cubic, and Reno — were tested. The bitrate is consistent with that used in the paper, and the video duration for each log is <strong>15 minutes</strong>.
</p>

<p><strong>(a) Packet Loss Variations</strong></p>
<ul>
  <li>1%</li>
  <li>3%</li>
  <li>5%</li>
  <li>7%</li>
  <li>10%</li>
</ul>

<p><strong>(b) Bandwidth Conditions (with 0% packet loss)</strong></p>
<ul>
  <li>350 Kbps</li>
  <li>500 Kbps</li>
  <li>1 Mbps</li>
  <li>1.5 Mbps</li>
  <li>2 Mbps</li>
</ul>

<hr />

<h2>ABR Algorithms Used</h2>
<ul>
  <li><strong>BOLA</strong></li>
  <li><strong>Throughput-based</strong></li>
</ul>

<p>Both log sets include performance data for these ABR algorithms to compare QoE under identical network and CCA conditions.</p>

![This image show the flow of this log](Dataset.png)
