import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
from PIL import Image

# Introduction
st.title('Urban Mobility Impact Assessment and Comparison Tool')
st.write('This is a prototype of a tool to help comparing potential impacts of policies on a local urban mobility '
         'scenario. It aims to provide a quick interface to compare impacts across user groups (personas) and across '
         'future scenarios. The standard values have been defined as reference values by the research team. The '
         'exemplary application aims to compare the impact of eight policies for different persona groups and across '
         '2030 scenarios, measured by CO2 equivalent (CO2e) emissions, energy demand in mega joule (MJ), and '
         'calories burned.')

# Information
st.subheader('Information')
st.write('You can reset the form by refreshing the website. No values or uploaded images are stored. The code is '
         'available on Github: https://github.com/TjarkGall/decision-tool-interface')
st.write('The concept was developed as part of the Institute Pascal research programme 2022 and has been continued as '
         'part of the work of the <a href="http://www.chaire-anthropolis.fr/">Anthropolis Chair.</a>',
         unsafe_allow_html=True)
st.subheader('Question?')
st.write('Contact Tjark Gall | tjark.gall@irt-systemx.fr')

# Anthropolis logo
image = Image.open('data/images/Anthropolis_logo_colour.png')
st.image(image, use_column_width=True)

# Step 2: Defining Future Scenarios
st.header('Defining Future Scenarios')

# Number of scenarios
st.subheader('Number of scenarios')
no_scen = st.slider('With how many scenarios do you want to work?', min_value=2, max_value=8, value=4)

# Scenario names and descriptions
st.subheader('Scenario names and descriptions')
scen_names = []
scen_desc = []
for i in range(no_scen):
    default_name = f'S{i + 1}: '
    if i == 0:
        default_name += 'Saclay 2.0'
        default_desc = 'Continuation of today’s development. The Saclay Plateau today is dominated by universities ' \
                       'and technology-related institutions. Some residential buildings and other functions ' \
                       'exist and are growing. Nevertheless, on weekend or holiday periods, ' \
                       'the plateau remains mostly empty. Saclay 2.0 would be the continuation of the ' \
                       'current growth. More university and technology functions would grow, complemented by ' \
                       'more residential buildings. Nevertheless, by 2030, ' \
                       'the character of the plateau remains to be largely linked to university’s seasonality and ' \
                       'depending on the incoming commuters, primarily between Tuesday and Thursday and ' \
                       'barely staying or utilising other functions on the plateau.'
    elif i == 1:
        default_name += 'Paris 2.0'
        default_desc = 'High-density, mixed-use neighbourhood. The second scenario is more optimistic on the ' \
                       'integrated development of the plateau. It assumes that a large number of residential' \
                       ' developments, going further than only student and international researcher housing, ' \
                       'adds a critical mass of population density to allow for a variety of other functions to ' \
                       'arise and remain active even in holiday seasons or weekends.'
    elif i == 2:
        default_name += 'Rural Campus'
        default_desc = 'Low-density, low diversity rural district. This scenario describes mostly the plateau as it ' \
                       'has been since the 1970s. While more offices and universities are added, its functions and ' \
                       'character remains primarily rural. Residential functions, as well as the accompanying ' \
                       'other functions, remain limited and their growth stagnates, maintaining primarily the status ' \
                       'quo of activity and functional mix.'
    elif i == 3:
        default_name += 'Village Campus'
        default_desc = 'High-density active core, surrounded by low-density. As a mix between the scenario ' \
                       '‘Paris 2.0’ and ‘Rural Campus’, this scenario is defined by overall low density and ' \
                       'restricted developments. However, it has modern yet traditional French village cores with ' \
                       'high level of mixed-use, walkability, and a range of bars and restaurants for students and ' \
                       'other inhabitants of the plateau.'
    else:
        default_name += f'Scenario {i + 1}'
        default_desc = ''
    scen_names.append(st.text_input(f'Scenario {i + 1} name:', value=default_name))
    scen_desc.append(st.text_area(f'Scenario {i + 1} description (max. 750 characters):',
                                  value=default_desc, max_chars=750))

