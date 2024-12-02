from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import random

app = FastAPI()

# Obsługa plików statycznych (serwowanie HTML, JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")


class Points(BaseModel):
    A: tuple
    B: tuple
    P: tuple


def wyznacznik_macierzy(A, B, P):
    return A[0] * B[1] + B[0] * P[1] + P[0] * A[1] - P[0] * B[1] - A[0] * P[1] - B[0] * A[1]


def iloczyn_wektorowy(A, B, P):
    # A, B, P to krotki z współrzędnymi np. (x_A, y_A)
    x_A, y_A = A
    x_B, y_B = B
    x_P, y_P = P

    # Obliczenie różnic współrzędnych
    delta_x_AB = x_B - x_A
    delta_y_AB = y_B - y_A
    delta_x_AP = x_P - x_A
    delta_y_AP = y_P - y_A

    # Obliczenie iloczynu wektorowego
    iloczyn_wektorowy = delta_x_AB * delta_y_AP - delta_x_AP * delta_y_AB

    return iloczyn_wektorowy


@app.get("/losuj-wspolrzedne")
def losuj_wspolrzedne():
    A = (random.uniform(-100, 100), random.uniform(-100, 100))
    B = (random.uniform(-100, 100), random.uniform(-100, 100))
    P = (random.uniform(-100, 100), random.uniform(-100, 100))
    return {"A": A, "B": B, "P": P}


@app.post("/sprawdz-punkt")
def sprawdz_punkt(points: Points):
    wynik_det = wyznacznik_macierzy(points.A, points.B, points.P)
    wynik_vec = iloczyn_wektorowy(points.A, points.B, points.P)
    roznica = wynik_det - wynik_vec

    message = ""
    if wynik_det > 0:
        message = "Punkt P znajduje się po prawej stronie odcinka AB."
    elif wynik_det < 0:
        message = "Punkt P znajduje się po lewej stronie odcinka AB."
    else:
        message = "Punkt P leży na odcinku AB."

    return {
        "wyznacznik_macierzy": wynik_det,
        "iloczyn_wektorowy": wynik_vec,
        "roznica": roznica,
        "message": message
    }


# Serwowanie pliku index.html na żądanie GET
@app.get("/")
def read_index():
    return FileResponse('static/index.html')
