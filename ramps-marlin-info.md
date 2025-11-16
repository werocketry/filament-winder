# RAMPS / Marlin — Winder driver settings (concise)

This document collects stepper microstepping and current settings used on the winder (RAMPS + A4988 and TB6600 drivers). All wiring and switch/jumper states below are retained from the original notes.

**Quick wiring (RAMPS sockets → function):**

- `X` → Carriage (linear X axis)
- `Y` → Mandrel rotation (rotary A axis, axis ∥ X)
- `Z` → Eye tilt pivot (rotary B axis, axis ∥ Y)

---

## A4988 on RAMPS (MS1 / MS2 / MS3)

- RAMPS jumpers pull the A4988 MS pins HIGH when installed; no jumper = LOW (A4988 internal pulldown).

Microstep table (MS1, MS2, MS3):

| Mode      |    MS1    |    MS2    |    MS3    |
| --------- | :-------: | :-------: | :-------: |
| Full (1×) | OFF (LOW) | OFF (LOW) | OFF (LOW) |
| 1/2       | ON (HIGH) | OFF (LOW) | OFF (LOW) |
| 1/4       | OFF (LOW) | ON (HIGH) | OFF (LOW) |
| 1/8       | ON (HIGH) | ON (HIGH) | OFF (LOW) |
| 1/16      | ON (HIGH) | ON (HIGH) | ON (HIGH) |

References: Pololu A4988 docs and common RAMPS/A4988 tutorials.

---

## TB6600 DIP switches (SW1–SW6)

Most TB6600-style modules (e.g., TB67S109AFTG variants) use SW1–SW3 for microstepping and SW4–SW6 for current. Tables below show positions and corresponding resolution/current.

Microstepping (SW1, SW2, SW3):

| SW1 | SW2 | SW3 | Microstep    | Pulses/rev |
| --: | --: | --: | :----------- | ---------: |
|  ON |  ON |  ON | NC           |         NC |
|  ON |  ON | OFF | Full (1×)    |        200 |
|  ON | OFF |  ON | 1/2 (mode A) |        400 |
| OFF |  ON |  ON | 1/2 (mode B) |        400 |
|  ON | OFF | OFF | 1/4          |        800 |
| OFF |  ON | OFF | 1/8          |       1600 |
| OFF | OFF |  ON | 1/16         |       3200 |
| OFF | OFF | OFF | 1/32         |       6400 |

Current (SW4, SW5, SW6) — RMS / Peak:

| SW4 | SW5 | SW6 | RMS (A) | Peak (A) |
| --: | --: | --: | ------: | -------: |
|  ON |  ON |  ON |     0.5 |      0.7 |
|  ON | OFF |  ON |     1.0 |      1.2 |
|  ON |  ON | OFF |     1.5 |      1.7 |
|  ON | OFF | OFF |     2.0 |      2.2 |
| OFF |  ON |  ON |     2.5 |      2.7 |
| OFF | OFF |  ON |     2.8 |      2.9 |
| OFF |  ON | OFF |     3.0 |      3.2 |
| OFF | OFF | OFF |     3.5 |      4.0 |

Sources: MakerGuides TB6600 tutorial, vendor datasheets and unit silkscreen markings.

---

## Recommended / recorded per-axis settings

- **Z socket — Axis B (eye tilt pivot) — A4988**

  - MS1: ON, MS2: ON, MS3: ON → 1/16 microstepping

- **Y socket — Axis A (mandrel rotation) — TB6600**

  - SW1: OFF, SW2: OFF, SW3: ON → 1/16 microstepping
  - SW4: OFF, SW5: OFF, SW6: ON → 2.8 A RMS (2.9 A peak)

- **X socket — Axis X (linear carriage) — TB6600**
  - SW1: OFF, SW2: OFF, SW3: ON → 1/16 microstepping
  - SW4: OFF, SW5: ON, SW6: ON → 2.5 A RMS (2.7 A peak)