# Scenario characteristics
st.subheader('Scenario characteristics')
st.write('Define the level of Intermodality (IM), Mixed Use (MU), Density (DE), and Public Transport (PT) for each '
         'of the scenarios from low to very high. These numbers are not taken into consideration in the calculation '
         'but shall help to distinguish the scenarios during the following steps.')

scen_chars_prep = [{"IM": "3: high", "MU": "1: low", "DE": "4: very high", "PT": "3: high", },
                   {"IM": "4: very high", "MU": "4: very high", "DE": "4: very high", "PT": "4: very high", },
                   {"IM": "2: medium", "MU": "1: low", "DE": "1: low", "PT": "2: medium", },
                   {"IM": "2: medium", "MU": "4: very high", "DE": "2: medium", "PT": "3: high"}, ]

if no_scen != len(scen_chars_prep):
    scen_chars_prep = [dict.fromkeys(scen_chars_prep[0]) for _ in range(no_scen)]

scen_chars = pd.DataFrame(scen_chars_prep, index=scen_names)
scen_chars.IM = scen_chars.IM.astype("category")
scen_chars.MU = scen_chars.MU.astype("category")
scen_chars.DE = scen_chars.DE.astype("category")
scen_chars.PT = scen_chars.PT.astype("category")

cols = ["IM", "MU", "DE", "PT"]

for col in cols:
    categories = list(scen_chars[col].cat.categories)
    for cat in ["1: low", "2: medium", "3: high", "4: very high"]:
        if cat not in categories:
            scen_chars[col] = scen_chars[col].cat.add_categories(cat)

scen_chars.IM = scen_chars.IM.cat.set_categories(["1: low", "2: medium", "3: high", "4: very high"])
scen_chars.MU = scen_chars.MU.cat.set_categories(["1: low", "2: medium", "3: high", "4: very high"])
scen_chars.DE = scen_chars.DE.cat.set_categories(["1: low", "2: medium", "3: high", "4: very high"])
scen_chars.PT = scen_chars.PT.cat.set_categories(["1: low", "2: medium", "3: high", "4: very high"])

scen_chars = st.experimental_data_editor(scen_chars)

# Scenario images
st.subheader('Scenario images')
scen_images = []
for i in range(no_scen):
    default_image_path = f'data/images/scenario_0{i + 1}.png'
    uploaded_files = st.file_uploader(f'Upload image(s) for {scen_names[i]}:', type=['jpg', 'jpeg', 'png'],
                                      key=f'scenario{i + 1}', accept_multiple_files=True)
    if uploaded_files:
        scen_images.append(uploaded_files[0])
    else:
        scen_images.append(default_image_path)

# Show scenario info
st.subheader('Scenario information')
for i in range(no_scen):
    st.write(f'### {scen_names[i]}')
    if scen_images[i] is not None:
        st.image(scen_images[i], width=300)
    st.write(scen_desc[i])
    st.write(scen_chars.loc[scen_names[i]])

# Step 3: Defining Future Personas
st.header('Defining Future Personas')

# Number of personas
st.subheader('Number of personas')
no_pers = st.slider('With how many personas do you want to work?', min_value=2, max_value=8, value=4)

# Persona names and descriptions
st.subheader('Persona names and descriptions')
pers_name = []
pers_desc = []
for i in range(no_pers):
    default_name = f''
    if i == 0:
        default_name += 'Jacqueline'
        default_desc = 'Jacqueline is a French woman aged 40 who works full-time at a technology company as a ' \
                       'manager, exercises daily and stays healthy. She appreciates her privacy and has flexible ' \
                       'work schedules. She doesn’t want to walk too much because she carries lots of bags around, ' \
                       'she prefers to cycle. She has no children and no partner and can be described as a ' \
                       'workaholic. She is a bit concerned with sustainability issues.'
    elif i == 1:
        default_name += 'Thierry'
        default_desc = 'Thierry is a 67-year-old man who visits the campus during the day to work. He is a professor ' \
                       'and will soon be retired. He comes to the plateau from time to time to give guest lectures ' \
                       'and lives inside Paris. He is not in charge of children. He usually uses public transport ' \
                       'but lately is struggling due to a leg injury. He is very concerned by sustainability.'
    elif i == 2:
        default_name += 'Adrian'
        default_desc = 'Adrian is a 35-year-old French man working part-time at a local supermarket in an ' \
                       'administrative function. He is in charge of two kindergarten and one primary school child. ' \
                       'He has a medium income. He has many time constraints and lots of activities and scheduled ' \
                       'meetings. He uses his car due to his complex daily movements and no possibility to deal ' \
                       'with delays. Sustainability is not the priority in his choices due to several constraints.'
    elif i == 3:
        default_name += 'Rui'
        default_desc = 'Rui is a 21-year-old female. She is an international undergrad exchange student from China, ' \
                       'studying at CentraleSupélec. She lives on the campus in one of the student residencies. ' \
                       'She mainly moves between her daily activities by walking and cycling because she cares about ' \
                       'sustainability and has not many alternatives. It is also cheaper.'
    else:
        default_name += f'Persona {i + 1}'
        default_desc = ''
    pers_name.append(st.text_input(f'Name of persona {i + 1}:', value=default_name))
    pers_desc.append(
        st.text_area(f'Description of persona {i + 1} (max. 250 char.):', value=default_desc, max_chars=250))

