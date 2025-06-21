import hashlib
import time

def mine(block_number, transactions, previous_hash, prefix_zeros):
    """
    Fungsi simulasi untuk menambang sebuah blok.

    Args:
        block_number (int): Nomor blok saat ini.
        transactions (str): Transaksi-transaksi di dalam blok.
        previous_hash (str): Hash dari blok sebelumnya.
        prefix_zeros (int): Tingkat kesulitan (jumlah angka nol di awal hash).

    Returns:
        tuple: Hash yang valid dan nonce yang ditemukan.
    """
    prefix_str = '0' * prefix_zeros
    nonce = 0
    
    print(f"\nMemulai penambangan untuk Blok #{block_number}...")
    print(f"Tingkat kesulitan: Mencari hash yang diawali dengan {prefix_str}")
    
    start_time = time.time()

    while True:
        # 1. Gabungkan semua data blok + nonce
        text_to_hash = str(block_number) + transactions + previous_hash + str(nonce)
        
        # 2. Lakukan hashing menggunakan SHA-256
        new_hash = hashlib.sha256(text_to_hash.encode()).hexdigest()
        
        # 3. Cek apakah hash memenuhi syarat kesulitan (diawali dengan '0' sejumlah prefix_zeros)
        if new_hash.startswith(prefix_str):
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            print(f"\n--- BLOK DITEMUKAN! ---")
            print(f"Nonce yang ditemukan: {nonce}")
            print(f"Hash yang valid    : {new_hash}")
            print(f"Waktu yang dibutuhkan: {elapsed_time:.4f} detik")
            print(f"Total hash dicoba    : {nonce + 1}")
            
            return new_hash, nonce
            
        # 4. Jika tidak, coba nonce berikutnya
        nonce += 1

# --- DATA SIMULASI ---
if __name__ == '__main__':
    # Tingkat kesulitan (coba ubah angka ini dari 3, 4, 5, atau 6 untuk melihat perbedaannya)
    # Kesulitan di jaringan Bitcoin asli setara dengan sekitar 18-20+ angka nol!
    difficulty = 5 
    
    # Data blok dummy
    block_data = {
        'block_number': 849001,
        'transactions': "Alice mengirim 1 BTC ke Bob, Charlie mengirim 0.5 BTC ke David",
        'previous_hash': '00000000000000000002a7b450b73f8a0c24a64e1b0f69f0b1f1d1e2e3d4f5g6'
    }

    # Mulai simulasi mining
    mined_hash, mined_nonce = mine(
        block_number=block_data['block_number'],
        transactions=block_data['transactions'],
        previous_hash=block_data['previous_hash'],
        prefix_zeros=difficulty
    )