import os
import glob
import subprocess

def main():
    # Define paths (Must be Absolute paths)
    rtklib_path = r'C:\Users\User\RTKLIB-demo5-demo5\bin'
    convbin_path = os.path.join(rtklib_path, 'convbin.exe')

    # Define data directories
    data_dir = os.path.abspath('Data')
    raw_dir = os.path.join(data_dir, 'Raw')
    rinex_dir = os.path.join(data_dir, 'Rinex')
    
    # Create RINEX directory if it doesn't exist
    if not os.path.exists(rinex_dir):
        os.makedirs(rinex_dir)
    
    print("=== UBX to RINEX Batch Processing ===")
    
    # Step 1: Find all UBX files
    print("Step 1: Finding UBX files...")
    ubx_files = find_ubx_files(raw_dir)
    print(f"Found {len(ubx_files)} UBX files")
    
    # Step 2: Convert all UBX files to RINEX
    print("\nStep 2: Converting UBX files to RINEX...")
    rinex_files = []
    for ubx_file in ubx_files:
        try:
            obs_file = convert_ubx_to_rinex(ubx_file, rinex_dir, convbin_path)
            if obs_file and os.path.exists(obs_file):
                rinex_files.append(obs_file)
                print(f"✓ Converted: {os.path.basename(ubx_file)}")
            else:
                print(f"✗ Failed: {os.path.basename(ubx_file)}")
        except Exception as e:
            print(f"✗ Error converting {os.path.basename(ubx_file)}: {e}")
    
    print(f"Successfully converted {len(rinex_files)} files to RINEX")
    
    
def find_ubx_files(raw_dir):
    """Find all .ubx files in the Raw directory"""
    if not os.path.exists(raw_dir):
        raise FileNotFoundError(f"Raw directory not found: {raw_dir}")
    
    ubx_pattern = os.path.join(raw_dir, "*.ubx")
    ubx_files = glob.glob(ubx_pattern)
    
    return sorted(ubx_files)


def convert_ubx_to_rinex(ubx_file, rinex_dir, convbin_path):
    """Convert a single UBX file to RINEX format"""
    base_name = os.path.splitext(os.path.basename(ubx_file))[0]
    obs_file = os.path.join(rinex_dir, f'{base_name}.obs')
    nav_file = os.path.join(rinex_dir, f'{base_name}.nav')
    sbs_file = os.path.join(rinex_dir, f'{base_name}.sbs')
    
    # Command to convert UBX to RINEX
    command = [
        convbin_path, '-r', 'ubx', '-y', 'J,S,C', 
        '-o', obs_file, '-n', nav_file, '-s', sbs_file, 
        ubx_file
    ]
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return obs_file if os.path.exists(obs_file) else None
    except subprocess.CalledProcessError as e:
        print(f"Error running convbin: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return None
    

if __name__ == "__main__":
    main()