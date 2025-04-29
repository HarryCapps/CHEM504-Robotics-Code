# CHEM504-Robotics-Code
This GitHub repository contains the code used in a research project for _CHEM504 - Robotics and Automation in Chemistry_ at the University of Liverpool.

## Description

### Project Overview

This project involves automating the Blue Bottle Experiment using a UR5e robotic arm and computer vision. Working in groups, a system to perform the experiment autonomously, detect colour changes, and potentially analyse the reaction kinetics will be designed. Subject to chemical availability, phenosafranine, indigo carmine, and resazurin may also be considered.

### The Blue Bottle Experiment

The Blue Bottle Experiment demonstrates the reversible oxidation and reduction of methylene blue. When shaken, the solution mixes with oxygen, oxidising methylene blue to its blue form. Over time, the dissolved oxygen is consumed by glucose in the reaction, and methylene blue is reduced to its colourless (leuco) form.

![image](https://github.com/user-attachments/assets/f0d46fd7-f9c2-44cb-8bfc-536ab88977f2)

### Resazurin Test

The resazurin test demonstrates the reversible oxidation and reduction of the redox indicator resazurin. In its oxidised form, resazurin is blue. In its reduced form, resofurin is pink. This reaction has applications in the alamarBlue™ assay, which is a cell viability assay that measures cell proliferation and cytotoxicity using the metabolic activity of living cells, converting resazurin to resorufin.

![image](https://github.com/user-attachments/assets/29d70cac-7c86-445c-af21-293f21e1efc4)

Adapted from Uzarski _et al._ (J. S. Uzarski, M. D. DiVito, J. A. Wertheim, W. M. Miller, _Biomaterials_, 2017, **129**, 163-175).

#### Kinetics

The reaction follows first-order kinetics with respect to hydroxide ions, methylene blue, and glucose, while it is zero-order with respect to oxygen. The rate of reaction can be determined by measuring the time it takes for a solution of known concentrations to lose its colour.

To determine the activation energy, an Arrhenius plot can be used. This involves plotting the natural logarithm of the decolouration time against the inverse of the absolute temperature. As explained by Campbell, this approach is valid because the rate-determining step does not depend on the oxygen concentration. Therefore, the time taken for the solution to turn colourless is directly related to the rate constnat. This relationship yields a straight line in the Arrhenius plot.

J. A. Campbell, _J. Chem. Educ._, 1963, **40**, 578.

### "Chemical Traffic Light" Experiment

The "Chemical Traffic Light" experiment is a redox reaction that demonstrates colour changes based on oxidation states. A solution containing indigo carmine, glucose (a reducing agent), and sodium hydroxide or potassium hydroxide in water changes colour when shaken and left to rest. When oxygen is introduced by shaking, indigo carmine is oxidised, turning the solution red. As the oxygen is consumed, it transitions through yellow (partially reduced) to green (fully reduced) when left undisturbed. This reversible cycle, driven by oxidation from air and reduction by glucose, mimics a traffic light sequence and illustrates redox chemistry and reaction kinetics.

![image](https://github.com/user-attachments/assets/f2aa221a-4378-4d13-a24b-a467d02ccecd)

Adapted from Habibi _et al._ (S. C. Habibi, B. K. Bloom, A. E. Sjoblom, O. W. Schmitz, A. Edwards, Z. R. Croasmun-Adams, R. J. DeLuca, J. S. Smith, K. L. Kuntz, _J. Chem. Edu._, 2024, **101**, 2505-2512.).

## Prerequisites

The following software is required to run the code and acquire the appropriate data:

- Visual Studio Code (or other code editor) - https://code.visualstudio.com/download
- Arduino IDE - https://www.arduino.cc/en/software
- Python (Anaconda is recommended. To install, click "Free Download using the URL") - https://www.anaconda.com/

The following pieces of equipment are also required:

- UR5e
- HD Web camera
- Hotplate stirrer
- Sample vial(s)
- 20 mm magnetic stirrer bar(s)
- White background

## Installation


## Usage

Below is a set of instructions for collecting data using the hardware listed before and the code provided.
1. Turn on the UR5e robotic arm.
2. Connect the HD Web camera to your computer.
3. Place your sample vials in the home position(s), each containing a 20 mm magnetic stirrer bar.
4. Position your camera in front of a white background where the robot will hold the sample vials for a given length of time.
5. Run the Robotic Movements Code.

## Authors
If you have any questions or would like additional information, please contact:
- Stephenie Bellew (sgsbelle@liverpool.ac.uk)
- Harry Capps (sghcapps@liverpool.ac.uk)
- Michael Gillin (sgmgilli@liverpool.ac.uk)

## License
This project is not currently licensed.

## Acknowledgements
The authors would like to thank Dr John Ward and Dr Gabriella Pizzuto for their tuition, support, and assistance during this project. The authors would also like to thank Laura Jones and Nikola Radulov for their assistance with the robotic functionalities. Lastly, the authors would like to thank the technicians in the Central Teaching Laboratories at the University of Liverpool for maintaining the equipment and keeping the students safe.
