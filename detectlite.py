import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def signal_analyzer():
    print("Signal Analysis Framework")
    print("=" * 45)
    
    # System configuration
    sample_rate = 10000
    duration = 10.0
    pattern_length = 2.0
    freq_low, freq_high = 32, 256
    noise_factor = np.sqrt(2)
    
    # Time domain setup
    time_vector = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    pattern_time = np.linspace(0, pattern_length, int(sample_rate * pattern_length), endpoint=False)
    
    # Generate reference pattern
    reference_pattern = signal.chirp(pattern_time, freq_low, pattern_length, freq_high, method='linear')
    print(f"Reference pattern: {freq_low}-{freq_high} Hz across {pattern_length}s")
    
    # Random placement parameters
    max_offset = duration - pattern_length
    insertion_point = np.random.uniform(0, max_offset)
    
    # Background noise generation
    background = np.random.normal(0, noise_factor, len(time_vector))
    
    # Signal composition
    composite_signal = background.copy()
    insert_start = int(insertion_point * sample_rate)
    insert_end = insert_start + len(reference_pattern)
    composite_signal[insert_start:insert_end] += reference_pattern
    
    print(f"Pattern embedded at t = {insertion_point:.2f}s")
    
    # Cross-correlation analysis
    xcorr_result = np.correlate(composite_signal, reference_pattern, mode='full')
    
    # Peak detection
    max_index = np.argmax(xcorr_result)
    
    # Time axis reconstruction
    xcorr_time = np.linspace(-pattern_length, duration, len(xcorr_result))
    estimated_location = xcorr_time[max_index]
    
    # Performance metrics
    location_error = abs(estimated_location - insertion_point)
    
    print(f"ANALYSIS RESULTS:")
    print(f"   Actual location:     {insertion_point:.3f}s")
    print(f"   Estimated location:  {estimated_location:.3f}s")
    print(f"   Timing error:        {location_error*1000:.1f} ms")
    
    # Visualization framework
    fig, (plot1, plot2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Primary signal plot
    plot1.plot(time_vector, composite_signal, 'b-', alpha=0.7, linewidth=0.5)
    plot1.axvline(insertion_point, color='green', linestyle='--', linewidth=2, label=f'Actual: {insertion_point:.2f}s')
    plot1.axvline(estimated_location, color='red', linestyle='-', linewidth=2, label=f'Estimated: {estimated_location:.2f}s')
    plot1.set_title('Composite Signal Analysis')
    plot1.set_xlabel('Time (s)')
    plot1.set_ylabel('Amplitude')
    plot1.legend()
    plot1.grid(True, alpha=0.3)
    
    # Correlation analysis plot
    plot2.plot(xcorr_time, xcorr_result, 'purple', linewidth=1)
    plot2.plot(estimated_location, xcorr_result[max_index], 'ro', markersize=8, label='Peak Detection')
    plot2.set_title('Cross-Correlation Analysis')
    plot2.set_xlabel('Time Offset (s)')
    plot2.set_ylabel('Correlation Magnitude')
    plot2.legend()
    plot2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Performance evaluation
    if location_error < 0.1:
        print("EXCELLENT performance! Error < 100ms")
    elif location_error < 0.2:
        print("GOOD performance! Error < 200ms")
    else:
        print("Performance requires optimization")
    
    return insertion_point, estimated_location, location_error

if __name__ == "__main__":
    actual_pos, detected_pos, error = signal_analyzer()
    print(f"\nSignal analysis complete!")
    print(f"Final error: {error*1000:.1f} ms")