# Persona characteristics
st.subheader('Persona characteristics')
st.write('Set the number of home-work-home kilometres for a normal day for each persona and their weight in '
         'kilograms (for calorie calculations)')

# Define default values for all personas
default_values = {'Jacqueline': [60, 57], 'Thierry': [40, 84], 'Adrian': [10, 72], 'Rui': [4, 53]}
for i in range(4, no_pers):
    default_values[f'Persona {i + 1}'] = [0, 0]

# Create the DataFrame with the default values
pers_chars = pd.DataFrame.from_dict(default_values, orient='index', columns=['Distance (km)', 'Weight (kg)']).fillna(0)

# Persona images
st.subheader('Persona images')
pers_images = []
for i in range(no_pers):
    default_image_path = f'data/images/persona_0{i + 1}.png'
    uploaded_files = st.file_uploader(f'Upload image(s) for {pers_name[i]}:', type=['jpg', 'jpeg', 'png'],
                                      key=f'persona{i + 1}', accept_multiple_files=True)
    if uploaded_files:
        pers_images.append(uploaded_files[0])
    else:
        pers_images.append(default_image_path)

# Show persona info
st.subheader('Persona information')
for i in range(no_pers):
    st.write(f'### {pers_name[i]}')
    if pers_images[i] is not None:
        st.image(pers_images[i], width=300)
    st.write(pers_desc[i])
    st.write(pers_chars.loc[pers_name[i]])

# Step 4: Likelihood of scenarios
st.header('Likelihood of scenarios')

# Scenario description
st.write('Define for each of the scenarios the probability in % between 0 and 100. The sum must add up to 100.')

# Default values
default_values = [40, 15, 25, 20]
for i in range(no_scen - 4):
    default_values.append(0)

# Scenario likelihood sliders
total_likelihood = 0
for i in range(no_scen):
    scen_likelihood = st.slider(f'Likelihood of scenario {scen_names[i]} in percent:', min_value=0, max_value=100,
                                value=default_values[i], step=5)
    total_likelihood += scen_likelihood

# Calculate total likelihood
if total_likelihood != 100:
    st.error("Error: The sum of likelihoods must be equal to 100.")

# Display total likelihood
st.write(f'Total likelihood: {total_likelihood}%')
if total_likelihood != 100:
    st.write('Please adjust the likelihoods so that the sum is 100%.', unsafe_allow_html=True)
    st.markdown('<style>div.stError > p:first-child {color: red; font-weight: bold;}</style>', unsafe_allow_html=True)

# Number of people moving to/on the plateau per day
st.subheader('Number of people moving to/on the plateau per day')
no_people = st.number_input('How many people move to/on the plateau per day?', value=50000)

# Persona weights likelihood sliders
st.subheader('Persona weights in overall population')
st.write('Define for each of the personas the weight in percent between 0 and 100. 10 means that 10% of the overall '
         'population defined above are similar to the defined persona. The weights must add up to 100.')
pers_weights = []
for i in range(no_pers):
    default_weights = [10, 60, 20, 10] + [0] * (no_scen - 4)
    pers_weights.append(st.slider(f'Weight in percent of {pers_name[i]} in overall population:', min_value=0,
                                  max_value=100, step=5, value=default_weights[i], key=f"pers_weight_{i}"))
