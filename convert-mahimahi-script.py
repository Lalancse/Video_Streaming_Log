INPUT_FILE = "car-snaroya-smestad.txt"
OUTPUT_FILE = "car-snaroya-smestad.up"

PACKET_SIZE_BYTES = 1500
PACKET_SIZE_BITS = PACKET_SIZE_BYTES * 8

timestamps = []
current_time_ms = 0

with open(INPUT_FILE, "r") as f:
    prev_line = None

    for line in f:
        if not line.strip():
            continue
        
        cols = line.split()
        
        bytes_recv = float(cols[4])
        delta_ms = float(cols[5])
        
        if delta_ms <= 0:
            continue
        
        # throughput in bits/sec
        bps = (bytes_recv * 8.0) / (delta_ms / 1000.0)
        
        packets_per_ms = bps / PACKET_SIZE_BITS / 1000.0
        
        total_packets = int(packets_per_ms * delta_ms)
        
        if total_packets <= 0:
            current_time_ms += delta_ms
            continue
        
        interval = delta_ms / total_packets
        
        for i in range(total_packets):
            ts = int(current_time_ms + i * interval)
            timestamps.append(ts)
        
        current_time_ms += delta_ms

# Write Mahimahi trace
with open(OUTPUT_FILE, "w") as f:
    for ts in timestamps:
        f.write(f"{ts}\n")

print("Mahimahi trace generated:", OUTPUT_FILE)
