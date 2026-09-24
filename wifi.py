import subprocess

# Get saved Wi-Fi profiles
profiles = subprocess.check_output(
    "netsh wlan show profiles",
    shell=True
).decode()

# Extract profile names
names = [
    line.split(":")[1].strip()
    for line in profiles.split("\n")
    if "All User Profile" in line
]

# Display profiles
print("\nSaved Wi-Fi Networks:\n")

for i, name in enumerate(names, 1):
    print(f"[{i}] {name}")

# Let the user select a network
choice = int(input("\nChoose WiFi number: "))

if 1 <= choice <= len(names):
    wifi = names[choice - 1]
    print(f"\nSelected Wi-Fi: {wifi}")
else:
    print("Invalid choice.")