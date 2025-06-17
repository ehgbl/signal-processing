import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def signal_analyzer():
    print("Signal Analysis Framework")
    print("=" * 45)
    
    #parameters
    sample_rate = 10000
    duration = 10.0
    pattern_length = 2.0
    freq_low, freq_high = 32, 256
    noise_factor = np.sqrt(2)
    
    #time vectors for full signal and pattern
    time_vector = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    pattern_time = np.linspace(0, pattern_length, int(sample_rate * pattern_length), endpoint=False)
    
    
    reference_pattern = signal.chirp(pattern_time, freq_low, pattern_length, freq_high, method='linear')
    print(f"Reference pattern: {freq_low}-{freq_high} Hz across {pattern_length}s")
    
    #Random start 
    max_offset = duration - pattern_length
    insertion_point = np.random.uniform(0, max_offset)
    
    background = np.random.normal(0, noise_factor, len(time_vector))
    
    composite_signal = background.copy()
    insert_start = int(insertion_point * sample_rate)
    insert_end = insert_start + len(reference_pattern)
    composite_signal[insert_start:insert_end] += reference_pattern
    xcorr_result = np.correlate(composite_signal, reference_pattern, mode='full')
    
    max_index = np.argmax(xcorr_result)
    
    # time axis for cross-correlation

    xcorr_time = np.linspace(-pattern_length, duration, len(xcorr_result))
    estimated_location = xcorr_time[max_index]
    
    # print performance evaluation

    location_error = abs(estimated_location - insertion_point)
    plt.tight_layout()
    plt.show()
    
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