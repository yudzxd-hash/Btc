import pandas as pd
import pandas_ta as ta
import yfinance as yf
from datetime import datetime, timedelta

# --- PENGATURAN STRATEGI ---
# Anda bisa mengubah parameter ini untuk eksperimen
# Contoh: 'BBCA.JK' (BCA), 'TLKM.JK' (Telkom), 'BTC-USD' (Bitcoin), 'ETH-USD' (Ethereum)
TICKER = 'BTC-USD' 
START_DATE = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d') # Data 1 tahun terakhir
TIME_INTERVAL = '1d' # '1d' untuk harian, '1h' untuk per jam
SHORT_MA_PERIOD = 20  # Periode MA jangka pendek
LONG_MA_PERIOD = 50   # Periode MA jangka panjang

def get_market_data(ticker, start_date, interval):
    """
    Mengunduh data pasar historis dari Yahoo Finance.
    """
    print(f"Mengunduh data untuk {ticker}...")
    data = yf.download(ticker, start=start_date, interval=interval)
    if data.empty:
        print(f"Tidak ada data yang ditemukan untuk ticker {ticker}. Coba ganti ticker.")
        return None
    print("Data berhasil diunduh.")
    return data

def apply_strategy(df):
    """
    Menerapkan strategi Moving Average Crossover dan menghasilkan sinyal.
    """
    if df is None:
        return None
        
    print(f"Menerapkan strategi MA Crossover (SMA {SHORT_MA_PERIOD} / SMA {LONG_MA_PERIOD})...")
    
    # Hitung Simple Moving Average (SMA) menggunakan pandas-ta
    df.ta.sma(length=SHORT_MA_PERIOD, append=True)
    df.ta.sma(length=LONG_MA_PERIOD, append=True)
    
    # Ganti nama kolom agar lebih mudah dibaca
    df.rename(columns={f'SMA_{SHORT_MA_PERIOD}': 'SMA_short', f'SMA_{LONG_MA_PERIOD}': 'SMA_long'}, inplace=True)

    # Buang baris yang tidak memiliki data MA lengkap
    df.dropna(inplace=True)

    print("Mencari sinyal crossover...")
    # Membuat kolom 'signal'
    # Inisialisasi dengan 0 (tidak ada sinyal)
    df['signal'] = 0

    # Sinyal BELI (1): Ketika SMA pendek memotong ke ATAS SMA panjang
    # Kondisi 1: SMA pendek hari ini > SMA panjang hari ini
    # Kondisi 2: SMA pendek kemarin < SMA panjang kemarin
    buy_condition = (df['SMA_short'] > df['SMA_long']) & (df['SMA_short'].shift(1) < df['SMA_long'].shift(1))
    df.loc[buy_condition, 'signal'] = 1

    # Sinyal JUAL (-1): Ketika SMA pendek memotong ke BAWAH SMA panjang
    # Kondisi 1: SMA pendek hari ini < SMA panjang hari ini
    # Kondisi 2: SMA pendek kemarin > SMA panjang kemarin
    sell_condition = (df['SMA_short'] < df['SMA_long']) & (df['SMA_short'].shift(1) > df['SMA_long'].shift(1))
    df.loc[sell_condition, 'signal'] = -1
    
    return df

def main():
    """
    Fungsi utama untuk menjalankan bot.
    """
    # 1. Dapatkan data pasar
    market_data = get_market_data(TICKER, START_DATE, TIME_INTERVAL)
    
    # 2. Terapkan strategi untuk mendapatkan sinyal
    signals_df = apply_strategy(market_data)
    
    if signals_df is not None:
        # 3. Tampilkan hanya baris di mana sinyal terjadi
        recent_signals = signals_df[signals_df['signal'] != 0]

        if recent_signals.empty:
            print("\nTidak ada sinyal Beli/Jual yang ditemukan dalam periode waktu yang ditentukan.")
        else:
            print("\n--- SINYAL TRADING DITEMUKAN ---")
            for index, row in recent_signals.iterrows():
                signal_type = "BELI (BUY)" if row['signal'] == 1 else "JUAL (SELL)"
                print(f"Tanggal: {index.date()} | Sinyal: {signal_type} | Harga Penutupan: ${row['Close']:.2f}")
            
            # Tampilkan sinyal terakhir
            last_signal_row = recent_signals.iloc[-1]
            last_signal_type = "BELI (BUY)" if last_signal_row['signal'] == 1 else "JUAL (SELL)"
            print("\n--- Sinyal Terakhir ---")
            print(f"Aset: {TICKER}")
            print(f"Tanggal: {last_signal_row.name.date()}")
            print(f"Sinyal: {last_signal_type}")
            print(f"Harga Saat Sinyal: ${last_signal_row['Close']:.2f}")
            print(f"SMA Pendek: {last_signal_row['SMA_short']:.2f} | SMA Panjang: {last_signal_row['SMA_long']:.2f}")


if __name__ == "__main__":
    main()