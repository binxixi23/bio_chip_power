import random
import time

class BioChipChannel:
    def __init__(self, channel_id, is_reserve=False):
        self.channel_id = channel_id
        self.is_reserve = is_reserve
        self.is_active = not is_reserve
        self.status = "HEALTHY" # HEALTHY, CONGESTED, FAILED
        self.queue_load = 0

    def process_data(self, data_packets):
        if self.status == "FAILED":
            print(f"❌ [Channel {self.channel_id}] CRITICAL: Cosmic ray corruption detected!")
            return False
        
        self.queue_load += data_packets
        if self.queue_load > 80:
            self.status = "CONGESTED"
            print(f"⚠️ [Channel {self.channel_id}] Traffic Jam! Queue Load at {self.queue_load}%")
        else:
            self.status = "HEALTHY"
            print(f"⚡ [Channel {self.channel_id}] Oscillating charge at near-light speed. Load: {self.queue_load}%")
        
        # Simulate processing clearing the queue
        self.queue_load = max(0, self.queue_load - 40)
        return True

class SBLCSystem:
    def __init__(self):
        # 95% Active Cores, 5% Shield/Reserve Cores modeled simply
        self.active_pool = [BioChipChannel(i) for i in range(1, 4)]
        self.reserve_pool = [BioChipChannel(i, is_reserve=True) for i in range(4, 6)]

    def handle_traffic_routing(self, inbound_data):
        print(f"\n--- New Data Stream Incoming: {inbound_data} Packets ---")
        
        # Simulate an unexpected cosmic event causing random channel failure
        if random.random() < 0.2:
            corrupted_core = random.choice(self.active_pool)
            corrupted_core.status = "FAILED"

        for channel in self.active_pool:
            if channel.status == "FAILED":
                # Trigger the 5% Reserve "Soccer Sub" Logic
                if self.reserve_pool:
                    sub_core = self.reserve_pool.pop(0)
                    sub_core.is_active = True
                    sub_core.status = "HEALTHY"
                    print(f"🔄 [5% Reserve System] Swapping out Core {channel.channel_id}. Core {sub_core.channel_id} is entering the field!")
                    
                    # Replace the failed core in the active loop
                    self.active_pool.remove(channel)
                    self.active_pool.append(sub_core)
                    sub_core.process_data(inbound_data)
                else:
                    print("🚨 [5% Reserve System] Out of reserve cores! Systems overflowing!")
            else:
                # Normal Dynamic Routing / Deflection Routing
                if channel.status == "CONGESTED":
                    print(f"🔀 [Deflection Routing] Rerouting a portion of traffic away from Core {channel.channel_id}")
                    channel.process_data(inbound_data // 2)
                else:
                    channel.process_data(inbound_data)

# Run a brief 3-cycle test of your architecture
system = SBLCSystem()
for cycle in range(3):
    traffic = random.randint(30, 90)
    system.handle_traffic_routing(traffic)
    time.sleep(1)
