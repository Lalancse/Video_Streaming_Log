# Video_Streaming_Log

<p>
This repository provides video streaming logs collected under different
<strong>Adaptive Bitrate (ABR) algorithms</strong>, <strong>Congestion Control Algorithms (CCAs)</strong>,
and <strong>network conditions</strong>. The dataset is intended to facilitate the analysis of
video streaming <strong>Quality of Experience (QoE)</strong> and the behavior of different
transport-layer congestion control algorithms.
</p>

<p>
Two client-side ABR algorithms are considered:
</p>

<ul>
  <li><strong>BOLA</strong> (buffer-based ABR)</li>
  <li><strong>Throughput-based</strong> ABR</li>
</ul>

<hr />

<h2>Log Categories</h2>

<h3>1. <code>Paper_Video_Streaming_Log</code></h3>

<p>
These logs correspond to the experiments used in the research paper. The
following Congestion Control Algorithms were evaluated:
</p>

<ul>
  <li>BBR</li>
  <li>BBRv2</li>
  <li>Cubic</li>
  <li>Reno</li>
</ul>

<p>
Each CCA was evaluated under different bandwidth, buffer size, network delay,
and packet-loss conditions.
</p>

<h4>(a) Bandwidth Variations</h4>

<ul>
  <li>1 Mbps</li>
  <li>10 Mbps</li>
  <li>20 Mbps</li>
</ul>

<h4>(b) Buffer Sizes</h4>

<ul>
  <li>10 KB</li>
  <li>100 KB</li>
  <li>1 MB</li>
</ul>

<h4>(c) Network Delays</h4>

<ul>
  <li>100 ms</li>
  <li>200 ms</li>
  <li>300 ms</li>
</ul>

<h4>(d) Packet Loss Rates</h4>

<ul>
  <li>0%</li>
  <li>3%</li>
  <li>5%</li>
</ul>

<hr />

<h3>2. <code>Old_Video_Streaming_Log</code></h3>

<p>
These logs were collected using a separate experimental setup in which
<strong>Mahimahi</strong> was used to emulate the network environment.
The same CCAs—BBR, BBRv2, Cubic, and Reno—were evaluated.
</p>

<p>
The video bitrates are consistent with those used in the paper, and the
video duration for each experimental run is approximately
<strong>15 minutes</strong>.
</p>

<h4>(a) Packet Loss Variations</h4>

<ul>
  <li>1%</li>
  <li>3%</li>
  <li>5%</li>
  <li>7%</li>
  <li>10%</li>
</ul>

<h4>(b) Bandwidth Conditions with 0% Packet Loss</h4>

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
  <li><strong>BOLA</strong> — Buffer-based adaptive bitrate algorithm</li>
  <li><strong>Throughput-based</strong> — Throughput-based adaptive bitrate algorithm</li>
</ul>

<p>
Both log categories contain performance data obtained using these ABR
algorithms, allowing the QoE of different CCAs to be compared under
identical network conditions.
</p>

<img src="Dataset.png" alt="Flow of the video streaming log dataset" width="800">

<hr />

<h2>Mahimahi Network Emulation</h2>

<p>
The Mahimahi-based experiments use the
<strong>car.snaroya-smestad</strong> trace from the MMSys 2013
path-bandwidth trace collection.
</p>

<p>
<strong>Trace source:</strong><br>
<a href="https://skuld.cs.umass.edu/traces/mmsys/2013/pathbandwidth/car.snaroya-smestad/">
https://skuld.cs.umass.edu/traces/mmsys/2013/pathbandwidth/car.snaroya-smestad/
</a>
</p>

<p>
The trace provides separate uplink and downlink network conditions and is
used with Mahimahi's <code>mm-link</code> to reproduce
<strong>time-varying network conditions</strong>.
</p>

<h3>Trace Setup</h3>

<p>
Download the corresponding <code>.up</code> and <code>.down</code> trace files
and specify their locations in the experiment script:
</p>

<pre><code>UPLINK="/path/to/car-snaroya-smestad.up"
DOWNLINK="/path/to/car-snaroya-smestad.down"</code></pre>

<p>
The trace-driven network environment can be started using:
</p>

<pre><code>mm-link "$UPLINK" "$DOWNLINK" -- bash</code></pre>

<hr />

<h2>Network Configuration</h2>

<p>
In addition to Mahimahi's trace-driven emulation, Linux
<strong>tc/netem</strong> is used to introduce controlled network conditions,
including bandwidth limitation, network delay, and packet loss.
</p>

<p>
An example configuration used for the random packet-loss experiments is:
</p>

<ul>
  <li><strong>Rate:</strong> 20 Mbps</li>
  <li><strong>Delay:</strong> 100 ms</li>
  <li><strong>Packet loss:</strong> 3%</li>
  <li><strong>Packet-loss model:</strong> Random/independent</li>
  <li><strong>TBF buffer:</strong> 1500 bytes</li>
  <li><strong>TBF queue limit:</strong> 10 MB</li>
  <li><strong>NetEm queue limit:</strong> 7000 packets</li>
</ul>

<h3>tc/netem Configuration</h3>

<pre><code>sudo tc qdisc add dev ingress root handle 1: tbf \
    rate 20mbit \
    buffer 1500 \
    limit 10MB

sudo tc qdisc add dev ingress parent 1:1 handle 30: netem \
    limit 7000 \
    delay 100ms \
    loss random 3%</code></pre>

<hr />

<h2>Packet Loss Model</h2>

<p>
The original packet-loss experiments use:
</p>

<pre><code>loss random 3%</code></pre>