total_weights = sum(pers_weights)
st.write(f'Total weight: {total_weights}%')
if total_weights != 100:
    st.error('Total weight must be 100%')

# Step 5: Mode likelihoods
st.header('Likelihood to use mode per scenario and persona')

# Text description
st.write('In this section, we define for each of the scenarios the likelihood for each persona to use a certain mode. '
         'The range of likelihood to take a mode is 0 = unlikely, 1 = rather unlikely, 2 = rather likely, 3 = likely, '
         'and 4 = very likely. The modes are Mobility on Demand (MoD), Car, Bike, Walk, Micromobility (MM), Public '
         'Transport and MoD (PT-MoD), Public Transport and Bike (PT-Bike), Public Transport and Walk (PT-Walk), '
         'Public Transport and Micromobility (PT-MM), Car-Walk and Micromobility and Walk (MM-Walk). For multimodal '
         'trips, we assume 80% to be done with the first-mentioned mode and 20% by the second.')

# Default values for persona likelihoods to use certain types of transport
mode_prep_s1 = [
    # Jacqueline
    {'MoD': "2", 'Car': "3", 'Bike': "0", 'Walk': "0", 'MM': "0", 'PT-MoD': "3", 'PT-Bike': "1", 'PT-Walk': "3",
     'PT-MM': "1", 'MoD-Walk': "1", 'MoD-MM': "0", 'Car-Walk': "3", 'MM-Walk': "0"},
    # Thierry
    {'MoD': "3", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "3", 'PT-Bike': "0", 'PT-Walk': "2",
     'PT-MM': "0", 'MoD-Walk': "3", 'MoD-MM': "0", 'Car-Walk': "1", 'MM-Walk': "0"},
    # Adrian
    {'MoD': "3", 'Car': "3", 'Bike': "1", 'Walk': "1",
     'MM': "2", 'PT-MoD': "2", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "1", 'MoD-Walk': "3", 'MoD-MM': "3", 'Car-Walk': "4", 'MM-Walk': "0"},
    # Rui
    {'MoD': "3", 'Car': "0", 'Bike': "4", 'Walk': "4",
     'MM': "3", 'PT-MoD': "1", 'PT-Bike': "4", 'PT-Walk': "4",
     'PT-MM': "4", 'MoD-Walk': "1", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "4"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"}
]
mode_prep_s2 = [
    # Jacqueline
    {'MoD': "0", 'Car': "2", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "4", 'PT-Bike': "2", 'PT-Walk': "4",
     'PT-MM': "2", 'MoD-Walk': "1", 'MoD-MM': "0", 'Car-Walk': "1", 'MM-Walk': "0"},
    # Thierry
    {'MoD': "2", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "4", 'PT-Bike': "0", 'PT-Walk': "3",
     'PT-MM': "1", 'MoD-Walk': "3", 'MoD-MM': "1", 'Car-Walk': "1", 'MM-Walk': "0"},
    # Adrian
    {'MoD': "4", 'Car': "3", 'Bike': "1", 'Walk': "1",
     'MM': "2", 'PT-MoD': "2", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "1", 'MoD-Walk': "3", 'MoD-MM': "4", 'Car-Walk': "4", 'MM-Walk': "0"},
    # Rui
    {'MoD': "3", 'Car': "0", 'Bike': "4", 'Walk': "4",
     'MM': "3", 'PT-MoD': "1", 'PT-Bike': "4", 'PT-Walk': "4",
     'PT-MM': "4", 'MoD-Walk': "1", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "4"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"}
]
mode_prep_s3 = [
    # Jacqueline
    {'MoD': "3", 'Car': "4", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "1",
     'PT-MM': "0", 'MoD-Walk': "2", 'MoD-MM': "0", 'Car-Walk': "4", 'MM-Walk': "0"},
    # Thierry
    {'MoD': "1", 'Car': "1", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "2", 'PT-Bike': "0", 'PT-Walk': "1",
     'PT-MM': "0", 'MoD-Walk': "2", 'MoD-MM': "0", 'Car-Walk': "2", 'MM-Walk': "0"},
    # Adrian
    {'MoD': "3", 'Car': "4", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "1", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "2", 'MoD-MM': "2", 'Car-Walk': "4", 'MM-Walk': "0"},
    # Rui
    {'MoD': "0", 'Car': "0", 'Bike': "4", 'Walk': "3",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "2", 'PT-Walk': "3",
     'PT-MM': "1", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "1"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"}
]
mode_prep_s4 = [
    # Jacqueline
    {'MoD': "1", 'Car': "3", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "3", 'PT-Bike': "1", 'PT-Walk': "3",
     'PT-MM': "3", 'MoD-Walk': "1", 'MoD-MM': "0", 'Car-Walk': "4", 'MM-Walk': "0"},
    # Thierry
    {'MoD': "1", 'Car': "1", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "2", 'PT-Bike': "0", 'PT-Walk': "2",
     'PT-MM': "1", 'MoD-Walk': "3", 'MoD-MM': "1", 'Car-Walk': "2", 'MM-Walk': "0"},
    # Adrian
    {'MoD': "4", 'Car': "4", 'Bike': "0", 'Walk': "0",
     'MM': "1", 'PT-MoD': "1", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "3", 'MoD-MM': "2", 'Car-Walk': "4", 'MM-Walk': "0"},
    # Rui
    {'MoD': "3", 'Car': "2", 'Bike': "4", 'Walk': "3",
     'MM': "2", 'PT-MoD': "2", 'PT-Bike': "3", 'PT-Walk': "3",
     'PT-MM': "2", 'MoD-Walk': "2", 'MoD-MM': "1", 'Car-Walk': "1", 'MM-Walk': "3"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"}
]
mode_prep_s5 = [
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"},
    # Persona n
    {'MoD': "0", 'Car': "0", 'Bike': "0", 'Walk': "0",
     'MM': "0", 'PT-MoD': "0", 'PT-Bike': "0", 'PT-Walk': "0",
     'PT-MM': "0", 'MoD-Walk': "0", 'MoD-MM': "0", 'Car-Walk': "0", 'MM-Walk': "0"}
]
mode_prep_s6 = mode_prep_s5
mode_prep_s7 = mode_prep_s5
mode_prep_s8 = mode_prep_s5

mode_prep = {0: mode_prep_s1, 1: mode_prep_s2, 2: mode_prep_s3, 3: mode_prep_s4,
             4: mode_prep_s5, 5: mode_prep_s6, 6: mode_prep_s7, 7: mode_prep_s8}

modes = ["MoD", "Car", "Bike", "Walk", "MM", "PT-MoD", "PT-Bike", "PT-Walk", "PT-MM", "MoD-Walk", "MoD-MM", "Car-Walk",
         "MM-Walk"]

mode_pref_list = []

for i in range(no_scen):
    mode_pref = pd.DataFrame(mode_prep[i][0:no_pers], index=(pers_name[:no_pers]))
    for mode in modes:
        mode_pref[mode] = mode_pref[mode].astype("category")
        categories = list(mode_pref[mode].cat.categories)
        missing_categories = [cat for cat in ["0", "1", "2", "3", "4"] if cat not in categories]
        mode_pref[mode] = mode_pref[mode].cat.add_categories(missing_categories)
        mode_pref[mode] = mode_pref[mode].cat.set_categories(["0", "1", "2", "3", "4"])
        mode_pref[mode] = mode_pref[mode].cat.reorder_categories(sorted(mode_pref[mode].cat.categories))
    st.write(f'### {scen_names[i]}')
    st.write(
        f'How likely is it that each persona uses a certain mode in the scenario {scen_names[i]}? '
        f'(0 = unlikely, 4 = very likely)')
    if scen_images[i] is not None:
        st.image(scen_images[i], width=300)
    mode_pref = st.experimental_data_editor(mode_pref)
    mode_pref_list.append(mode_pref)


# Step 6: Mode likelihoods
st.header('Distribution of travel distances by mode and persona')
# Calculate kilometers per mode for each persona in scenario 1
dist_mode_list = []

for i in range(no_scen):
    dist_mode = mode_pref_list[i]
    dist_mode = dist_mode.astype(float)
    dist_mode = dist_mode.div(dist_mode.sum(axis=1), axis=0)
    dist_mode['PT'] = 0.8 * dist_mode['PT-MoD'] + 0.8 * dist_mode['PT-Bike'] + 0.8 * dist_mode['PT-Walk'] + \
                      0.8 * dist_mode['PT-MM']
    dist_mode['car_n'] = dist_mode['Car'] + 0.8 * dist_mode['Car-Walk']
    dist_mode['MoD_n'] = dist_mode['MoD'] + 0.2 * dist_mode['PT-MoD'] + 0.8 * dist_mode['MoD-Walk'] + \
                                                                          0.8 * dist_mode['MoD-MM']
    dist_mode['MM_n'] = dist_mode['MM'] + 0.2 * dist_mode['PT-MM'] + 0.2 * dist_mode['MoD-MM']
    dist_mode['Bike_n'] = dist_mode['Bike'] + 0.2 * dist_mode['PT-Bike']
    dist_mode['Walk_n'] = dist_mode['Walk'] + 0.2 * dist_mode['PT-Walk'] + 0.2 * dist_mode['MoD-Walk'] + \
                          0.2 * dist_mode['Car-Walk'] + 0.2 * dist_mode['MM-Walk']
    dist_mode['Car'] = dist_mode['car_n']
    dist_mode['MoD'] = dist_mode['MoD_n']
    dist_mode['MM'] = dist_mode['MM_n']
    dist_mode['Bike'] = dist_mode['Bike_n']
    dist_mode['Walk'] = dist_mode['Walk_n']
    dist_mode = dist_mode[['PT', 'Car', 'MoD', 'MM', 'Bike', 'Walk']]
    dist_mode = dist_mode.mul(pers_chars['Distance (km)'], axis=0).round(1)
    dist_mode_list.append(dist_mode)


# Transform the dataframe to long format
for i in range(no_scen):
    dist_mode = dist_mode_list[i]
    dist_mode = dist_mode.stack().reset_index()
    dist_mode.columns = ['persona', 'Mode', 'km']

    # Define the chart
    chart_dist_mode = alt.Chart(dist_mode).mark_bar().encode(
        x=alt.X('Mode:N', sort=["PT","Car","MoD", "MM", "Bike", "Walk"],
            axis=alt.Axis(title=None, labelAngle=0, labelPadding=5, labelFlush=False, tickCount=4,labels=False)),
        y=alt.Y('km:Q', axis=alt.Axis(title='Kilometers')),
        color=alt.Color('Mode:N',
                        scale=alt.Scale(domain=["PT","Car","MoD", "MM", "Bike", "Walk"],
                                        range=['#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e', '#16a085'])),
        column=alt.Column('persona:N', header=alt.Header(labelOrient='bottom', title=None))
    ).properties(
        width=160,
        title={
            'text': 'Modal shift for ' + scen_names[i],
            'fontSize': 16,
            'fontWeight': 'bold',
            'anchor': 'start',
            'offset': 20}
    ).configure_axis(
        grid=False,
        labelFontSize=12,
        titleFontSize=14
    )

    # Render the chart using Streamlit
    st.altair_chart(chart_dist_mode, use_container_width=False)


# Step 7
st.header('Underlying values for impact assessment')

# Define the default values for CO2 emissions and energy demand
co2_default = [50, 120, 40, 10, 15, 0]
energy_default = [1.5, 3.5, 1.2, 0.4, 0.6, 0]

# Create the editable DataFrame for CO2 emissions and energy demand
df = pd.DataFrame({
    'PT': [co2_values[0], energy_values[0]],
    'Car': [co2_values[1], energy_values[1]],
    'MoD': [co2_values[2], energy_values[2]],
    'MM': [co2_values[3], energy_values[3]],
    'Bike': [co2_values[4], energy_values[4]],
    'Walk': [co2_values[5], energy_values[5]]
}, index=['CO2 emissions (g/km/passenger)', 'Energy demand (MJ/km/passenger)'])

# Show the DataFrame for editing USE EDITABLE FORMAT


# Create the input fields
walk_calories_input = st.number_input('Calories burnt per kg per km while walking:', value=50)
bike_calories_input = st.number_input('Calories burnt per kg per km while cycling:', value=30)