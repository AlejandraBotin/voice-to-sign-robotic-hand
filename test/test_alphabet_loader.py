# test_alphabet_loader.py
from alphabet import load_alphabet, get_pose

PATH = "Alphabet.xlsx"   

data = load_alphabet(PATH)

print("OK: archivo leído")
print("Filas:", len(data.df))
print("Columnas:", list(data.df.columns))
print("Ejemplo mapping keys (primeros 10):", list(data.mapping.keys())[:10])

# Prueba una letra que exista en tu Excel
fingers, wrist = get_pose(data.mapping, "A")
print("A -> fingers:", fingers, "wrist:", wrist)

# Checks básicos (si algo peta aquí, está mal)
assert len(fingers) == 5, "Deben ser 5 dedos"
assert all(isinstance(x, int) for x in fingers), "Dedos deben ser int"
assert isinstance(wrist, int), "Wrist debe ser int"

print("✅ Todo bien.")