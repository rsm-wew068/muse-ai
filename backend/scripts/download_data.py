import os
import requests
import zipfile
import io

# We will use a subset of the AILab POP1k7 dataset or similar available via direct link.
# For stability, I will use a reliable mirror of specific MIDI files.
# Dataset: A collection of Pop/Rock MIDIs.

DATASET_URL = "https://github.com/asigalov61/Tegridy-MIDI-Dataset/raw/master/Tegridy-MIDI-Dataset-CC-BY-NC-SA.zip"
# Alternative: "https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip" (Classical)
# Let's try downloading from a reliable source. 
# actually, let's use a smaller repo to avoid timeouts.

def download_midi_dataset():
    target_dir = "../data/midi_dataset"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    print("Downloading MIDI dataset...")
    # This is a placeholder. For the demo, I will simulate downloading by creating 
    # a few complex MIDI files if the download fails, BUT let's try a real DL first.
    # Using a known repository of MIDI files.
    
    # Let's clone a small repo instead of a massive zip
    os.system(f"git clone https://github.com/ldzhangyx/POP909-Dataset {target_dir}/pop909")

if __name__ == "__main__":
    download_midi_dataset()
