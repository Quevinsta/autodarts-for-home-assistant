![Autodarts for Home Assistant](https://raw.githubusercontent.com/Quevinsta/autodarts-for-home-assistant/main/images/icon.png)

![GitHub release](https://img.shields.io/github/v/release/Quevinsta/autodarts-for-home-assistant)
![Downloads](https://img.shields.io/github/downloads/Quevinsta/autodarts-for-home-assistant/total)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Compatible-41BDF5?logo=home-assistant&logoColor=white)
![HACS](https://img.shields.io/badge/HACS-Custom-orange)
![License](https://img.shields.io/github/license/Quevinsta/autodarts-for-home-assistant)
![Stars](https://img.shields.io/github/stars/Quevinsta/autodarts-for-home-assistant?style=social)

# 🎯 Autodarts for Home Assistant

---

## 🇬🇧 English

### Overview
**Autodarts for Home Assistant** is a local Home Assistant integration for **Autodarts X01 systems**.

It provides **real-time dart game data** directly from Autodarts, without any cloud dependency.

---

### ✨ Features
- 🎯 Dart 1 / 2 / 3 with **S / D / T / M** notation  
- 🧾 Throw Summary (e.g. `T20 | T20 | D20`)
- ➕ Turn Total
- 🎯 Remaining score
- ✅ Checkout Possible (binary sensor)
- 🟢 Autodarts Status (online / offline)
- 🏆 Leg Won / ❌ Leg Lost (binary sensors)
- 🔒 Fully local (HTTP polling)

---

### 📦 Installation (HACS)
1. Go to **HACS → Integrations**
2. Add this repository as a **Custom Repository**
3. Search for **Autodarts for Home Assistant**
4. Install the integration
5. Restart Home Assistant

---

### ⚙️ Configuration
After installation:
1. Go to **Settings → Devices & Services**
2. Click **Add integration**
3. Search for **Autodarts**
4. Enter:
   - **Host** (IP address of Autodarts)
   - **Port** (default: `3180`)

---

### 🧠 Supported Game Modes
- X01 (501 / 301 / custom)

---

### 🧩 Sensors
- Dart 1 / 2 / 3
- Dart values
- Throw Summary
- Turn Total
- Remaining score
- Checkout Possible
- Autodarts Status
- Leg Won / Lost

---

### 🛠️ Troubleshooting
- Ensure Autodarts is running and reachable via browser
- Check Home Assistant logs for integration errors
- Restart Home Assistant after updates

---

### 📄 License
MIT License

---

## 🇳🇱 Nederlands

### Overzicht
**Autodarts for Home Assistant** is een lokale Home Assistant-integratie voor **Autodarts X01-systemen**.

De integratie toont **real-time dartinformatie** rechtstreeks vanuit Autodarts, zonder cloud of externe diensten.

---

### ✨ Functies
- 🎯 Pijl 1 / 2 / 3 met **S / D / T / M** notatie  
- 🧾 Worp samenvatting (bijv. `T20 | T20 | D20`)
- ➕ Beurt totaal
- 🎯 Resterende score
- ✅ Checkout mogelijk (binaire sensor)
- 🟢 Autodarts status (online / offline)
- 🏆 Leg gewonnen / ❌ Leg verloren
- 🔒 Volledig lokaal (HTTP polling)

---

### 📦 Installatie (HACS)
1. Ga naar **HACS → Integraties**
2. Voeg deze repository toe als **Custom Repository**
3. Zoek naar **Autodarts for Home Assistant**
4. Installeer de integratie
5. Herstart Home Assistant

---

### ⚙️ Configuratie
Na installatie:
1. Ga naar **Instellingen → Apparaten & Services**
2. Klik op **Integratie toevoegen**
3. Zoek naar **Autodarts**
4. Vul in:
   - **Host** (IP-adres van Autodarts)
   - **Poort** (standaard: `3180`)

---

### 🎯 Ondersteunde speltypen
- X01 (501 / 301 / aangepast)

---

### 📄 Licentie
MIT-licentie
