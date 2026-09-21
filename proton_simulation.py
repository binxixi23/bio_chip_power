"""
SBLC v2.0: Protonic Ice Gate - Grotthuss Cascade Latency Simulator
Author: Cuong Dang (binxixi23)

This script models the proton-hopping (hopping-turn) mechanism of water molecules 
confined inside ginseng-derived carbon nano-channels under space cryogenic 
conditions and varying electro-stabilization field intensities.
"""

import math
import time

class ProtonicIceChannel:
    def __init__(self, length_nm: float, diameter_nm: float, initial_temp_k: float):
        """
        Initializes a single nano-confined bio-hybrid ice wire.
        """
        self.length = length_nm
        self.diameter = diameter_nm
        self.temperature = initial_temp_k
        
        # Physical Constants
        self.H2O_SPACING_NM = 0.276  # Average distance between water molecules in Ice Ih
        self.kB = 1.380649e-23        # Boltzmann constant (J/K)
        self.h = 6.62607015e-34       # Planck constant (J*s)
        
        # Calculate number of water molecules aligned in the primary channel line
        self.num_molecules = max(1, math.ceil(self.length / self.H2O_SPACING_NM))
        
        # Ginseng Self-Doping Factor: mineral ions reduce the activation energy barrier
        # (Presence of K+, Ca2+, Na+ alters localized potential wells)
        self.activation_energy_base_ev = 0.18  # Base activation energy for proton hop in ice (eV)
        self.ginseng_doping_reduction_ev = 0.04 # Reduction due to bio-mineral doping
        self.Ea = (self.activation_energy_base_ev - self.ginseng_doping_reduction_ev) * 1.60218e-19 # Joules

    def calculate_hop_frequency(self, electric_field_v_per_m: float) -> float:
        """
        Calculates the proton hopping frequency per node using Arrhenius-Eyring Transition State Theory,
        modified by an external electro-stabilization/gate field.
        """
        # Dipole moment of water molecule in ice matrix (~3.0 Debye converted to Coulomb-meters)
        dipole_moment = 3.0 * 3.33564e-30 
        
        # Field contribution lowering the barrier in forward direction
        field_energy_bias = dipole_moment * electric_field_v_per_m
        effective_Ea = max(1e-22, self.Ea - field_energy_bias)
        
        # Eyring-Polanyi equation for reaction rate
        attempt_frequency = (self.kB * self.temperature) / self.h
        hop_rate_per_second = attempt_frequency * math.exp(-effective_Ea / (self.kB * self.temperature))
        
        return hop_rate_per_second

    def simulate_cascade(self, electric_field_v_per_m: float):
        """
        Simulates the total time taken for a proton cascade to propagate through the entire wire.
        """
        hop_rate = self.calculate_hop_frequency(electric_field_v_per_m)
        
        # Total latency = hop time per node * number of sequential molecular flips
        time_per_hop_seconds = 1.0 / hop_rate
        total_latency_seconds = time_per_hop_seconds * self.num_molecules
        
        # Calculate operational frequency threshold (Terahertz mapping)
        max_frequency_thz = (1.0 / total_latency_seconds) / 1e12
        
        print(f"--- SBLC v2.0 Channel Simulation Report ---")
        print(f"Channel Specs: {self.length} nm Length | {self.num_molecules} Molecules Aligned")
        print(f"Thermal State: {self.temperature} K (Deep Space Operating Point)")
        print(f"Applied Gate Field: {electric_field_v_per_m:.2e} V/m")
        print(f"Single Hop Latency: {time_per_hop_seconds * 1e15:.2f} femtoseconds")
        print(f"Total Cascade Latency: {total_latency_seconds * 1e12:.4f} picoseconds")
        print(f"Theoretical Max Processing Frequency: {max_frequency_thz:.2f} THz")
        print(f"--------------------------------------------\n")
        
        return total_latency_seconds

if __name__ == "__main__":
    # Test Configuration: A 5nm nano-confined gate operating at space background temps
    # with an active electro-stabilization gate voltage.
    space_gate = ProtonicIceChannel(length_nm=5.0, diameter_nm=1.5, initial_temp_k=150.0)
    
    # Simulate under standard standby field
    space_gate.simulate_cascade(electric_field_v_per_m=1.0e7)
    
    # Simulate under Accelerated Gate Overdrive Field
    space_gate.simulate_cascade(electric_field_v_per_m=5.0e8)
