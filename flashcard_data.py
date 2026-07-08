PRELOADED_DECKS = {
    "JEE": {
        "Physics": {
            "Mechanics": [
                {
                    "question": "State the work-energy theorem.",
                    "answer": "The net work done by all forces acting on a particle equals its change in kinetic energy."
                },
                {
                    "question": "Formula for terminal velocity of a sphere dropping in viscous fluid.",
                    "answer": "v = (2r^2 * (rho - sigma) * g) / (9 * eta)"
                },
                {
                    "question": "Define conservative forces.",
                    "answer": "Forces where work done depends only on initial and final positions, not on the path taken."
                },
                {
                    "question": "State Kepler's third law of planetary motion.",
                    "answer": "The square of the orbital period is proportional to the cube of the semi-major axis: T^2 alpha r^3."
                },
                {
                    "question": "Formula for acceleration due to gravity at depth 'd'.",
                    "answer": "g_d = g * (1 - d/R)"
                },
                {
                    "question": "What is the velocity of a particle at the highest point of a projectile motion?",
                    "answer": "v = u * cos(theta), directed horizontally."
                },
                {
                    "question": "Define the coefficient of restitution (e).",
                    "answer": "e = (Velocity of separation) / (Velocity of approach)"
                },
                {
                    "question": "What is the relation between torque and angular momentum?",
                    "answer": "Torque = dL/dt (Rate of change of angular momentum)"
                },
                {
                    "question": "State the parallel axes theorem for moment of inertia.",
                    "answer": "I = I_cm + M * d^2"
                },
                {
                    "question": "State the perpendicular axes theorem for planar objects.",
                    "answer": "I_z = I_x + I_y"
                },
                {
                    "question": "Formula for escape velocity from Earth's surface.",
                    "answer": "v_e = sqrt(2 * G * M / R)"
                },
                {
                    "question": "What is the variation of gravity with altitude 'h' (where h << R)?",
                    "answer": "g_h = g * (1 - 2h/R)"
                },
                {
                    "question": "Define conservative field condition via potential energy gradient.",
                    "answer": "F = -dU/dr"
                },
                {
                    "question": "Time period of a simple pendulum of length L.",
                    "answer": "T = 2 * pi * sqrt(L / g)"
                },
                {
                    "question": "Condition for pure rolling of a sphere on a flat surface.",
                    "answer": "v = omega * R and a = alpha * R at the contact point."
                },
                {
                    "question": "Work done by a static frictional force during pure rolling?",
                    "answer": "Zero, because instantaneous displacement of the contact point is zero."
                },
                {
                    "question": "Express banking angle 'theta' for a frictionless curved road.",
                    "answer": "tan(theta) = v^2 / (r * g)"
                },
                {
                    "question": "Center of mass location for a solid hemisphere of radius R.",
                    "answer": "3R / 8 along the axis of symmetry from the base center."
                },
                {
                    "question": "Rocket propulsion thrust force formula.",
                    "answer": "Thrust = u * (dm/dt) where u is relative exhaust velocity."
                },
                {
                    "question": "What is Hooke's Law within elastic limits?",
                    "answer": "Stress is directly proportional to strain (Stress = Y * Strain)."
                }
            ],
            "Electrodynamics": [
                {
                    "question": "State Gauss's Law in electrostatics.",
                    "answer": "The total electric flux through a closed surface equals net enclosed charge divided by epsilon_0."
                },
                {
                    "question": "Formula for the capacitance of a parallel plate capacitor.",
                    "answer": "C = (K * epsilon_0 * A) / d"
                },
                {
                    "question": "Define drift velocity of conduction electrons.",
                    "answer": "The average velocity attained by charged particles due to an electric field: v_d = (e * E * tau) / m."
                },
                {
                    "question": "State Ampere's Circuital Law.",
                    "answer": "The line integral of magnetic field around any closed loop equals mu_0 * I."
                },
                {
                    "question": "Write Faraday's Law of electromagnetic induction.",
                    "answer": "The induced electromotive force equals the negative rate of change of magnetic flux: emf = -d(phi)/dt."
                },
                {
                    "question": "Formula for magnetic field at the center of a circular current loop.",
                    "answer": "B = (mu_0 * I) / (2 * R)"
                },
                {
                    "question": "State Lenz's Law.",
                    "answer": "The direction of induced current opposes the change in magnetic flux that produced it."
                },
                {
                    "question": "Energy density stored in an electric field.",
                    "answer": "u_E = 0.5 * epsilon_0 * E^2"
                },
                {
                    "question": "Energy density stored in a magnetic field.",
                    "answer": "u_B = B^2 / (2 * mu_0)"
                },
                {
                    "question": "Write the Lorentz force equation.",
                    "answer": "F = q * E + q * (v x B)"
                },
                {
                    "question": "Self-inductance formula for a long solenoid.",
                    "answer": "L = mu_0 * n^2 * A * l"
                },
                {
                    "question": "What is the quality factor (Q) of a series LCR circuit?",
                    "answer": "Q = (1 / R) * sqrt(L / C)"
                },
                {
                    "question": "Resonant frequency formula for a series LCR circuit.",
                    "answer": "f = 1 / (2 * pi * sqrt(L * C))"
                },
                {
                    "question": "Write Maxwell's displacement current expression.",
                    "answer": "I_d = epsilon_0 * (d(phi_E) / dt)"
                },
                {
                    "question": "Electric potential at a distance 'r' from a point charge 'q'.",
                    "answer": "V = q / (4 * pi * epsilon_0 * r)"
                },
                {
                    "question": "State Kirchhoff's current law (KCL).",
                    "answer": "The algebraic sum of currents entering a junction equals zero (Conservation of charge)."
                },
                {
                    "question": "State Kirchhoff's voltage law (KVL).",
                    "answer": "The algebraic sum of potential changes around any closed loop is zero (Conservation of energy)."
                },
                {
                    "question": "Torque experienced by an electric dipole in a uniform electric field.",
                    "answer": "Torque = p x E"
                },
                {
                    "question": "Relation between electric field and potential gradient.",
                    "answer": "E = -dV/dr"
                },
                {
                    "question": "Force per unit length between two parallel current-carrying wires.",
                    "answer": "F/l = (mu_0 * I_1 * I_2) / (2 * pi * d)"
                }
            ],
            "Thermodynamics & Kinetic Theory": [
                {
                    "question": "State the zeroth law of thermodynamics.",
                    "answer": "If two systems are each in thermal equilibrium with a third, they are in thermal equilibrium with each other."
                },
                {
                    "question": "State the first law of thermodynamics.",
                    "answer": "dQ = dU + dW (heat supplied equals change in internal energy plus work done by the system)."
                },
                {
                    "question": "Formula for work done in an isothermal process for an ideal gas.",
                    "answer": "W = nRT * ln(V2/V1)"
                },
                {
                    "question": "Formula for work done in an adiabatic process.",
                    "answer": "W = (P1V1 - P2V2) / (gamma - 1)"
                },
                {
                    "question": "Condition satisfied during an adiabatic process for an ideal gas.",
                    "answer": "PV^gamma = constant"
                },
                {
                    "question": "Efficiency formula of a Carnot engine operating between T1 (hot) and T2 (cold).",
                    "answer": "eta = 1 - T2/T1"
                },
                {
                    "question": "State the second law of thermodynamics (Clausius statement).",
                    "answer": "Heat cannot flow spontaneously from a colder body to a hotter body without external work."
                },
                {
                    "question": "Formula for the mean kinetic energy of one mole of an ideal gas.",
                    "answer": "KE = (3/2) * R * T"
                },
                {
                    "question": "Formula for RMS speed of gas molecules.",
                    "answer": "v_rms = sqrt(3RT/M)"
                },
                {
                    "question": "Degrees of freedom and Cv for a monoatomic ideal gas.",
                    "answer": "f = 3, Cv = (3/2)R"
                },
                {
                    "question": "Degrees of freedom and Cv for a diatomic ideal gas (no vibration).",
                    "answer": "f = 5, Cv = (5/2)R"
                },
                {
                    "question": "Relation between Cp and Cv (Mayer's relation).",
                    "answer": "Cp - Cv = R"
                },
                {
                    "question": "Define an isochoric process.",
                    "answer": "A thermodynamic process occurring at constant volume, so W = 0."
                },
                {
                    "question": "What does entropy measure in a thermodynamic system?",
                    "answer": "The degree of disorder or randomness of the system; total entropy of an isolated system never decreases."
                },
                {
                    "question": "Formula for the coefficient of performance (COP) of a refrigerator.",
                    "answer": "COP = Q2 / W = T2 / (T1 - T2)"
                }
            ],
            "Waves & Oscillations": [
                {
                    "question": "Formula for the time period of a mass-spring SHM system.",
                    "answer": "T = 2 * pi * sqrt(m/k)"
                },
                {
                    "question": "General displacement equation of a particle in SHM.",
                    "answer": "x(t) = A * sin(omega*t + phi)"
                },
                {
                    "question": "Formula for maximum velocity in SHM.",
                    "answer": "v_max = A * omega"
                },
                {
                    "question": "Formula for maximum acceleration in SHM.",
                    "answer": "a_max = A * omega^2"
                },
                {
                    "question": "Relation between total energy and amplitude in SHM.",
                    "answer": "E = (1/2) * k * A^2, constant throughout the motion."
                },
                {
                    "question": "Speed of a transverse wave on a stretched string.",
                    "answer": "v = sqrt(T/mu), where T is tension and mu is linear mass density."
                },
                {
                    "question": "Formula for fundamental frequency of a string fixed at both ends.",
                    "answer": "f1 = v / (2L)"
                },
                {
                    "question": "Formula for fundamental frequency of a closed organ pipe.",
                    "answer": "f1 = v / (4L)"
                },
                {
                    "question": "Condition for constructive interference of two waves.",
                    "answer": "Path difference = n * lambda (integer multiple of wavelength)."
                },
                {
                    "question": "Formula for beat frequency produced by two waves of close frequencies.",
                    "answer": "f_beat = |f1 - f2|"
                },
                {
                    "question": "Doppler effect formula for an observer moving towards a stationary source.",
                    "answer": "f' = f * (v + v_o) / v"
                },
                {
                    "question": "Define resonance in a driven oscillating system.",
                    "answer": "The phenomenon where amplitude becomes maximum when the driving frequency equals the natural frequency of the system."
                },
                {
                    "question": "What is the phase difference between a wave's displacement and its velocity in SHM?",
                    "answer": "pi/2 radians (velocity leads displacement by 90 degrees)."
                },
                {
                    "question": "Formula for the time period of a simple pendulum.",
                    "answer": "T = 2 * pi * sqrt(L/g)"
                },
                {
                    "question": "How does intensity of sound relate to amplitude?",
                    "answer": "Intensity is proportional to the square of the amplitude (I proportional to A^2)."
                }
            ],
            "Optics": [
                {
                    "question": "Mirror formula relating object distance u, image distance v, and focal length f.",
                    "answer": "1/v + 1/u = 1/f"
                },
                {
                    "question": "Lens formula relating object distance u, image distance v, and focal length f.",
                    "answer": "1/v - 1/u = 1/f"
                },
                {
                    "question": "Formula for lens magnification.",
                    "answer": "m = v/u"
                },
                {
                    "question": "Lensmaker's formula for a thin lens.",
                    "answer": "1/f = (n-1) * (1/R1 - 1/R2)"
                },
                {
                    "question": "Snell's law of refraction.",
                    "answer": "n1 * sin(theta1) = n2 * sin(theta2)"
                },
                {
                    "question": "Formula for critical angle for total internal reflection.",
                    "answer": "sin(theta_c) = 1/n (n being the refractive index of the denser medium)."
                },
                {
                    "question": "Condition for total internal reflection to occur.",
                    "answer": "Light must travel from a denser to a rarer medium and strike the interface at an angle greater than the critical angle."
                },
                {
                    "question": "Formula for fringe width in Young's double slit experiment.",
                    "answer": "beta = (lambda * D) / d"
                },
                {
                    "question": "Condition for constructive interference in YDSE (path difference).",
                    "answer": "Path difference = n * lambda"
                },
                {
                    "question": "Formula for angular resolution limit of an optical instrument (Rayleigh criterion).",
                    "answer": "theta_min = 1.22 * lambda / D"
                },
                {
                    "question": "Formula for combined focal length of two thin lenses in contact.",
                    "answer": "1/F = 1/f1 + 1/f2"
                },
                {
                    "question": "What is the condition for a compound microscope's magnifying power at normal adjustment?",
                    "answer": "M = (L/fo) * (D/fe), where L is tube length, fo and fe are objective and eyepiece focal lengths."
                },
                {
                    "question": "What causes dispersion of white light through a prism?",
                    "answer": "Refractive index varies with wavelength, so different colours refract by different amounts."
                },
                {
                    "question": "Define diffraction of light.",
                    "answer": "The bending of light waves around obstacles or through apertures comparable in size to the wavelength."
                },
                {
                    "question": "Malus's law for intensity of polarized light through an analyzer.",
                    "answer": "I = I0 * cos^2(theta)"
                }
            ],
            "Modern Physics": [
                {
                    "question": "Einstein's photoelectric equation.",
                    "answer": "KE_max = h*nu - phi (photon energy minus work function)."
                },
                {
                    "question": "Formula for de Broglie wavelength of a particle.",
                    "answer": "lambda = h / p = h / (m*v)"
                },
                {
                    "question": "Bohr's formula for the energy of the nth orbit of a hydrogen atom.",
                    "answer": "E_n = -13.6 eV / n^2"
                },
                {
                    "question": "Bohr's formula for the radius of the nth orbit of hydrogen.",
                    "answer": "r_n = 0.529 * n^2 angstrom"
                },
                {
                    "question": "Formula for radioactive decay law.",
                    "answer": "N = N0 * e^(-lambda*t)"
                },
                {
                    "question": "Relation between half-life and decay constant.",
                    "answer": "t_1/2 = 0.693 / lambda"
                },
                {
                    "question": "Einstein's mass-energy equivalence relation.",
                    "answer": "E = m * c^2"
                },
                {
                    "question": "Define binding energy per nucleon.",
                    "answer": "The energy required to remove one nucleon from the nucleus, indicating nuclear stability."
                },
                {
                    "question": "What is the threshold frequency in the photoelectric effect?",
                    "answer": "The minimum frequency of incident light below which no photoemission occurs, regardless of intensity."
                },
                {
                    "question": "Difference between nuclear fission and fusion.",
                    "answer": "Fission splits a heavy nucleus into lighter ones; fusion combines light nuclei into a heavier one, both releasing energy."
                },
                {
                    "question": "Formula for stopping potential in photoelectric effect.",
                    "answer": "e * V0 = h*nu - phi"
                },
                {
                    "question": "What are the three types of radioactive emissions?",
                    "answer": "Alpha particles, beta particles, and gamma rays."
                },
                {
                    "question": "Moseley's law relating X-ray frequency to atomic number Z.",
                    "answer": "sqrt(nu) = a * (Z - b), where a and b are constants."
                },
                {
                    "question": "Define mass defect in a nucleus.",
                    "answer": "The difference between the sum of masses of individual nucleons and the actual mass of the nucleus."
                },
                {
                    "question": "Wave-particle duality principle statement.",
                    "answer": "Matter and radiation exhibit both wave-like and particle-like properties depending on the experiment."
                }
            ]
        },
        "Chemistry": {
            "Physical": [
                {
                    "question": "What is the hybridisation of Cl in ClO4-?",
                    "answer": "sp3 hybridisation"
                },
                {
                    "question": "State Henry's law for solubility of gases.",
                    "answer": "The solubility of a gas in a liquid is directly proportional to its partial pressure: p = K_H * x."
                },
                {
                    "question": "Write the integrated rate equation for a first-order reaction.",
                    "answer": "k = (2.303 / t) * log(A_0 / A)"
                },
                {
                    "question": "Define conjugate acid-base pairs.",
                    "answer": "Two species that differ only by a single proton (H+ ion)."
                },
                {
                    "question": "State the Nernst Equation for cell potentials.",
                    "answer": "E = E_zero - (RT / nF) * ln(Q)"
                },
                {
                    "question": "Write the Arrhenius equation for temperature dependence of reaction rates.",
                    "answer": "k = A * e^(-E_a / RT)"
                },
                {
                    "question": "State the relationship between cell potential and Gibbs free energy.",
                    "answer": "delta_G = -n * F * E_cell"
                },
                {
                    "question": "Define Raoult's Law for volatile liquids.",
                    "answer": "The partial vapor pressure of each component is directly proportional to its mole fraction: p_A = p_A_zero * x_A."
                },
                {
                    "question": "Formula for degree of dissociation (alpha) using van 't Hoff factor (i) for dissociation.",
                    "answer": "alpha = (i - 1) / (n - 1)"
                },
                {
                    "question": "State Hess's Law of constant heat summation.",
                    "answer": "The total enthalpy change for a chemical reaction is the same regardless of whether it occurs in one step or multiple steps."
                },
                {
                    "question": "What is the relation between K_p and K_c?",
                    "answer": "K_p = K_c * (RT)^(delta_n)"
                },
                {
                    "question": "Formula for the half-life of a first-order reaction.",
                    "answer": "t_1/2 = 0.693 / k"
                },
                {
                    "question": "Define buffer capacity metrics.",
                    "answer": "The number of moles of acid or base added per liter of buffer solution required to change its pH by one unit."
                },
                {
                    "question": "State the relationship between solubility product (K_sp) and solubility (S) for a salt like AgCl.",
                    "answer": "K_sp = S^2"
                },
                {
                    "question": "What is the packing efficiency of a Face-Centered Cubic (FCC) lattice?",
                    "answer": "74%"
                },
                {
                    "question": "What is the packing efficiency of a Body-Centered Cubic (BCC) lattice?",
                    "answer": "68%"
                },
                {
                    "question": "Define the Schottky defect in crystals.",
                    "answer": "A stoichiometric defect where stoichiometric numbers of cations and anions are missing from the crystal lattice."
                },
                {
                    "question": "Define the Frenkel defect in ionic crystals.",
                    "answer": "A defect where an smaller ion leaves its correct lattice site and occupies an interstitial position."
                },
                {
                    "question": "Write down Faraday's First Law of Electrolysis formula.",
                    "answer": "m = Z * I * t"
                },
                {
                    "question": "What is the expression for Debye-Huckel Onsager equation for strong electrolytes?",
                    "answer": "Lambda_m = Lambda_m_zero - A * sqrt(C)"
                }
            ],
            "Organic": [
                {
                    "question": "Reagents used in the Hoffmann Bromamide Degradation reaction loop.",
                    "answer": "Br2 mixed alongside sodium hydroxide (NaOH) or KOH aqueous solutions."
                },
                {
                    "question": "What is the major product of Williamson Ether synthesis with tert-butyl chloride?",
                    "answer": "Isobutylene (Elimination occurs instead of nucleophilic substitution)."
                },
                {
                    "question": "Reagent setup used in Rosenmund Reduction process arrays.",
                    "answer": "H2 over Pd catalyzed alongside BaSO4 deactivated with sulfur poisons."
                },
                {
                    "question": "Define anti-Markovnikov addition rule criterion.",
                    "answer": "In presence of peroxides, HBr adds to unsymmetrical alkenes so hydrogen hooks to less-hydrogenated carbon."
                },
                {
                    "question": "Identify the product when phenol gets distilled directly over Zinc dust.",
                    "answer": "Benzene"
                },
                {
                    "question": "What are the reagents used in Reimer-Tiemann reaction to prepare salicylaldehyde?",
                    "answer": "Chloroform (CHCl3) and aqueous Sodium Hydroxide (NaOH)."
                },
                {
                    "question": "What is the intermediate formed during the Reimer-Tiemann reaction?",
                    "answer": "Dichlorocarbene (:CCl2)"
                },
                {
                    "question": "Reagents used in the Clemmensen Reduction.",
                    "answer": "Zinc amalgam (Zn/Hg) and concentrated Hydrochloric Acid (HCl)."
                },
                {
                    "question": "Reagents used in Wolff-Kishner Reduction loops.",
                    "answer": "Hydrazine (NH2NH2) followed by heating with KOH in ethylene glycol."
                },
                {
                    "question": "What test distinguishes Aldehydes from Ketones using ammoniacal silver nitrate?",
                    "answer": "Tollens' Test (Forms a shiny silver mirror)."
                },
                {
                    "question": "Condition required for a molecule to undergo Cannizzaro reaction.",
                    "answer": "Aldehydes lacking an alpha-hydrogen atom (e.g., Formaldehyde, Benzaldehyde)."
                },
                {
                    "question": "What is the electrophile in aromatic nitration?",
                    "answer": "Nitronium ion (NO2+)"
                },
                {
                    "question": "What product is formed when primary amine reacts with Chloroform and KOH?",
                    "answer": "Isocyanide or Carbylamine (foul-smelling compound)."
                },
                {
                    "question": "What is Hinsberg's reagent chemically?",
                    "answer": "Benzenesulfonyl chloride (C6H5SO2Cl)."
                },
                {
                    "question": "Which mechanism does the substitution of primary alkyl halides generally follow?",
                    "answer": "SN2 mechanism (Bi-molecular nucleophilic substitution)."
                },
                {
                    "question": "Which intermediate is formed in an SN1 reaction pathway?",
                    "answer": "A planar, stable carbocation intermediate."
                },
                {
                    "question": "State Huckel's rule of aromaticity.",
                    "answer": "The planar cyclic conjugated ring system must possess (4n + 2) pi electrons."
                },
                {
                    "question": "What reagent is used in Kolbe's reaction to form Salicylic acid from Phenol?",
                    "answer": "Carbon dioxide (CO2) followed by acidification."
                },
                {
                    "question": "What compound is known as Lucas reagent?",
                    "answer": "Anhydrous Zinc Chloride (ZnCl2) in concentrated HCl."
                },
                {
                    "question": "Major product obtained when HBr adds to propene via Markovnikov rule.",
                    "answer": "2-Bromopropane"
                }
            ],
            "Inorganic Chemistry": [
                {
                    "question": "State the modern periodic law.",
                    "answer": "Properties of elements are periodic functions of their atomic number."
                },
                {
                    "question": "General trend of atomic radius across a period (left to right).",
                    "answer": "Atomic radius generally decreases due to increasing nuclear charge."
                },
                {
                    "question": "General trend of ionization enthalpy down a group.",
                    "answer": "Ionization enthalpy generally decreases due to increasing atomic size and shielding."
                },
                {
                    "question": "Define electronegativity.",
                    "answer": "The tendency of an atom in a molecule to attract shared electrons towards itself."
                },
                {
                    "question": "What type of hybridisation does the central atom have in NH3?",
                    "answer": "sp3 hybridisation"
                },
                {
                    "question": "VSEPR theory prediction for the shape of a molecule with 4 bond pairs and 0 lone pairs.",
                    "answer": "Tetrahedral geometry"
                },
                {
                    "question": "Define Lewis acid.",
                    "answer": "A species that can accept a pair of electrons (electron-deficient species)."
                },
                {
                    "question": "What is back bonding, with an example?",
                    "answer": "Donation of a lone pair from a smaller atom into an empty orbital of an adjacent atom, e.g. in BF3."
                },
                {
                    "question": "State Fajans' rules regarding covalent character in ionic compounds.",
                    "answer": "Covalent character increases with smaller cation size, larger anion size, and higher cationic charge."
                },
                {
                    "question": "Which is the strongest oxoacid of chlorine and why?",
                    "answer": "HClO4 (perchloric acid), due to maximum number of oxygen atoms stabilizing the conjugate base."
                },
                {
                    "question": "Define coordination number in a coordination compound.",
                    "answer": "The number of ligand donor atoms directly bonded to the central metal atom or ion."
                },
                {
                    "question": "Werner's postulate regarding primary and secondary valency.",
                    "answer": "Primary valency is ionizable and equals oxidation state; secondary valency is non-ionizable and equals coordination number."
                },
                {
                    "question": "What causes color in most transition metal complexes?",
                    "answer": "d-d electronic transitions of unpaired electrons between split d-orbitals (crystal field splitting)."
                },
                {
                    "question": "Name the process used to extract iron from its ore in a blast furnace.",
                    "answer": "Reduction of haematite/magnetite ore using carbon monoxide (smelting)."
                },
                {
                    "question": "State the effect of lanthanide contraction on group 3 and subsequent transition elements.",
                    "answer": "It causes the atomic/ionic radii of elements after lanthanides to be nearly the same as their lighter congeners."
                },
                {
                    "question": "Define disproportionation reaction with an example.",
                    "answer": "A redox reaction where the same element is simultaneously oxidized and reduced, e.g. 2H2O2 -> 2H2O + O2."
                },
                {
                    "question": "What is the geometry of XeF4 molecule?",
                    "answer": "Square planar geometry"
                },
                {
                    "question": "State the diagonal relationship observed between Li and Mg.",
                    "answer": "Elements diagonally placed in the periodic table show similar chemical properties, e.g. both form covalent oxides and nitrides."
                }
            ]
        },
        "Maths": {
            "Calculus": [
                {
                    "question": "State the conditions required for Rolle's Theorem on interval [a,b].",
                    "answer": "f(x) must be continuous on [a,b], differentiable on open (a,b), and f(a) = f(b)."
                },
                {
                    "question": "Evaluate value of Integral dx/(1+x^2) bounded from 0 to 1.",
                    "answer": "pi / 4"
                },
                {
                    "question": "State Leibniz's rule for differentiating under integral signs.",
                    "answer": "d/dx [int_{u(x)}^{v(x)} f(t)dt] = f(v(x))*v'(x) - f(u(x))*u'(x)"
                },
                {
                    "question": "Write the general solution format for linear differential equation: dy/dx + Py = Q.",
                    "answer": "y * e^(int P dx) = int (Q * e^(int P dx)) dx + C"
                },
                {
                    "question": "Condition for two functional curves to cut orthogonally at intersections.",
                    "answer": "The product of their tangent gradients at the intersection point must equal negative unity (m_1 * m_2 = -1)."
                },
                {
                    "question": "Formula for standard limit of (sin x) / x as x approaches 0.",
                    "answer": "1"
                },
                {
                    "question": "Write the expansion of e^x series.",
                    "answer": "1 + x + x^2/2! + x^3/3! + ..."
                },
                {
                    "question": "State L'Hopital's Rule condition.",
                    "answer": "If a limit evaluates to 0/0 or inf/inf, it can be evaluated by differentiating numerator and denominator independently."
                },
                {
                    "question": "Integral of ln(x) dx.",
                    "answer": "x * ln(x) - x + C"
                },
                {
                    "question": "State Lagrange's Mean Value Theorem expression.",
                    "answer": "f'(c) = (f(b) - f(a)) / (b - a) for some c in open (a,b)."
                },
                {
                    "question": "Condition for a function to be strictly increasing on an interval.",
                    "answer": "f'(x) > 0 for all x in that interval."
                },
                {
                    "question": "Point of inflection condition inside higher derivatives.",
                    "answer": "f''(x) = 0 and f'''(x) != 0 at that specific location."
                },
                {
                    "question": "State the property of definite integrals for int_{-a}^{a} f(x) dx when f(x) is odd.",
                    "answer": "Zero"
                },
                {
                    "question": "State the property of definite integrals for int_{0}^{a} f(x) dx.",
                    "answer": "Equal to int_{0}^{a} f(a - x) dx"
                },
                {
                    "question": "What is the integrating factor (IF) for dy/dx + Py = Q?",
                    "answer": "IF = e^(int P dx)"
                },
                {
                    "question": "Write down the derivative of a^x with respect to x.",
                    "answer": "a^x * ln(a)"
                },
                {
                    "question": "Formula for curvature radius radius baseline calculation.",
                    "answer": "R = [1 + (dy/dx)^2]^(3/2) / |d^2y/dx^2|"
                },
                {
                    "question": "Integral of sec(x) dx.",
                    "answer": "ln|sec(x) + tan(x)| + C"
                },
                {
                    "question": "Condition for continuity of f(x) at x = a.",
                    "answer": "Left-hand limit = Right-hand limit = Functional value f(a)."
                },
                {
                    "question": "Express Taylor series expansion format around point a.",
                    "answer": "f(x) = f(a) + f'(a)(x-a) + f''(a)(x-a)^2/2! + ..."
                }
            ],
            "Coordinate Geometry": [
                {
                    "question": "General equation of a tangent to parabola y^2 = 4ax with gradient 'm'.",
                    "answer": "y = mx + a/m"
                },
                {
                    "question": "Condition for line y = mx + c to touch ellipse x^2/a^2 + y^2/b^2 = 1.",
                    "answer": "c^2 = a^2 * m^2 + b^2"
                },
                {
                    "question": "Formula for the length of perpendicular from (x_1, y_1) to Ax + By + C = 0.",
                    "answer": "d = |Ax_1 + By_1 + C| / sqrt(A^2 + B^2)"
                },
                {
                    "question": "Eccentricity relation equation for a hyperbola.",
                    "answer": "e = sqrt(1 + b^2 / a^2)"
                },
                {
                    "question": "Co-ordinates of the centroid of a triangle with vertices (x_i, y_i).",
                    "answer": "((x_1+x_2+x_3)/3, (y_1+y_2+y_3)/3)"
                },
                {
                    "question": "Focus coordinates for the parabola x^2 = -4ay.",
                    "answer": "(0, -a)"
                },
                {
                    "question": "Directrix equation for the parabola y^2 = 4ax.",
                    "answer": "x = -a"
                },
                {
                    "question": "Length of the latus rectum of ellipse x^2/a^2 + y^2/b^2 = 1 (where a > b).",
                    "answer": "2b^2 / a"
                },
                {
                    "question": "Distance between the foci of an ellipse.",
                    "answer": "2ae"
                },
                {
                    "question": "Distance between directrices of a hyperbola.",
                    "answer": "2a / e"
                },
                {
                    "question": "Parametric coordinates of any point on the ellipse x^2/a^2 + y^2/b^2 = 1.",
                    "answer": "(a*cos(theta), b*sin(theta))"
                },
                {
                    "question": "Angle between two intersecting lines with gradients m_1 and m_2.",
                    "answer": "tan(theta) = |(m_1 - m_2) / (1 + m_1*m_2)|"
                },
                {
                    "question": "General equation of a circle passing through origin with intercepts a and b.",
                    "answer": "x^2 + y^2 - ax - by = 0"
                },
                {
                    "question": "Condition for orthogonally intersecting circles x^2+y^2+2g_i x+2f_i y+c_i=0.",
                    "answer": "2*g_1*g_2 + 2*f_1*f_2 = c_1 + c_2"
                },
                {
                    "question": "Equation of Director Circle for ellipse x^2/a^2 + y^2/b^2 = 1.",
                    "answer": "x^2 + y^2 = a^2 + b^2"
                },
                {
                    "question": "Asymptotes equations for hyperbola x^2/a^2 - y^2/b^2 = 1.",
                    "answer": "y = +/- (b/a) * x"
                },
                {
                    "question": "Condition for lines Ax+By+C=0 and A'x+B'x+C'=0 to match parallel alignments.",
                    "answer": "A/A' = B/B'"
                },
                {
                    "question": "Area of a triangle using vertex coordinates matrix.",
                    "answer": "Area = 0.5 * |x_1(y_2-y_3) + x_2(y_3-y_1) + x_3(y_1-y_2)|"
                },
                {
                    "question": "Equation of chord of contact from external point (x_1, y_1) to circle x^2+y^2=r^2.",
                    "answer": "x*x_1 + y*y_1 = r^2"
                },
                {
                    "question": "Length of tangent from external point (x_1, y_1) to circle x^2+y^2+2gx+2fy+c=0.",
                    "answer": "L = sqrt(x_1^2 + y_1^2 + 2gx_1 + 2fy_1 + c)"
                }
            ],
            "Algebra": [
                {
                    "question": "Formula for the number of permutations of n distinct objects taken r at a time.",
                    "answer": "P(n,r) = n! / (n-r)!"
                },
                {
                    "question": "Formula for the number of combinations of n distinct objects taken r at a time.",
                    "answer": "C(n,r) = n! / (r! * (n-r)!)"
                },
                {
                    "question": "State the general term in the binomial expansion of (x+y)^n.",
                    "answer": "T_(r+1) = C(n,r) * x^(n-r) * y^r"
                },
                {
                    "question": "What is Euler's formula relating complex exponential to trigonometric functions?",
                    "answer": "e^(i*theta) = cos(theta) + i*sin(theta)"
                },
                {
                    "question": "Formula for the modulus of a complex number z = a + ib.",
                    "answer": "|z| = sqrt(a^2 + b^2)"
                },
                {
                    "question": "State De Moivre's theorem.",
                    "answer": "(cos(theta) + i*sin(theta))^n = cos(n*theta) + i*sin(n*theta)"
                },
                {
                    "question": "General formula for the nth term of an arithmetic progression.",
                    "answer": "a_n = a + (n-1)*d"
                },
                {
                    "question": "Determinant condition for a system of linear equations to have a unique solution.",
                    "answer": "The determinant of the coefficient matrix must be non-zero."
                },
                {
                    "question": "Formula for the inverse of a 2x2 matrix [[a,b],[c,d]].",
                    "answer": "Inverse = (1/(ad-bc)) * [[d,-b],[-c,a]]"
                },
                {
                    "question": "Define a skew-symmetric matrix.",
                    "answer": "A square matrix A such that A^T = -A, with all diagonal elements equal to zero."
                },
                {
                    "question": "State the multiplication rule of probability for independent events.",
                    "answer": "P(A and B) = P(A) * P(B)"
                },
                {
                    "question": "State Bayes' theorem.",
                    "answer": "P(A|B) = [P(B|A) * P(A)] / P(B)"
                },
                {
                    "question": "Formula for the sum of the binomial coefficients C(n,0) + C(n,1) + ... + C(n,n).",
                    "answer": "2^n"
                },
                {
                    "question": "Condition for three complex numbers to be collinear on the Argand plane.",
                    "answer": "(z2 - z1) / (z3 - z1) must be a real number."
                },
                {
                    "question": "Formula for variance of a binomial distribution B(n,p).",
                    "answer": "Variance = n * p * (1-p)"
                }
            ],
            "Vectors & 3D Geometry": [
                {
                    "question": "Formula for the dot product of two vectors A and B.",
                    "answer": "A.B = |A| * |B| * cos(theta)"
                },
                {
                    "question": "Formula for the cross product magnitude of two vectors A and B.",
                    "answer": "|A x B| = |A| * |B| * sin(theta)"
                },
                {
                    "question": "Condition for two vectors to be perpendicular.",
                    "answer": "Their dot product must equal zero (A.B = 0)."
                },
                {
                    "question": "Condition for two vectors to be parallel.",
                    "answer": "Their cross product must equal the zero vector (A x B = 0)."
                },
                {
                    "question": "Formula for the scalar triple product of vectors A, B, C.",
                    "answer": "[A B C] = A . (B x C)"
                },
                {
                    "question": "Geometric meaning of the scalar triple product being zero.",
                    "answer": "The three vectors are coplanar."
                },
                {
                    "question": "Formula for direction cosines l, m, n of a line and the relation between them.",
                    "answer": "l^2 + m^2 + n^2 = 1"
                },
                {
                    "question": "Equation of a line through a point with position vector a and parallel to vector b.",
                    "answer": "r = a + t*b, for scalar parameter t."
                },
                {
                    "question": "Vector equation of a plane with normal vector n passing through point with position vector a.",
                    "answer": "(r - a) . n = 0"
                },
                {
                    "question": "Formula for the shortest distance between two skew lines.",
                    "answer": "d = |(a2 - a1) . (b1 x b2)| / |b1 x b2|"
                },
                {
                    "question": "Formula for the angle between two planes with normal vectors n1 and n2.",
                    "answer": "cos(theta) = |n1.n2| / (|n1| * |n2|)"
                },
                {
                    "question": "Formula for distance of a point (x1,y1,z1) from plane Ax+By+Cz+D=0.",
                    "answer": "d = |Ax1+By1+Cz1+D| / sqrt(A^2+B^2+C^2)"
                },
                {
                    "question": "Formula for a unit vector along a given vector A.",
                    "answer": "unit vector = A / |A|"
                },
                {
                    "question": "Section formula for a point dividing segment AB in ratio m:n (position vectors).",
                    "answer": "r = (m*b + n*a) / (m+n)"
                },
                {
                    "question": "Vector equation of a line passing through two points with position vectors a and b.",
                    "answer": "r = a + t*(b - a), for scalar parameter t."
                },
                {
                    "question": "Condition for four points with position vectors a, b, c, d to be coplanar.",
                    "answer": "The vectors (b-a), (c-a), (d-a) must have a zero scalar triple product."
                },
                {
                    "question": "Formula for the projection of vector A onto vector B.",
                    "answer": "Projection = (A.B) / |B|"
                },
                {
                    "question": "Formula for the area of a triangle using two side vectors A and B from a common vertex.",
                    "answer": "Area = (1/2) * |A x B|"
                },
                {
                    "question": "Formula for the volume of a tetrahedron using three edge vectors from one vertex.",
                    "answer": "Volume = (1/6) * |A . (B x C)|"
                },
                {
                    "question": "Formula for the angle between a line with direction vector b and a plane with normal n.",
                    "answer": "sin(theta) = |b.n| / (|b| * |n|)"
                }
            ],
            "Trigonometry": [
                {
                    "question": "State the trigonometric identity for sin(A+B).",
                    "answer": "sin(A+B) = sin(A)cos(B) + cos(A)sin(B)"
                },
                {
                    "question": "State the trigonometric identity for cos(A+B).",
                    "answer": "cos(A+B) = cos(A)cos(B) - sin(A)sin(B)"
                },
                {
                    "question": "Formula for tan(A+B) in terms of tan(A) and tan(B).",
                    "answer": "tan(A+B) = (tanA + tanB) / (1 - tanA*tanB)"
                },
                {
                    "question": "Sine rule relating sides a,b,c of a triangle to angles A,B,C.",
                    "answer": "a/sin(A) = b/sin(B) = c/sin(C) = 2R"
                },
                {
                    "question": "Cosine rule for side a of a triangle.",
                    "answer": "a^2 = b^2 + c^2 - 2bc*cos(A)"
                },
                {
                    "question": "Formula for the general solution of sin(theta) = sin(alpha).",
                    "answer": "theta = n*pi + (-1)^n * alpha, for integer n."
                },
                {
                    "question": "Formula for the general solution of cos(theta) = cos(alpha).",
                    "answer": "theta = 2*n*pi +/- alpha, for integer n."
                },
                {
                    "question": "Formula for the area of a triangle given two sides and the included angle.",
                    "answer": "Area = (1/2) * a * b * sin(C)"
                },
                {
                    "question": "Formula for sin(2A) in terms of sin(A) and cos(A).",
                    "answer": "sin(2A) = 2*sin(A)*cos(A)"
                },
                {
                    "question": "Formula for cos(2A) in three common forms.",
                    "answer": "cos(2A) = 1 - 2sin^2(A) = 2cos^2(A) - 1 = cos^2(A) - sin^2(A)"
                },
                {
                    "question": "State the trigonometric identity for sin(A-B).",
                    "answer": "sin(A-B) = sin(A)cos(B) - cos(A)sin(B)"
                },
                {
                    "question": "State the trigonometric identity for cos(A-B).",
                    "answer": "cos(A-B) = cos(A)cos(B) + sin(A)sin(B)"
                },
                {
                    "question": "Formula for tan(A-B) in terms of tan(A) and tan(B).",
                    "answer": "tan(A-B) = (tanA - tanB) / (1 + tanA*tanB)"
                },
                {
                    "question": "Sum-to-product formula for sin(A) + sin(B).",
                    "answer": "sinA + sinB = 2 * sin((A+B)/2) * cos((A-B)/2)"
                },
                {
                    "question": "Product-to-sum formula for 2*sin(A)*cos(B).",
                    "answer": "2*sinA*cosB = sin(A+B) + sin(A-B)"
                },
                {
                    "question": "Formula for tan(theta/2) in terms of sin(theta) and cos(theta).",
                    "answer": "tan(theta/2) = sin(theta) / (1 + cos(theta)) = (1 - cos(theta)) / sin(theta)"
                },
                {
                    "question": "What is the range of the principal value branch of sin inverse (arcsin)?",
                    "answer": "[-pi/2, pi/2]"
                },
                {
                    "question": "What is the domain of the tan inverse (arctan) function?",
                    "answer": "All real numbers, (-infinity, infinity)"
                },
                {
                    "question": "Formula relating the sum of angles A, B, C of a triangle.",
                    "answer": "A + B + C = 180 degrees (pi radians)"
                },
                {
                    "question": "Formula for the height of a tower using angle of elevation theta and distance d from base.",
                    "answer": "Height = d * tan(theta)"
                }
            ]
        }
    },
    "NEET": {
        "Biology": {
            "Botany": [
                {
                    "question": "Where exactly does the Krebs cycle take place in eukaryotic cellular geometry?",
                    "answer": "Within the internal mitochondrial matrix space."
                },
                {
                    "question": "Which hormone promotes apical dominance in plants?",
                    "answer": "Auxin (Indole-3-acetic acid)."
                },
                {
                    "question": "Name the primary CO2 acceptor molecule in C4 photosynthetic cycles.",
                    "answer": "Phosphoenolpyruvate (PEP)."
                },
                {
                    "question": "State the function of tapetum layer within microsporangium configurations.",
                    "answer": "Provides structural nourishment to developing pollen grain cells."
                },
                {
                    "question": "Define parthenocarpy with commercial crop examples.",
                    "answer": "Development of seedless fruits without fertilization processes (e.g., Banana)."
                },
                {
                    "question": "What are the criteria for essentiality of elements in plant nutrition?",
                    "answer": "Element must be indispensable for growth, irreplaceable by others, and directly involved in metabolism."
                },
                {
                    "question": "Name the fungus that produces Cyclosporin A immunosuppressants.",
                    "answer": "Trichoderma polysporum."
                },
                {
                    "question": "Which ecological pyramid format cannot execute inverted positions?",
                    "answer": "Pyramid of Energy is always upright due to thermodynamic transfer rules."
                },
                {
                    "question": "Define endospermic seeds with crop instances.",
                    "answer": "Seeds retaining endosperm tissue upon reaching maturity stages (e.g., Maize, Castor, Wheat)."
                },
                {
                    "question": "What is the genetic ploidy level of endosperm tissue in Angiosperms?",
                    "answer": "Triploid (3n) due to triple fusion events."
                },
                {
                    "question": "Which tracking pigment captures solar energy during oxygenic photosynthesis?",
                    "answer": "Chlorophyll-a molecules."
                },
                {
                    "question": "Name the enzyme complex cataloging nitrogen fixation within root nodules.",
                    "answer": "Nitrogenase enzyme complex (highly sensitive to molecular oxygen)."
                },
                {
                    "question": "What unique anatomical structural configuration defines leaves of C4 plants?",
                    "answer": "Kranz Anatomy layout configuration."
                },
                {
                    "question": "Which gaseous plant growth regulator triggers quick ripening of fruit?",
                    "answer": "Ethylene"
                },
                {
                    "question": "Name the structural tissue transport channel that shifts sugars through plant bodies.",
                    "answer": "Phloem sieve tube networks."
                },
                {
                    "question": "Define the biological term for the cell wall splitting step during cellular divisions.",
                    "answer": "Cytokinesis process loop."
                },
                {
                    "question": "What specialized pore configurations handle guttation drops along leaf borders?",
                    "answer": "Hydathodes structures."
                },
                {
                    "question": "Name the botanical family grouping holding tomato and potato plants.",
                    "answer": "Solanaceae family classification."
                },
                {
                    "question": "Define thematic photoperiodism behavior responses.",
                    "answer": "Physiological responses of plants relative to the comparative duration of daily light and dark cycles."
                },
                {
                    "question": "Which phase profile captures DNA replication during standard interphase blocks?",
                    "answer": "S-phase (Synthesis Phase)."
                }
            ],
            "Zoology": [
                {
                    "question": "What is the primary physiological function of interstitial Leydig cells?",
                    "answer": "Synthesis and secretion of testicular androgen hormones (testosterone)."
                },
                {
                    "question": "Which specific adenohypophyseal hormone triggers immediate ovulation cycles?",
                    "answer": "Luteinizing Hormone (LH surge)."
                },
                {
                    "question": "Name the structural and functional unit of the human kidney network.",
                    "answer": "Nephron"
                },
                {
                    "question": "Where are the bundle of His muscle fibers localized inside human cardiovascular networks?",
                    "answer": "Interventricular septal walls of heart systems."
                },
                {
                    "question": "Name the structural cell types secreting Pepsinogen zymogens inside gastric pits.",
                    "answer": "Chief cells (Peptic cells)."
                },
                {
                    "question": "State the exact genetic transmission mutation pattern defining Sickle Cell Anemia tracks.",
                    "answer": "Autosomal recessive point mutation changing Glutamic acid to Valine at 6th slot of beta-globin chain."
                },
                {
                    "question": "Which antibody class shows elevated counts during acute hypersensitivity or allergic responses?",
                    "answer": "Immunoglobulin E (IgE)."
                },
                {
                    "question": "What parameter describes the human structural joint linking atlas and axis vertebrae?",
                    "answer": "Pivot joint layout configuration."
                },
                {
                    "question": "Name the site where primary spermatogenesis transformations happen structurally.",
                    "answer": "Seminiferous tubules within testicular configurations."
                },
                {
                    "question": "Which hormone lowers human blood calcium profiles when hypercalcemia patterns develop?",
                    "answer": "Thyrocalcitonin (TCT) secreted by parafollicular C-cells."
                },
                {
                    "question": "Name the primary phagocytic leukocyte configurations shielding human immune networks.",
                    "answer": "Neutrophils and Monocytes."
                },
                {
                    "question": "Where are structural matching audio receptors localized within human ear apparatus systems?",
                    "answer": "Organ of Corti positioned over basilar membrane regions."
                },
                {
                    "question": "Name the primary structural connective link tying muscle blocks to skeletal layouts.",
                    "answer": "Tendons"
                },
                {
                    "question": "Which endocrine entity releases melatonin into human systemic loops?",
                    "answer": "Pineal gland structures."
                },
                {
                    "question": "What unique breathing organ configuration handles ventilation for insects?",
                    "answer": "Tracheolar tube infrastructure networks."
                },
                {
                    "question": "Name the primary target bile component formatting lipid emulsions.",
                    "answer": "Bile salts (Sodium glycocholate and taurocholate)."
                },
                {
                    "question": "Which cell structure component isolates the standard blood-filtering slit interface inside Bowman capsules?",
                    "answer": "Podocytes"
                },
                {
                    "question": "Define the physiological function of surfactant lining pulmonary alveoli interfaces.",
                    "answer": "Lowers internal surface tension to guard alveolar walls against collapse loops."
                },
                {
                    "question": "Name the primary oxygen-carrying metalloprotein layout formatting red blood cell masses.",
                    "answer": "Hemoglobin"
                },
                {
                    "question": "Which neural center guides automatic autonomic respiratory cycle parameters natively?",
                    "answer": "Medulla Oblongata center clusters."
                }
            ],
            "Genetics & Evolution": [
                {
                    "question": "State Mendel's law of dominance.",
                    "answer": "In a heterozygous pair of alleles, one allele (dominant) masks the expression of the other (recessive)."
                },
                {
                    "question": "State Mendel's law of independent assortment.",
                    "answer": "Genes for different traits are inherited independently of one another during gamete formation."
                },
                {
                    "question": "What is the genotype ratio produced from a monohybrid cross of two heterozygotes (Aa x Aa)?",
                    "answer": "1 AA : 2 Aa : 1 aa"
                },
                {
                    "question": "Define a test cross.",
                    "answer": "Crossing an individual of unknown genotype with a homozygous recessive individual to determine the unknown genotype."
                },
                {
                    "question": "What is the chromosomal basis of sex determination in humans?",
                    "answer": "XX produces female offspring, XY produces male offspring; the father's sperm determines the sex."
                },
                {
                    "question": "Define linkage in genetics.",
                    "answer": "The tendency of genes located close together on the same chromosome to be inherited together."
                },
                {
                    "question": "State Hardy-Weinberg principle.",
                    "answer": "Allele and genotype frequencies in a population remain constant across generations in the absence of evolutionary influences."
                },
                {
                    "question": "Define natural selection as proposed by Darwin.",
                    "answer": "Differential survival and reproduction of individuals due to heritable traits best suited to the environment."
                },
                {
                    "question": "What is a point mutation?",
                    "answer": "A change in a single nucleotide base pair in the DNA sequence."
                },
                {
                    "question": "Define homologous organs with an example.",
                    "answer": "Organs with the same basic structure and origin but different functions, e.g. forelimbs of frog, bird, and human."
                },
                {
                    "question": "What molecule carries genetic information in most organisms?",
                    "answer": "DNA (Deoxyribonucleic acid)."
                },
                {
                    "question": "Define a codon.",
                    "answer": "A sequence of three nucleotides on mRNA that codes for a specific amino acid."
                },
                {
                    "question": "Define incomplete dominance with an example.",
                    "answer": "A condition where neither allele is completely dominant, producing a blended phenotype, e.g. pink flowers from red and white parent plants."
                },
                {
                    "question": "Define co-dominance with an example.",
                    "answer": "A condition where both alleles are expressed equally in the phenotype, e.g. AB blood group in humans."
                },
                {
                    "question": "What is a pedigree analysis used for?",
                    "answer": "Tracing the inheritance pattern of a particular genetic trait through several generations of a family."
                },
                {
                    "question": "Define polygenic inheritance with an example.",
                    "answer": "A trait controlled by multiple genes each contributing a small additive effect, e.g. human skin colour."
                },
                {
                    "question": "Define genetic drift.",
                    "answer": "Random fluctuation in allele frequencies in a population, especially significant in small populations."
                },
                {
                    "question": "Define speciation.",
                    "answer": "The evolutionary process by which populations evolve to become distinct new species."
                },
                {
                    "question": "State the central dogma of molecular biology.",
                    "answer": "Genetic information flows from DNA to RNA to Protein."
                },
                {
                    "question": "Describe DNA replication's semi-conservative model.",
                    "answer": "Each daughter DNA molecule retains one original parental strand and one newly synthesized strand."
                }
            ],
            "Ecology & Environment": [
                {
                    "question": "Define an ecosystem.",
                    "answer": "A functional unit of nature comprising all living organisms and their physical environment interacting as a system."
                },
                {
                    "question": "Define a food chain.",
                    "answer": "A linear sequence of organisms through which nutrients and energy pass as one organism eats another."
                },
                {
                    "question": "State the 10 percent law of energy transfer between trophic levels.",
                    "answer": "Only about 10% of energy is transferred from one trophic level to the next; the rest is lost mainly as heat."
                },
                {
                    "question": "Define a keystone species.",
                    "answer": "A species that has a disproportionately large impact on its ecosystem relative to its abundance."
                },
                {
                    "question": "Define carrying capacity of a population.",
                    "answer": "The maximum population size an environment can sustainably support given available resources."
                },
                {
                    "question": "Define primary succession.",
                    "answer": "The establishment and development of an ecosystem in an area that has never previously supported life, e.g. on bare rock."
                },
                {
                    "question": "What is biomagnification?",
                    "answer": "The increasing concentration of a toxic substance in organisms at each successive trophic level."
                },
                {
                    "question": "Define biodiversity hotspot.",
                    "answer": "A biogeographic region with significant levels of biodiversity that is threatened by human habitation."
                },
                {
                    "question": "Name the layer of the atmosphere that protects Earth from harmful UV radiation.",
                    "answer": "The ozone layer, located in the stratosphere."
                },
                {
                    "question": "Define in-situ conservation with an example.",
                    "answer": "Conservation of species within their natural habitat, e.g. national parks and wildlife sanctuaries."
                },
                {
                    "question": "Define population density in ecology.",
                    "answer": "The number of individuals of a species per unit area or volume of habitat."
                },
                {
                    "question": "Name the three basic types of age pyramids in population ecology.",
                    "answer": "Expanding, stable, and declining age pyramids."
                },
                {
                    "question": "Define mutualism with an example.",
                    "answer": "An interaction where both species benefit, e.g. lichens (fungus and algae) or bees and flowering plants."
                },
                {
                    "question": "Define parasitism with an example.",
                    "answer": "An interaction where one organism (parasite) benefits at the expense of another (host), e.g. tapeworms in humans."
                },
                {
                    "question": "Define eutrophication.",
                    "answer": "Excessive nutrient enrichment of a water body, causing algal blooms and oxygen depletion."
                },
                {
                    "question": "Define a pollutant.",
                    "answer": "Any substance present in the environment in harmful concentrations that adversely affects organisms."
                },
                {
                    "question": "What was the primary goal of the Montreal Protocol?",
                    "answer": "To phase out the production and use of substances responsible for depleting the ozone layer."
                },
                {
                    "question": "What is the purpose of the Red Data Book?",
                    "answer": "It documents the conservation status of species that are threatened, endangered, or extinct."
                },
                {
                    "question": "Define species richness.",
                    "answer": "The number of different species present in a particular ecological community."
                },
                {
                    "question": "What is the primary anthropogenic cause of global warming?",
                    "answer": "Increased emission of greenhouse gases, especially carbon dioxide, from burning fossil fuels."
                }
            ]
        },
        "Physics": {
            "Mechanics & Properties of Matter": [
                {
                    "question": "Formula for the first equation of motion.",
                    "answer": "v = u + at"
                },
                {
                    "question": "Formula for kinetic energy of a moving object.",
                    "answer": "KE = (1/2) * m * v^2"
                },
                {
                    "question": "State Newton's second law of motion.",
                    "answer": "F = m*a (force equals mass times acceleration)."
                },
                {
                    "question": "State the law of conservation of linear momentum.",
                    "answer": "In absence of external force, total momentum of a system remains constant."
                },
                {
                    "question": "Formula for gravitational potential energy near Earth's surface.",
                    "answer": "PE = m*g*h"
                },
                {
                    "question": "Formula for Young's modulus of elasticity.",
                    "answer": "Y = stress / strain = (F/A) / (delta_L / L)"
                },
                {
                    "question": "State Pascal's law of fluid pressure.",
                    "answer": "Pressure applied to an enclosed fluid is transmitted equally in all directions."
                },
                {
                    "question": "State Bernoulli's principle.",
                    "answer": "For an ideal fluid in streamline flow, the sum of pressure energy, kinetic energy, and potential energy per unit volume remains constant."
                },
                {
                    "question": "Formula for surface tension.",
                    "answer": "T = Force / Length (force per unit length along the liquid surface)."
                },
                {
                    "question": "State Stokes' law for viscous drag on a sphere.",
                    "answer": "F = 6 * pi * eta * r * v"
                },
                {
                    "question": "Formula for centripetal acceleration.",
                    "answer": "a_c = v^2 / r"
                },
                {
                    "question": "Formula for torque produced by a force.",
                    "answer": "Torque = Force * perpendicular distance from the axis of rotation"
                },
                {
                    "question": "State the law of conservation of angular momentum.",
                    "answer": "In absence of external torque, the angular momentum of a system remains constant."
                },
                {
                    "question": "Formula for power in terms of work and time.",
                    "answer": "Power = Work / Time"
                },
                {
                    "question": "Formula for pressure exerted by a force over an area.",
                    "answer": "P = F / A"
                },
                {
                    "question": "Define the elastic limit of a material.",
                    "answer": "The maximum stress a material can withstand while still returning to its original shape once the force is removed."
                },
                {
                    "question": "Formula for density of a substance.",
                    "answer": "Density = Mass / Volume"
                },
                {
                    "question": "State Archimedes' principle.",
                    "answer": "The upward buoyant force on a submerged body equals the weight of the fluid displaced by it."
                },
                {
                    "question": "Define terminal velocity.",
                    "answer": "The constant maximum velocity reached by an object falling through a fluid when the net force on it becomes zero."
                },
                {
                    "question": "State the work-energy theorem.",
                    "answer": "The net work done on an object equals its change in kinetic energy."
                }
            ],
            "Electricity & Magnetism": [
                {
                    "question": "State Ohm's law.",
                    "answer": "V = IR, provided physical conditions like temperature remain constant."
                },
                {
                    "question": "Formula for electrical power dissipated in a resistor.",
                    "answer": "P = I^2 * R = V^2 / R"
                },
                {
                    "question": "Formula for equivalent resistance of resistors in series.",
                    "answer": "R_eq = R1 + R2 + R3 + ..."
                },
                {
                    "question": "Formula for equivalent resistance of resistors in parallel.",
                    "answer": "1/R_eq = 1/R1 + 1/R2 + 1/R3 + ..."
                },
                {
                    "question": "Coulomb's law formula for force between two point charges.",
                    "answer": "F = k * q1*q2 / r^2"
                },
                {
                    "question": "Formula for magnetic force on a moving charge (Lorentz force).",
                    "answer": "F = q*v*B*sin(theta)"
                },
                {
                    "question": "State Faraday's law of electromagnetic induction.",
                    "answer": "Induced EMF equals the negative rate of change of magnetic flux."
                },
                {
                    "question": "Formula for the energy stored in a charged capacitor.",
                    "answer": "E = (1/2) * C * V^2"
                },
                {
                    "question": "Formula for electric field due to a point charge at distance r.",
                    "answer": "E = k*q / r^2"
                },
                {
                    "question": "Formula for capacitance of a parallel plate capacitor.",
                    "answer": "C = epsilon_0 * A / d"
                },
                {
                    "question": "State Kirchhoff's current law.",
                    "answer": "The sum of currents entering a junction equals the sum of currents leaving it."
                },
                {
                    "question": "State Kirchhoff's voltage law.",
                    "answer": "The sum of potential differences around any closed loop in a circuit is zero."
                },
                {
                    "question": "Define magnetic flux.",
                    "answer": "The total number of magnetic field lines passing through a given area, phi = B*A*cos(theta)."
                },
                {
                    "question": "Formula for the force per unit length between two parallel current-carrying wires.",
                    "answer": "F/l = (mu_0 * I1 * I2) / (2*pi*d)"
                },
                {
                    "question": "What does the right-hand thumb rule determine?",
                    "answer": "The direction of the magnetic field produced around a current-carrying conductor."
                },
                {
                    "question": "State the principle on which a transformer works.",
                    "answer": "Mutual electromagnetic induction between two coils linked by a common changing magnetic flux."
                },
                {
                    "question": "State the principle on which an AC generator works.",
                    "answer": "Electromagnetic induction: rotating a coil in a magnetic field induces an alternating EMF."
                },
                {
                    "question": "Define electric potential at a point.",
                    "answer": "The work done per unit positive charge in bringing it from infinity to that point in an electric field."
                },
                {
                    "question": "Formula for the equivalent capacitance of capacitors in series.",
                    "answer": "1/C_eq = 1/C1 + 1/C2 + 1/C3 + ..."
                },
                {
                    "question": "Formula for the equivalent capacitance of capacitors in parallel.",
                    "answer": "C_eq = C1 + C2 + C3 + ..."
                }
            ],
            "Optics & Modern Physics": [
                {
                    "question": "Formula for power of a lens in terms of focal length.",
                    "answer": "P = 1/f (in metres), measured in dioptres."
                },
                {
                    "question": "Human eye defect corrected by a concave lens.",
                    "answer": "Myopia (short-sightedness/near-sightedness)."
                },
                {
                    "question": "Human eye defect corrected by a convex lens.",
                    "answer": "Hypermetropia (long-sightedness/far-sightedness)."
                },
                {
                    "question": "Formula relating refractive index to speed of light in a medium.",
                    "answer": "n = c / v"
                },
                {
                    "question": "Einstein's photoelectric equation.",
                    "answer": "KE_max = h*nu - phi"
                },
                {
                    "question": "Formula for radioactive half-life.",
                    "answer": "t_1/2 = 0.693 / lambda"
                },
                {
                    "question": "Mirror formula relating object distance u, image distance v, and focal length f.",
                    "answer": "1/v + 1/u = 1/f"
                },
                {
                    "question": "Lens formula relating object distance u, image distance v, and focal length f.",
                    "answer": "1/v - 1/u = 1/f"
                },
                {
                    "question": "Condition for total internal reflection to occur.",
                    "answer": "Light must travel from a denser to a rarer medium at an angle greater than the critical angle."
                },
                {
                    "question": "What atmospheric phenomenon causes a rainbow to form?",
                    "answer": "Dispersion and total internal reflection of sunlight inside water droplets."
                },
                {
                    "question": "What is the function of a compound microscope's objective lens?",
                    "answer": "It forms a real, inverted, and magnified image of a very small nearby object."
                },
                {
                    "question": "Define nuclear fission with an example.",
                    "answer": "The splitting of a heavy nucleus into two lighter nuclei with release of energy, e.g. Uranium-235 fission."
                },
                {
                    "question": "Define nuclear fusion with an example.",
                    "answer": "The combining of light nuclei into a heavier nucleus with release of energy, e.g. hydrogen fusing into helium in the Sun."
                },
                {
                    "question": "Define isotopes.",
                    "answer": "Atoms of the same element with the same number of protons but different numbers of neutrons."
                },
                {
                    "question": "How are X-rays typically produced?",
                    "answer": "By bombarding a metal target with high-speed electrons, causing sudden deceleration and photon emission."
                },
                {
                    "question": "What does the acronym LASER stand for?",
                    "answer": "Light Amplification by Stimulated Emission of Radiation."
                },
                {
                    "question": "What is a photodiode commonly used for?",
                    "answer": "Detecting light by converting incident photons into an electrical current."
                },
                {
                    "question": "Formula for the de Broglie wavelength of a moving particle.",
                    "answer": "lambda = h / (m*v)"
                },
                {
                    "question": "Einstein's photoelectric equation.",
                    "answer": "KE_max = h*nu - phi"
                },
                {
                    "question": "Formula for power of a lens in terms of its focal length.",
                    "answer": "P = 1/f (in metres), measured in dioptres."
                }
            ],
            "Thermodynamics & Waves": [
                {
                    "question": "Formula relating Celsius and Kelvin temperature scales.",
                    "answer": "T(K) = T(C) + 273.15"
                },
                {
                    "question": "Formula for heat required to raise temperature of a substance.",
                    "answer": "Q = m * c * delta_T"
                },
                {
                    "question": "Formula for heat required for a phase change.",
                    "answer": "Q = m * L (L being latent heat)."
                },
                {
                    "question": "Formula for speed of sound in air (approximate dependence).",
                    "answer": "v proportional to sqrt(T), where T is absolute temperature."
                },
                {
                    "question": "State the first law of thermodynamics.",
                    "answer": "dQ = dU + dW"
                },
                {
                    "question": "Define specific heat capacity.",
                    "answer": "The amount of heat required to raise the temperature of a unit mass of a substance by one degree."
                },
                {
                    "question": "Define latent heat.",
                    "answer": "The heat absorbed or released during a phase change at constant temperature, without a temperature change."
                },
                {
                    "question": "State Boyle's law.",
                    "answer": "At constant temperature, the pressure of a fixed mass of gas is inversely proportional to its volume."
                },
                {
                    "question": "State Charles's law.",
                    "answer": "At constant pressure, the volume of a fixed mass of gas is directly proportional to its absolute temperature."
                },
                {
                    "question": "State the ideal gas law.",
                    "answer": "PV = nRT"
                },
                {
                    "question": "Define the Doppler effect.",
                    "answer": "The apparent change in frequency of a wave due to relative motion between the source and the observer."
                },
                {
                    "question": "Define resonance.",
                    "answer": "A phenomenon where a system oscillates with maximum amplitude when driven at its natural frequency."
                },
                {
                    "question": "Formula relating wave speed, frequency, and wavelength.",
                    "answer": "v = f * lambda"
                },
                {
                    "question": "Distinguish pitch and loudness of sound.",
                    "answer": "Pitch depends on frequency; loudness depends on amplitude (intensity) of the sound wave."
                },
                {
                    "question": "What is the typical frequency range of ultrasound?",
                    "answer": "Above 20,000 Hz (20 kHz), beyond the range of human hearing."
                },
                {
                    "question": "What is infrasound?",
                    "answer": "Sound waves with frequency below 20 Hz, below the range of human hearing."
                },
                {
                    "question": "State the first law of thermodynamics.",
                    "answer": "dQ = dU + dW (heat supplied equals change in internal energy plus work done by the system)."
                },
                {
                    "question": "Formula relating Celsius and Kelvin temperature scales.",
                    "answer": "T(K) = T(C) + 273.15"
                },
                {
                    "question": "Formula for heat required for a phase change.",
                    "answer": "Q = m * L, where L is the latent heat of the substance."
                },
                {
                    "question": "Formula for speed of sound's approximate dependence on temperature.",
                    "answer": "v is proportional to sqrt(T), where T is the absolute temperature."
                }
            ]
        },
        "Chemistry": {
            "Physical Chemistry": [
                {
                    "question": "State Avogadro's law.",
                    "answer": "Equal volumes of all gases at the same temperature and pressure contain equal numbers of molecules."
                },
                {
                    "question": "Ideal gas equation.",
                    "answer": "PV = nRT"
                },
                {
                    "question": "State the mole concept relation between moles, mass, and molar mass.",
                    "answer": "Number of moles = Given mass / Molar mass"
                },
                {
                    "question": "Formula for molarity of a solution.",
                    "answer": "Molarity = moles of solute / volume of solution in litres"
                },
                {
                    "question": "Formula for pH of a solution.",
                    "answer": "pH = -log10[H+]"
                },
                {
                    "question": "State the Arrhenius definition of acids and bases.",
                    "answer": "Acids increase H+ ion concentration and bases increase OH- ion concentration in aqueous solution."
                },
                {
                    "question": "State Le Chatelier's principle.",
                    "answer": "If a system at equilibrium is disturbed, it shifts in the direction that counteracts the disturbance."
                },
                {
                    "question": "Formula for rate of a first order reaction in terms of half-life.",
                    "answer": "t_1/2 = 0.693 / k"
                },
                {
                    "question": "Define oxidation in terms of electron transfer.",
                    "answer": "Loss of electrons by a species (increase in oxidation number)."
                },
                {
                    "question": "Formula for molality of a solution.",
                    "answer": "Molality = moles of solute / mass of solvent in kg"
                },
                {
                    "question": "Define normality of a solution.",
                    "answer": "The number of gram equivalents of solute dissolved per litre of solution."
                },
                {
                    "question": "Define equivalent weight of a substance.",
                    "answer": "The mass of a substance that combines with or displaces one mole of hydrogen ions (or electrons)."
                },
                {
                    "question": "State Raoult's law for a solution of volatile liquids.",
                    "answer": "The partial vapour pressure of each component is proportional to its mole fraction in the solution."
                },
                {
                    "question": "Define osmotic pressure.",
                    "answer": "The pressure required to prevent the flow of solvent molecules across a semi-permeable membrane by osmosis."
                },
                {
                    "question": "Name the four common colligative properties of solutions.",
                    "answer": "Relative lowering of vapour pressure, elevation of boiling point, depression of freezing point, and osmotic pressure."
                },
                {
                    "question": "Define a catalyst.",
                    "answer": "A substance that increases the rate of a chemical reaction without itself being permanently consumed."
                },
                {
                    "question": "Define activation energy.",
                    "answer": "The minimum energy required by reactant molecules to undergo an effective collision and form products."
                },
                {
                    "question": "Distinguish an exothermic reaction from an endothermic reaction.",
                    "answer": "Exothermic reactions release heat to the surroundings; endothermic reactions absorb heat from the surroundings."
                }
            ],
            "Organic Chemistry": [
                {
                    "question": "General formula of an alkane homologous series.",
                    "answer": "CnH(2n+2)"
                },
                {
                    "question": "General formula of an alkene homologous series.",
                    "answer": "CnH2n"
                },
                {
                    "question": "Define isomers.",
                    "answer": "Compounds having the same molecular formula but different structural arrangements."
                },
                {
                    "question": "Name the functional group -COOH.",
                    "answer": "Carboxylic acid group"
                },
                {
                    "question": "Name the functional group -CHO.",
                    "answer": "Aldehyde group"
                },
                {
                    "question": "What is denaturation of proteins?",
                    "answer": "Loss of a protein's native secondary and tertiary structure due to heat, pH change, or chemical agents, usually losing biological activity."
                },
                {
                    "question": "Define a monosaccharide with an example.",
                    "answer": "The simplest form of carbohydrate that cannot be hydrolyzed further, e.g. glucose."
                },
                {
                    "question": "What type of bond links amino acids in a protein?",
                    "answer": "Peptide bond (amide linkage, -CO-NH-)."
                },
                {
                    "question": "What is the basic principle behind IUPAC naming of organic compounds?",
                    "answer": "Naming is based on identifying the longest carbon chain, the principal functional group, and numbering substituents for lowest locants."
                },
                {
                    "question": "Classify hydrocarbons based on carbon-carbon bonding.",
                    "answer": "Saturated (alkanes, only single bonds) and unsaturated (alkenes and alkynes, with double or triple bonds)."
                },
                {
                    "question": "Name the functional group present in esters.",
                    "answer": "-COO- (carboxylate ester linkage)"
                },
                {
                    "question": "Name the functional group present in ethers.",
                    "answer": "-O- (an oxygen atom linking two alkyl/aryl groups)"
                },
                {
                    "question": "Define a primary amine with an example.",
                    "answer": "An amine with one alkyl/aryl group attached to nitrogen, e.g. methylamine (CH3NH2)."
                },
                {
                    "question": "Define a polymer with an example.",
                    "answer": "A large molecule made of repeating structural units called monomers, e.g. polyethylene made from ethylene monomers."
                },
                {
                    "question": "Classify vitamins based on solubility.",
                    "answer": "Fat-soluble (A, D, E, K) and water-soluble (B-complex, C)."
                },
                {
                    "question": "Name the two types of nucleic acids found in living organisms.",
                    "answer": "DNA (deoxyribonucleic acid) and RNA (ribonucleic acid)."
                },
                {
                    "question": "Define an enzyme.",
                    "answer": "A biological catalyst, usually a protein, that speeds up specific biochemical reactions in living organisms."
                },
                {
                    "question": "What is glycolysis?",
                    "answer": "The metabolic pathway that breaks down one molecule of glucose into two molecules of pyruvate, releasing energy as ATP."
                }
            ],
            "Inorganic Chemistry": [
                {
                    "question": "Modern periodic law statement.",
                    "answer": "Properties of elements are periodic functions of their atomic number."
                },
                {
                    "question": "General trend of metallic character across a period.",
                    "answer": "Metallic character decreases from left to right across a period."
                },
                {
                    "question": "Define isotopes with an example.",
                    "answer": "Atoms of the same element with the same number of protons but different numbers of neutrons, e.g. C-12 and C-14."
                },
                {
                    "question": "Name the gas responsible for the greenhouse effect that is most abundant from human activity.",
                    "answer": "Carbon dioxide (CO2)."
                },
                {
                    "question": "What is the biological importance of hemoglobin's iron content?",
                    "answer": "Iron in hemoglobin binds oxygen for transport through the bloodstream."
                },
                {
                    "question": "Which element is essential for chlorophyll structure in plants?",
                    "answer": "Magnesium"
                },
                {
                    "question": "Name the group of elements known as noble gases and state their key property.",
                    "answer": "Group 18 elements (He, Ne, Ar, Kr, Xe, Rn); they are chemically inert due to complete outer electron shells."
                },
                {
                    "question": "Define transition elements.",
                    "answer": "Elements with partially filled d-orbitals in their ground state or common oxidation states, located in the d-block."
                },
                {
                    "question": "Name the group 1 elements and state one common property.",
                    "answer": "Alkali metals (Li, Na, K, Rb, Cs, Fr); they are highly reactive, soft metals that form +1 ions."
                },
                {
                    "question": "Name the group 17 elements and state one common property.",
                    "answer": "Halogens (F, Cl, Br, I, At); they are highly reactive non-metals that readily gain one electron to form -1 ions."
                },
                {
                    "question": "Define hardness of water.",
                    "answer": "The presence of dissolved calcium and magnesium salts in water that prevents soap from forming a lather easily."
                },
                {
                    "question": "State the approximate pH of pure water at room temperature.",
                    "answer": "7 (neutral)"
                },
                {
                    "question": "Define a buffer solution.",
                    "answer": "A solution that resists changes in pH upon addition of small amounts of acid or base."
                },
                {
                    "question": "Define electrolysis.",
                    "answer": "The process of using electrical energy to drive a non-spontaneous chemical reaction, e.g. decomposition of a compound."
                },
                {
                    "question": "Define corrosion (rusting) and name one prevention method.",
                    "answer": "The gradual destruction of metals by chemical reaction with the environment; prevention includes galvanization (zinc coating)."
                },
                {
                    "question": "Define an ionic bond.",
                    "answer": "A chemical bond formed by the electrostatic attraction between oppositely charged ions."
                },
                {
                    "question": "Define a coordinate (dative) covalent bond.",
                    "answer": "A covalent bond where both shared electrons come from the same atom (the donor), e.g. in the ammonium ion NH4+."
                },
                {
                    "question": "Name the industrial process used to manufacture ammonia and its key catalyst.",
                    "answer": "The Haber process, using an iron catalyst under high pressure and moderate temperature."
                },
                {
                    "question": "Which magnesium-containing biomolecule is essential for photosynthesis?",
                    "answer": "Chlorophyll"
                },
                {
                    "question": "Which iron-containing biomolecule transports oxygen in blood?",
                    "answer": "Hemoglobin"
                }
            ]
        }
    },
    "CAT": {
        "Quant": {
            "Arithmetic": [
                {
                    "question": "Define the allegation rule formula ratio relationship.",
                    "answer": "Cheaper Quantity / Dearer Quantity = (Dearer Price - Mean Price) / (Mean Price - Cheaper Price)"
                },
                {
                    "question": "Formula for effective compound interest rate when compounding occurs half-yearly.",
                    "answer": "R_eff = (1 + R / 200)^2 - 1"
                },
                {
                    "question": "If speed ratios scale as a:b, what is the corresponding travel duration ratio?",
                    "answer": "b : a (inverse variance tracking properties)"
                },
                {
                    "question": "Work efficiency rule expression relating men, days, and output volume metric variables.",
                    "answer": "(M_1 * D_1 * H_1) / W_1 = (M_2 * D_2 * H_2) / W_2"
                },
                {
                    "question": "Express relationship between LCM, HCF, and product limits of two numbers A and B.",
                    "answer": "LCM(A,B) * HCF(A,B) = A * B"
                },
                {
                    "question": "Two values fluctuate as 20% growth and 20% decay. Express net percentage variance.",
                    "answer": "Net 4% drop down across final values."
                },
                {
                    "question": "Formula for calculating a discount sequence of x% followed by y%.",
                    "answer": "Net Discount = (x + y - (x * y / 100))%"
                },
                {
                    "question": "Express relative velocity computation when two objects speed along matching tracks.",
                    "answer": "Relative speed = |V_1 - V_2|"
                },
                {
                    "question": "Express relative velocity computation when two objects run opposite directions.",
                    "answer": "Relative speed = V_1 + V_2"
                },
                {
                    "question": "Express relationship defining average speed mapping across matching distance slots.",
                    "answer": "Average Speed = (2 * v_1 * v_2) / (v_1 + v_2)"
                },
                {
                    "question": "Formula for finding simple interest accumulation values.",
                    "answer": "SI = (P * R * T) / 100"
                },
                {
                    "question": "Express final compounding balance equation formula parameters.",
                    "answer": "A = P * (1 + R/100)^T"
                },
                {
                    "question": "Difference between CI and SI for 2 years duration constants.",
                    "answer": "Difference = P * (R / 100)^2"
                },
                {
                    "question": "Difference between CI and SI for 3 years duration constants.",
                    "answer": "Difference = P * (R / 100)^2 * (3 + R / 100)"
                },
                {
                    "question": "Rule configuration defining profit percentages over cost baseline variables.",
                    "answer": "Profit % = ((Selling Price - Cost Price) / Cost Price) * 100"
                },
                {
                    "question": "Rule configuration defining loss percentages over cost baseline variables.",
                    "answer": "Loss % = ((Cost Price - Selling Price) / Cost Price) * 100"
                },
                {
                    "question": "What does a partnership configuration map if capital timelines vary?",
                    "answer": "Profit split scales according to the product of investment capital and active timeline allocation: C_1*T_1 : C_2*T_2."
                },
                {
                    "question": "Express net downstream vector velocity relating boat speed B and stream flow S.",
                    "answer": "Downstream speed = B + S"
                },
                {
                    "question": "Express net upstream vector velocity relating boat speed B and stream flow S.",
                    "answer": "Upstream speed = B - S"
                },
                {
                    "question": "If a pipe fills tank surfaces over X hours, what fraction loads inside one hour?",
                    "answer": "1 / X total volume share capacity metrics."
                }
            ],
            "Algebra": [
                {
                    "question": "What is the combinations equation to distribute n items containing p identical entities?",
                    "answer": "Total paths = n! / p!"
                },
                {
                    "question": "Solve for base element x constraints if: log_2(x) + log_4(x) = 6.",
                    "answer": "Calculated value x = 16"
                },
                {
                    "question": "Condition for a quadratic expression ax^2 + bx + c to be always positive for all real x.",
                    "answer": "a > 0 and discriminant D < 0 (b^2 - 4ac < 0)"
                },
                {
                    "question": "Sum of an infinite geometric progression sequence configuration constraint.",
                    "answer": "S_inf = a / (1 - r) provided absolute ratio bounds stay beneath unity (|r| < 1)."
                },
                {
                    "question": "State the relationship between Arithmetic Mean (AM) and Geometric Mean (GM).",
                    "answer": "AM >= GM for all positive real numbers."
                },
                {
                    "question": "Find product values tracking all roots inside quadratic ax^2 + bx + c = 0.",
                    "answer": "Product = c / a"
                },
                {
                    "question": "Find sum values tracking all roots inside quadratic ax^2 + bx + c = 0.",
                    "answer": "Sum = -b / a"
                },
                {
                    "question": "Express sum equation formatting across n values inside arithmetic sequences.",
                    "answer": "S_n = (n / 2) * [2a + (n - 1)d]"
                },
                {
                    "question": "Express value mapping calculation for the n-th slot inside geometric progressions.",
                    "answer": "T_n = a * r^(n - 1)"
                },
                {
                    "question": "Sum of the first 'n' natural numbers formula expression.",
                    "answer": "S = [n * (n + 1)] / 2"
                },
                {
                    "question": "Sum of cubes of the first 'n' natural numbers formula expression.",
                    "answer": "S = [n * (n + 1) / 2]^2"
                },
                {
                    "question": "Express baseline condition generating equal roots across quadratic parameters.",
                    "answer": "Discriminant equals zero (b^2 - 4ac = 0)."
                },
                {
                    "question": "Express baseline condition generating imaginary roots across quadratic parameters.",
                    "answer": "Discriminant drops below zero (b^2 - 4ac < 0)."
                },
                {
                    "question": "Logarithmic base change rule transformation statement identity.",
                    "answer": "log_a(b) = log_c(b) / log_c(a)"
                },
                {
                    "question": "Number of terms inside full multinomial expansions mapping (x + y)^n layouts.",
                    "answer": "n + 1 distinct terms."
                },
                {
                    "question": "Write the identity mapping expansion format for a^3 - b^3.",
                    "answer": "(a - b) * (a^2 + ab + b^2)"
                },
                {
                    "question": "Express geometric mean computation across two metrics A and B.",
                    "answer": "GM = sqrt(A * B)"
                },
                {
                    "question": "Express harmonic mean computation across two metrics A and B.",
                    "answer": "HM = (2 * A * B) / (A + B)"
                },
                {
                    "question": "Maximum value of product X * Y when their sum X + Y is a constant C.",
                    "answer": "Occurs when X = Y = C / 2."
                },
                {
                    "question": "Express linear solution behavior if system profiles show: a_1/a_2 == b_1/b_2 != c_1/c_2.",
                    "answer": "The system represents parallel lines and contains zero valid solutions."
                }
            ],
            "Geometry & Mensuration": [
                {
                    "question": "Formula for the area of a triangle given base and height.",
                    "answer": "Area = (1/2) * base * height"
                },
                {
                    "question": "Formula for the area of a triangle using Heron's formula.",
                    "answer": "Area = sqrt(s(s-a)(s-b)(s-c)), where s = (a+b+c)/2"
                },
                {
                    "question": "Pythagoras theorem statement for a right triangle.",
                    "answer": "Hypotenuse^2 = Base^2 + Perpendicular^2"
                },
                {
                    "question": "Formula for the area of a circle.",
                    "answer": "Area = pi * r^2"
                },
                {
                    "question": "Formula for the curved surface area of a cylinder.",
                    "answer": "CSA = 2 * pi * r * h"
                },
                {
                    "question": "Formula for the volume of a cone.",
                    "answer": "Volume = (1/3) * pi * r^2 * h"
                },
                {
                    "question": "Formula for the volume of a sphere.",
                    "answer": "Volume = (4/3) * pi * r^3"
                },
                {
                    "question": "Property of angles in a cyclic quadrilateral.",
                    "answer": "Opposite angles are supplementary, i.e. they sum to 180 degrees."
                },
                {
                    "question": "Formula for the exterior angle sum of any polygon.",
                    "answer": "360 degrees, regardless of the number of sides."
                },
                {
                    "question": "Formula relating the sum of interior angles of an n-sided polygon.",
                    "answer": "Sum = (n-2) * 180 degrees"
                },
                {
                    "question": "Condition for two triangles to be similar (AA similarity criterion).",
                    "answer": "If two angles of one triangle equal two angles of another, the triangles are similar."
                },
                {
                    "question": "Circle theorem: angle subtended by a diameter at any point on the circle.",
                    "answer": "It is always a right angle (90 degrees) - angle in a semicircle."
                },
                {
                    "question": "Property of a tangent to a circle at the point of contact.",
                    "answer": "The tangent is always perpendicular to the radius drawn to the point of contact."
                },
                {
                    "question": "Formula for the area of a trapezium with parallel sides a, b and height h.",
                    "answer": "Area = (1/2) * (a+b) * h"
                },
                {
                    "question": "Formula for the total surface area of a cube with side a.",
                    "answer": "TSA = 6 * a^2"
                },
                {
                    "question": "Formula for the total surface area of a cuboid with dimensions l, b, h.",
                    "answer": "TSA = 2*(lb + bh + hl)"
                },
                {
                    "question": "Formula for the volume of a frustum of a cone.",
                    "answer": "Volume = (pi*h/3) * (R^2 + r^2 + R*r)"
                },
                {
                    "question": "Distance formula between two points (x1,y1) and (x2,y2).",
                    "answer": "d = sqrt((x2-x1)^2 + (y2-y1)^2)"
                },
                {
                    "question": "Section formula for a point dividing a line segment in ratio m:n.",
                    "answer": "((m*x2+n*x1)/(m+n), (m*y2+n*y1)/(m+n))"
                },
                {
                    "question": "Formula for the volume of a prism.",
                    "answer": "Volume = Base Area * Height"
                }
            ],
            "Number System": [
                {
                    "question": "Formula to find the number of factors of N = a^p * b^q * c^r.",
                    "answer": "Number of factors = (p+1)(q+1)(r+1)"
                },
                {
                    "question": "Condition for a number to be divisible by 3.",
                    "answer": "The sum of its digits must be divisible by 3."
                },
                {
                    "question": "Condition for a number to be divisible by 11.",
                    "answer": "The difference between the sum of digits at odd and even positions must be 0 or a multiple of 11."
                },
                {
                    "question": "Formula for the sum of the first n natural numbers.",
                    "answer": "Sum = n(n+1)/2"
                },
                {
                    "question": "Define a perfect number with an example.",
                    "answer": "A number equal to the sum of its proper divisors, e.g. 28 = 1+2+4+7+14."
                },
                {
                    "question": "Formula to find the highest power of a prime p dividing n!.",
                    "answer": "Sum of floor(n/p^k) for k = 1,2,3,... until p^k exceeds n."
                },
                {
                    "question": "Remainder theorem shortcut: find remainder when a^n is divided by m using Euler's theorem.",
                    "answer": "If gcd(a,m)=1, a^(phi(m)) is congruent to 1 (mod m), where phi is Euler's totient function."
                },
                {
                    "question": "Definition of relatively prime (coprime) numbers.",
                    "answer": "Two numbers whose greatest common divisor (HCF) is 1."
                },
                {
                    "question": "Define a prime number.",
                    "answer": "A natural number greater than 1 with exactly two factors: 1 and itself."
                },
                {
                    "question": "Distinguish face value and place value of a digit in a number.",
                    "answer": "Face value is the digit itself; place value is the digit multiplied by its positional power of 10."
                },
                {
                    "question": "Shortcut for finding the unit digit of a^n using cyclicity.",
                    "answer": "Find the cyclicity pattern of the unit digit of the base 'a' and use n mod (cycle length) to pick the correct position."
                },
                {
                    "question": "Divisibility rule for 7.",
                    "answer": "Double the last digit, subtract it from the rest of the number; if the result is divisible by 7, so is the original number."
                },
                {
                    "question": "Property of the sum of two consecutive perfect squares' relation to odd numbers.",
                    "answer": "The difference of squares of consecutive integers n and n+1 is always the odd number (2n+1)."
                },
                {
                    "question": "Formula for converting a decimal number to binary.",
                    "answer": "Repeatedly divide the number by 2 and record remainders; the binary number is the remainders read in reverse order."
                },
                {
                    "question": "Define a rational number.",
                    "answer": "A number that can be expressed as p/q, where p and q are integers and q is not zero."
                },
                {
                    "question": "State the relation between LCM and HCF of two numbers a and b.",
                    "answer": "LCM(a,b) * HCF(a,b) = a * b"
                },
                {
                    "question": "Property used to quickly check divisibility by 9.",
                    "answer": "A number is divisible by 9 if the sum of its digits is divisible by 9."
                },
                {
                    "question": "Define a composite number.",
                    "answer": "A natural number greater than 1 that has more than two factors (i.e., it is not prime)."
                }
            ]
        },
        "DILR": {
            "Data Interpretation": [
                {
                    "question": "What is the first step when approaching a DI set with multiple tables/charts?",
                    "answer": "Spend time understanding what data is given and how the tables/charts relate before attempting questions."
                },
                {
                    "question": "How do you calculate percentage change between two data points?",
                    "answer": "((New Value - Old Value) / Old Value) * 100"
                },
                {
                    "question": "In a pie chart, how do you convert a given percentage share to degrees?",
                    "answer": "Degrees = (Percentage / 100) * 360"
                },
                {
                    "question": "What does a line graph typically emphasize in DI questions?",
                    "answer": "Trends and rate of change of a variable over time."
                },
                {
                    "question": "How is a weighted average calculated across multiple categories?",
                    "answer": "Weighted Average = Sum(value_i * weight_i) / Sum(weight_i)"
                },
                {
                    "question": "What is a caselet in CAT DILR?",
                    "answer": "A data set presented in paragraph/text form (rather than tables or charts) that requires the reader to extract structured data."
                },
                {
                    "question": "Key strategy tip for approaching DILR sets under time pressure.",
                    "answer": "Skim all sets first, attempt the most straightforward/least ambiguous set first to secure quick accuracy."
                },
                {
                    "question": "What does a stacked bar chart typically show that a simple bar chart cannot?",
                    "answer": "It shows both the total value and the breakdown of that total into sub-categories within a single bar."
                },
                {
                    "question": "What relationship does a scatter plot typically help identify?",
                    "answer": "The correlation or trend between two numerical variables."
                },
                {
                    "question": "What does a radar (spider) chart help compare?",
                    "answer": "Multiple quantitative variables of several entities on axes radiating from a central point."
                },
                {
                    "question": "What is an index number used for in DI questions?",
                    "answer": "To express the relative change of a variable compared to a fixed base period, usually set to 100."
                },
                {
                    "question": "Formula for Compound Annual Growth Rate (CAGR).",
                    "answer": "CAGR = ((Ending Value / Beginning Value)^(1/n) - 1) * 100, where n is the number of years."
                },
                {
                    "question": "How is ratio-proportion typically applied in DI questions?",
                    "answer": "To scale known quantities to find an unknown quantity when the relationship between two variables is fixed."
                },
                {
                    "question": "Strategy tip for a DI table with a missing value.",
                    "answer": "Use the given row/column totals and known relationships to back-calculate the missing figure."
                },
                {
                    "question": "How can a Venn diagram help in DI-based set questions?",
                    "answer": "It visually partitions overlapping categories, making it easier to compute unique and combined counts."
                },
                {
                    "question": "What is a good approximation strategy for DI questions with large numbers?",
                    "answer": "Round values sensibly and estimate rather than compute exact figures, especially for 'which is highest/lowest' type questions."
                },
                {
                    "question": "What does a line graph best help visualize in DI sets?",
                    "answer": "Trends and rate of change of one or more variables over a continuous time period."
                },
                {
                    "question": "Formula for finding percentage change between two data points.",
                    "answer": "((New Value - Old Value) / Old Value) * 100"
                },
                {
                    "question": "How do you convert a pie chart percentage share into degrees?",
                    "answer": "Degrees = (Percentage / 100) * 360"
                },
                {
                    "question": "Formula for a weighted average across multiple categories.",
                    "answer": "Weighted Average = Sum(value_i * weight_i) / Sum(weight_i)"
                }
            ],
            "Logical Reasoning": [
                {
                    "question": "In seating arrangement puzzles, what is the first step?",
                    "answer": "Draw the arrangement diagram and place fixed/definite clues first before working through relative clues."
                },
                {
                    "question": "How do you approach syllogism questions effectively?",
                    "answer": "Use Venn diagrams to visually check whether the conclusion necessarily follows from the given premises."
                },
                {
                    "question": "What does a blood relation puzzle typically test?",
                    "answer": "The ability to trace family relationships across generations using given clues to answer relationship queries."
                },
                {
                    "question": "In binary/ternary logic puzzles, what is a key technique?",
                    "answer": "Build a grid and eliminate impossible combinations systematically using each clue."
                },
                {
                    "question": "What is the key rule when solving a Directions and Distances puzzle?",
                    "answer": "Fix a starting point and consistently track orientation changes (left/right turns) on an imaginary compass grid."
                },
                {
                    "question": "What is the main goal of a Venn diagram based set-theory question?",
                    "answer": "To determine the count of elements in different overlapping regions using inclusion-exclusion principles."
                },
                {
                    "question": "Inclusion-exclusion formula for two overlapping sets A and B.",
                    "answer": "n(A union B) = n(A) + n(B) - n(A intersection B)"
                },
                {
                    "question": "What is coding-decoding in logical reasoning?",
                    "answer": "A puzzle type where letters/numbers are substituted by a rule, and the solver must decode or apply the same rule to a new term."
                },
                {
                    "question": "Key approach for blood relation puzzles with multiple generations.",
                    "answer": "Draw a family tree diagram as clues are read, marking gender and generation level clearly."
                },
                {
                    "question": "Key technique for solving number/letter series completion questions.",
                    "answer": "Look for a consistent arithmetic, geometric, or alternating pattern between consecutive terms."
                },
                {
                    "question": "Approach tip for clock-based reasoning puzzles.",
                    "answer": "Remember the minute hand moves 6 degrees per minute and the hour hand moves 0.5 degrees per minute, then compute the angle or time difference accordingly."
                },
                {
                    "question": "Approach tip for calendar-based reasoning puzzles.",
                    "answer": "Use the fact that days of the week repeat every 7 days, and account for leap years when counting odd days."
                },
                {
                    "question": "What skill do cubes and dice puzzles primarily test?",
                    "answer": "3D spatial visualization, especially tracking which faces are opposite, adjacent, or hidden after rotation."
                },
                {
                    "question": "What is an input-output reasoning question testing?",
                    "answer": "The ability to detect a hidden rule (e.g., sorting/shifting rule) applied step-by-step to a given input sequence."
                },
                {
                    "question": "Key strategy for matrix-based arrangement puzzles.",
                    "answer": "Draw a grid and eliminate impossible cell placements systematically using each given clue."
                },
                {
                    "question": "What does a 'statement and assumption' question test?",
                    "answer": "Whether a given assumption is implicitly taken for granted by the statement, even though not explicitly stated."
                },
                {
                    "question": "What does a 'statement and conclusion' question test?",
                    "answer": "Whether the given conclusion logically and definitely follows from the statement provided."
                },
                {
                    "question": "Inclusion-exclusion formula for two overlapping sets A and B.",
                    "answer": "n(A union B) = n(A) + n(B) - n(A intersection B)"
                },
                {
                    "question": "Key rule for directions and distances puzzles.",
                    "answer": "Fix a starting point and consistently track orientation changes (left/right turns) on an imaginary compass grid."
                }
            ]
        },
        "VARC": {
            "Verbal Ability": [
                {
                    "question": "What is the main goal of a Para-jumble question?",
                    "answer": "To rearrange jumbled sentences into a logically coherent paragraph by identifying the opening/linking sentences."
                },
                {
                    "question": "What should you look for first in a Para-jumble to find the opening sentence?",
                    "answer": "A sentence that introduces the topic generally, without pronouns referring back to something not yet mentioned."
                },
                {
                    "question": "What is the purpose of an odd-sentence-out (para-summary related) question?",
                    "answer": "To identify the sentence that does not fit the theme or logical flow of an otherwise coherent paragraph."
                },
                {
                    "question": "What does a para-summary question require you to identify?",
                    "answer": "The option that best captures the core idea of the passage without omitting essential points or adding new ones."
                },
                {
                    "question": "Define a synonym versus an antonym.",
                    "answer": "A synonym has a similar meaning to a word; an antonym has an opposite meaning."
                },
                {
                    "question": "What is the key strategy for critical reasoning (verbal logic) questions?",
                    "answer": "Identify the premise and conclusion, then evaluate whether the given statement strengthens, weakens, or is irrelevant to the argument."
                },
                {
                    "question": "What is the main goal of a sentence correction question?",
                    "answer": "To identify and fix grammatical errors in a sentence while preserving its intended meaning."
                },
                {
                    "question": "What skill do fill-in-the-blanks vocabulary questions test?",
                    "answer": "The ability to choose the word that best fits both the grammatical and contextual meaning of the sentence."
                },
                {
                    "question": "Define an idiom with an example.",
                    "answer": "A fixed phrase whose figurative meaning differs from its literal words, e.g. 'spill the beans' meaning to reveal a secret."
                },
                {
                    "question": "What does an analogy question test?",
                    "answer": "The ability to identify a relationship between a pair of words and find another pair sharing the same relationship."
                },
                {
                    "question": "Define one-word substitution with an example.",
                    "answer": "Replacing a phrase with a single word of the same meaning, e.g. 'a person who studies birds' = 'ornithologist'."
                },
                {
                    "question": "Rule for converting active voice to passive voice.",
                    "answer": "The object of the active sentence becomes the subject, and the verb is changed to a form of 'be' plus the past participle."
                },
                {
                    "question": "Rule for converting direct speech to indirect speech.",
                    "answer": "Remove quotation marks, adjust the reporting verb tense, and shift pronouns and time references accordingly."
                },
                {
                    "question": "What does an error-spotting question require?",
                    "answer": "Identifying the specific part of a sentence that contains a grammatical or usage error."
                },
                {
                    "question": "What does a phrase replacement (sentence improvement) question test?",
                    "answer": "The ability to select the grammatically and stylistically best replacement for an underlined portion of a sentence."
                },
                {
                    "question": "What is the key strategy for critical reasoning (verbal logic) questions?",
                    "answer": "Identify the premise and conclusion, then evaluate whether the given statement strengthens, weakens, or is irrelevant to the argument."
                },
                {
                    "question": "Define a synonym versus an antonym.",
                    "answer": "A synonym has a similar meaning to a word; an antonym has an opposite meaning."
                }
            ],
            "Reading Comprehension": [
                {
                    "question": "What is the recommended first step when approaching an RC passage?",
                    "answer": "Read the passage once for overall structure and main idea before attempting to answer specific questions."
                },
                {
                    "question": "What does an 'inference' based RC question require?",
                    "answer": "Identifying what can be logically concluded from the passage, even though it is not directly stated."
                },
                {
                    "question": "What is the difference between the main idea and a supporting detail in RC?",
                    "answer": "The main idea is the central point of the passage; supporting details are the specific facts/examples that back it up."
                },
                {
                    "question": "What does a 'tone of the passage' question test?",
                    "answer": "The author's attitude or emotional stance toward the subject, e.g. critical, neutral, appreciative."
                },
                {
                    "question": "Strategy tip for vocabulary-in-context RC questions.",
                    "answer": "Substitute the answer choices back into the sentence and check which preserves the original meaning in context."
                },
                {
                    "question": "Distinguish skimming from scanning while reading an RC passage.",
                    "answer": "Skimming captures the overall gist quickly; scanning searches for specific details or keywords."
                },
                {
                    "question": "What does an 'author's purpose' question ask you to identify?",
                    "answer": "Why the author wrote the passage, e.g. to inform, persuade, criticize, or entertain."
                },
                {
                    "question": "What does a 'primary purpose of the passage' question test?",
                    "answer": "The ability to identify the single overarching goal the entire passage is trying to achieve."
                },
                {
                    "question": "Name common RC passage themes tested in CAT.",
                    "answer": "Science and technology, economics and business, philosophy, history, and literary/cultural criticism."
                },
                {
                    "question": "Distinguish a fact from an opinion in an RC passage.",
                    "answer": "A fact is a verifiable, objective statement; an opinion is a subjective judgment or belief of the author."
                },
                {
                    "question": "What does a para-completion question require?",
                    "answer": "Selecting the sentence that most logically completes a paragraph while maintaining its tone and flow."
                },
                {
                    "question": "What is the best elimination strategy for tricky RC multiple-choice options?",
                    "answer": "Eliminate options that are too extreme, only partially true, or not directly supported by the passage's text."
                },
                {
                    "question": "How should you manage time across long and short RC passages in CAT?",
                    "answer": "Attempt shorter, easier passages first to bank quick marks, then allocate remaining time to longer or denser passages."
                },
                {
                    "question": "What does a 'main argument' type RC question test?",
                    "answer": "The ability to identify the central claim the author is trying to establish and support with evidence."
                },
                {
                    "question": "What role do contrast cue words like 'however' and 'but' play in RC passages?",
                    "answer": "They signal a shift in the author's argument or tone, often indicating an important qualification or counterpoint."
                },
                {
                    "question": "What is the recommended first step when approaching an RC passage?",
                    "answer": "Read the passage once for overall structure and main idea before attempting to answer specific questions."
                },
                {
                    "question": "What does an 'inference' based RC question require?",
                    "answer": "Identifying what can be logically concluded from the passage, even though it is not directly stated."
                },
                {
                    "question": "What does a 'tone of the passage' question test?",
                    "answer": "The author's attitude or emotional stance toward the subject, e.g. critical, neutral, appreciative."
                },
                {
                    "question": "Strategy tip for vocabulary-in-context RC questions.",
                    "answer": "Substitute the answer choices back into the sentence and check which preserves the original meaning in context."
                }
            ]
        }
    }
}