<p>
This configuration specifies a <strong>random/independent packet-loss model</strong>
with a nominal packet-loss probability of 3%. Therefore, the original
packet-loss experiments should be interpreted as evaluations under
<strong>uniform random packet-loss conditions</strong>.
</p>

<p>
Random packet loss does not fully represent wireless environments, where
packet losses may occur in bursts because of fading, interference, mobility,
and rapidly changing channel conditions.
</p>

<p>
To account for this behavior, additional experiments can use a
<strong>bursty packet-loss model</strong> to evaluate the CCAs under
temporally correlated loss conditions.
</p>

<hr />

<h2>Running the Video Streaming Experiment</h2>

<p>
The experimental setup consists of a <strong>Chromium Toy QUIC Server</strong>,
the <strong>DASH.js reference player</strong> running on the client side,
and a Python-based logger that collects DASH.js runtime statistics.
</p>

<h3>1. Start the Chromium Toy QUIC Server</h3>

<p>
The server is implemented using the <strong>Chromium Toy QUIC Server</strong>.
Navigate to the Chromium source directory (<code>depot_tools/src</code>) and
execute the <code>run-serve.sh</code> shell script:
</p>

<pre><code>./run-serve.sh</code></pre>

<p>
The <code>run-serve.sh</code> script contains the required server-side
commands and configurations. It also contains the commands required for
<strong>server-side logging</strong>.
</p>

<hr />

<h3>2. Start the DASH.js Development Server</h3>

<p>
Navigate to the <code>dash.js</code> directory and execute:
</p>

<pre><code>sudo npm run start</code></pre>

<p>
This starts the DASH.js development server and makes the DASH.js
reference player available through the local web server.
</p>

<hr />

<h3>3. Launch Chromium with QUIC Enabled</h3>

<p>
Open another terminal and execute:
</p>

<pre><code>chromium-browser \
    --user-data-dir=/tmp/chrome-profile \
    --no-proxy-server \
    --enable-quic \
    --origin-to-force-quic-on=www.example.org:443 \
    --host-resolver-rules='MAP www.example.org:443 192.168.31.86:6121' \
    --disable-web-security \
    http://localhost:3000/samples/dash-if-reference-player/index.html</code></pre>

<p>
The command enables QUIC in Chromium and maps
<code>www.example.org:443</code> to the Chromium Toy QUIC Server running
at:
</p>

<pre><code>192.168.31.86:6121</code></pre>

<p>
<strong>Note:</strong> The IP address <code>192.168.31.86</code> corresponds
to the server address used in our experimental setup. It should be replaced
with the appropriate server IP address when reproducing the experiment on
another system.
</p>

<hr />

<h3>4. Start the Client-Side Logger</h3>

<p>
The <code>logger.py</code> script is used to collect runtime information from
the DASH.js player. Run the logger and specify the desired output file name.
For example:
</p>

<pre><code>python3 logger.py BBR_3%_Bola_1</code></pre>

<p>
In this example:
</p>

<ul>
  <li><code>BBR</code> represents the congestion control algorithm.</li>
  <li><code>3%</code> represents the packet-loss rate.</li>
  <li><code>Bola</code> represents the client-side ABR algorithm.</li>
  <li><code>1</code> represents the experimental run number.</li>
</ul>

<p>
The logger collects DASH.js runtime statistics at an interval of
<strong>100 ms</strong>. These measurements are subsequently used to analyze
the behavior of the streaming session and calculate video streaming QoE.
</p>

<h4>DASH.js Logging Modification</h4>

<p>
To collect the required runtime statistics, modifications are made to the
DASH.js reference player's <code>main.js</code> file located at:
</p>

<pre><code>dash.js/samples/dash-if-reference-player/app/main.js</code></pre>

<p>
The modified code periodically obtains the required DASH.js player statistics,
which are then captured by <code>logger.py</code>.
</p>

<hr />

<h3>5. Load and Play the DASH Video</h3>

<p>
After launching the DASH.js reference player, enter the following DASH
manifest URL (<code>.mpd</code>) in the player's URL field:
</p>

<pre><code>https://www.example.org/output.mpd</code></pre>

<p>
Click <strong>Load</strong> to start the video playback.
The DASH client will request video segments from the Chromium Toy QUIC Server
while the client-side and server-side logging mechanisms collect the
corresponding experimental data.
</p>

<hr />

<h3>Complete Experiment Execution Sequence</h3>

<pre><code>1. Configure the Network Environment
              |
              v
2. Start the Chromium Toy QUIC Server
              |
              v
3. Start the DASH.js Development Server
              |
              v
4. Launch Chromium with QUIC Enabled
              |
              v
5. Start the Client-Side Logger
              |
              v
6. Enter the DASH Manifest URL
              |
              v
7. Load and Play the Video
              |
              v
8. Collect Client- and Server-Side Logs</code></pre>

<p>
Before reproducing the experiments, ensure that the
<strong>network interface, server IP address, server port, Mahimahi trace
paths, video manifest path, and output log paths</strong> are configured
according to the local system.
</p>

<hr />

<h2>Repository Structure</h2>

<pre><code>.
├── README.md
├── Dataset.png
├── run-server.sh
├── network_setup_random_loss.sh
├── Paper_Video_Streaming_Log/
└── Old_Video_Streaming_Log/</code></pre>

<hr />

<h2>Summary</h2>

<p>
This repository provides video streaming logs for analyzing the interaction
between <strong>Congestion Control Algorithms</strong>,
<strong>Adaptive Bitrate algorithms</strong>, and different
<strong>network conditions</strong>. The provided experiment configuration,
network emulation setup, execution procedure, and logging mechanism are
intended to support the reproducibility and further analysis of the reported
video streaming experiments.
</p>
