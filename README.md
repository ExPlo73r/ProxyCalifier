# Proxy Califier

Archivo: fraudscan.py
Creador: Viernez13 
Comunidad: Cybeersecurity

---
 Descripción
Proxy Califier es una herramienta en Python que analiza un listado de direcciones IP usando la base pública de Scamalytics para identificar aquellas con un Fraud Score bajo, clasificándolas como seguras.

Incluye un banner ASCII de presentación al inicio.
<img width="1621" height="370" alt="image" src="https://github.com/user-attachments/assets/bf23be38-93b9-416e-8f7a-22d5269dc68e" />

---

 Características
- Procesa un listado de IPs desde un archivo.
- Consulta automáticamente el Fraud Score de cada IP.
- Filtra y muestra solo las IPs seguras.
- Exporta los resultados a un archivo CSV.
- Incluye control de tiempo entre consultas para evitar bloqueos.
- Código simple y fácil de extender.

---

 Requisitos
- Python 3.7 o superior
- Dependencias (ver `requirements.txt`)

Instalación de dependencias:
```bash
python3 -m pip install -r requirements.txt
```

---

 Estructura sugerida del proyecto
```
ProxyCalifier/
│
├── fraudscan.py         # Script principal
├── lista.txt            # Archivo con IPs a evaluar (una por línea)
├── requirements.txt     # Dependencias de Python
└── README.md            # Documentación
```

---

Formato del archivo de IPs "lñista.txt"
- Una IP por línea.
- Puedes comentar líneas con #.

Ejemplo:
```
8.8.8.8
1.1.1.1
# 192.168.0.1 -> ignorada
```

---

Uso
1. Guarda las IPs en un archivo (por ejemplo `lista.txt`).
2. Ejecuta el script:
   ```bash
   python3 fraudscan.py lista.txt --max-score 10 --salida ips_seguras.csv
   ```
3. Parámetros:
   - `archivo_ips`: Ruta al archivo con IPs.
   - `--max-score`: Máximo Fraud Score para considerar “seguro” (por defecto: 10).
   - `--salida`: Archivo CSV de salida (por defecto: `ips_seguras.csv`).
   - `--delay`: Segundos de espera entre consultas (por defecto: 1.5).

---

 Ejemplo
```bash
python3 fraudscan.py lista.txt --max-score 15 --delay 2
```
Salida:
```
[SEGURO] 8.8.8.8 -> 5/100
[RIESGO] 1.1.1.1 -> 70/100

Hecho. 1/2 IPs seguras (≤ 15).
CSV: /ruta/completa/ips_seguras.csv
```

---

 Salida CSV
```
ip,fraud_score
8.8.8.8,5
```

---
Notas importantes
- El script hace scraping de Scamalytics; si el HTML cambia, habrá que ajustar la expresión regular usada para extraer el puntaje.
- Respetar los términos de uso del servicio utilizando `--delay` para espaciar las consultas.
- Para uso intensivo o integraciones, se recomienda la API oficial de Scamalytics.

---

Licencia
Uso libre para la Comunidad Cybeersecurity.
Mantener créditos a Viernez13 como creador. Consulte `LICENSE.txt` para más detalles.
