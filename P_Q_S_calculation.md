### Method 1: Calculating P, Q, and S Based on Sequence Components

#### 1. **Reconstruct Voltages and Currents**
The sequence components $V_{seq}$ and $I_{seq}$ (positive, negative, zero) are provided as real and imaginary parts. Combine them to reconstruct the complex phasors:

$$
V_{seq} = V_{seq,\text{real}} + j \cdot V_{seq,\text{img}}
$$
$$
I_{seq} = I_{seq,\text{real}} + j \cdot I_{seq,\text{img}}
$$

Where:
- $V_{seq}$: Voltage sequence components (positive, negative, zero).
- $I_{seq}$: Current sequence components (positive, negative, zero).
- $j$: Imaginary unit $\sqrt{-1}$.


#### 2. **Calculate Total Complex Power (S)**
Using the sequence components, calculate the total complex power $S$:

$$
S = 3 \cdot \left( V_{\text{pos}} \cdot I_{\text{pos}}^* + V_{\text{neg}} \cdot I_{\text{neg}}^* + V_{\text{zero}} \cdot I_{\text{zero}}^* \right)
$$

Where:
- $V_{\text{pos}}, V_{\text{neg}}, V_{\text{zero}}$: Voltages for the positive, negative, and zero sequences.
- $I_{\text{pos}}, I_{\text{neg}}, I_{\text{zero}}$: Currents for the positive, negative, and zero sequences.
- $^*$: Denotes the complex conjugate.


#### 3. **Calculate Active and Reactive Power**
Calculate the active power ($P$) and reactive power ($Q$) directly using the sequence components:

- **Active Power ($P$):**
  $$
  P = 3 \cdot \left( |V_{\text{pos}}| \cdot |I_{\text{pos}}| \cdot \cos(\phi_{\text{pos}}) + |V_{\text{neg}}| \cdot |I_{\text{neg}}| \cdot \cos(\phi_{\text{neg}}) + |V_{\text{zero}}| \cdot |I_{\text{zero}}| \cdot \cos(\phi_{\text{zero}}) \right)
  $$

- **Reactive Power ($Q$):**
  $$
  Q = 3 \cdot \left( |V_{\text{pos}}| \cdot |I_{\text{pos}}| \cdot \sin(\phi_{\text{pos}}) + |V_{\text{neg}}| \cdot |I_{\text{neg}}| \cdot \sin(\phi_{\text{neg}}) + |V_{\text{zero}}| \cdot |I_{\text{zero}}| \cdot \sin(\phi_{\text{zero}}) \right)
  $$

Where:
- $|V_{seq}|$: Magnitude of the voltage sequence components.
- $|I_{seq}|$: Magnitude of the current sequence components.
- $\phi_{seq}$: Phase angle difference between the voltage and current sequence components.


#### 4. **Calculate Apparent Power (S)**
The apparent power is the magnitude of the complex power:

$$
S = \sqrt{P^2 + Q^2}
$$


### Method 2: Calculating P, Q, and S Based on Voltage Current of Each Phase

#### 1. **Formulas**
For an unbalanced three-phase power system, the active power ($P$), reactive power ($Q$), and apparent power ($S$) for each phase are calculated as follows:

- **Active Power ($P_\phi$) for each phase:**
  $$
  P_\phi = V_{LN,\phi} \cdot I_\phi \cdot \cos(\phi_\phi)
  $$

- **Reactive Power ($Q_\phi$) for each phase:**
  $$
  Q_\phi = V_{LN,\phi} \cdot I_\phi \cdot \sin(\phi_\phi)
  $$

- **Apparent Power ($S_\phi$) for each phase:**
  $$
  S_\phi = \sqrt{(P_\phi)^2 + (Q_\phi)^2}
  $$

Where:
- $V_{LN,\phi}$: Line-to-neutral voltage for phase $\phi$ ($\phi = A, B, C$).
- $I_\phi$: Current magnitude for phase $\phi$.
- $\phi_\phi$: Phase angle difference between voltage and current for phase $\phi$.


#### 2. **Total Power for the System**
The total active, reactive, and apparent power for the system are the sum of the respective quantities for all three phases:

- **Total Active Power ($P$):**
  $$
  P = P_A + P_B + P_C
  $$

- **Total Reactive Power ($Q$):**
  $$
  Q = Q_A + Q_B + Q_C
  $$

- **Total Apparent Power ($S$):**
  $$
  S = \sqrt{P^2 + Q^2}
  $$