INPUT_LOG = "data.txt"
OUTPUT_LOG = "ssl_info.txt"

def get_unique_ssl_info(input_path: str, output_path: str):
    unique_pairs = set()

    with open(input_path, encoding="utf-8") as infile:
        for line in infile:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            protocol = parts[-2]
            cipher = parts[-1]
            unique_pairs.add((protocol, cipher))

    with open(output_path, "w", encoding="utf-8") as outfile:
        for protocol, cipher in sorted(unique_pairs):
            outfile.write(f"{protocol} {cipher}\n")

if __name__ == "__main__":
    get_unique_ssl_info(INPUT_LOG, OUTPUT_LOG)
