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
scen_likelihood_list = []
for i in range(no_scen):
    scen_likelihood = st.slider(f'Likelihood of scenario {scen_names[i]} in percent:', min_value=0, max_value=100,
                                value=default_values[i], step=5)
    scen_likelihood_list.append(scen_likelihood)
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
        y=alt.Y('km:Q', axis=alt.Axis(title='Kilometres')),
        color=alt.Color('Mode:N',
                        scale=alt.Scale(domain=["PT","Car","MoD", "MM", "Bike", "Walk"],
                                        range=['#f39c12', '#16a085', '#f1c40f', '#34495e', '#e74c3c', '#2ecc71'])),
        column=alt.Column('persona:N', header=alt.Header(labelOrient='bottom', title=None))
    ).properties(
        width=160,
        title={
            'text': 'Modal shift in km for ' + scen_names[i],
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

# Create the input fields for individual values
walk_calories_input = st.number_input('Calories burned per kg per km while walking:', value=1)
bike_calories_input = st.number_input('Calories burned per kg per km while cycling:', value=0.4)

# Create editabe dataframe for inputs on emissions and energy demand per passenger kilometer
emissions_energy = {
    'CO2e': [15, 50, 150, 0, 0, 10],
    'MJ': [0.2, 0.8, 1.8, 0, 0, 0.5]
}

# Create the dataframe
emissions_energy = pd.DataFrame(emissions_energy, index=['PT', 'Car', 'MoD', 'MM', 'Bike', 'Walk']).T

# Add a title above the dataframe
st.write('Average CO2 equivalent emissions in g/passenger km and energy demand in MJ/passenger km')
emissions_energy = st.experimental_data_editor(emissions_energy)

# Step 8
st.header('CO2e, energy demand, and calories burned per individual persona')
mods = ['PT','Car','MoD','MM','Bike','Walk']

# Emissions calculation
st.subheader('CO2e emissions')

emis_ind_list = []
for i in range(no_scen):
    emis_ind = dist_mode_list[i].copy()
    for mod in mods:
        emis_ind[mod] = emis_ind[mod] * emissions_energy[mod][0]/1000
    emis_ind[scen_names[i]] = emis_ind.sum(axis=1)
    emis_ind = emis_ind[[scen_names[i]]]
    emis_ind_list.append(emis_ind)
    emis_ind_concat = pd.concat(emis_ind_list, ignore_index=False, join='outer')
    emis_ind_concat = emis_ind_concat.groupby(level=0).sum()
emis_ind_concat = emis_ind_concat.stack().reset_index()
emis_ind_concat.columns = ['Persona', 'Scenario', 'CO2e']

# Define the chart
chart_emis_ind = alt.Chart(emis_ind_concat).mark_bar().encode(
    x=alt.X('Scenario:N', sort=[],
            axis=alt.Axis(title=None, labelAngle=0, labelPadding=5, labelFlush=False, tickCount=4, labels=False)),
    y=alt.Y('CO2e:Q', axis=alt.Axis(title='CO2 equivalent in kg')),
    color=alt.Color('Scenario:N',
                    scale=alt.Scale(domain=scen_names,
                                    range=['#f39c12', '#16a085', '#f1c40f', '#34495e', '#e74c3c', '#2ecc71'])),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=160,
    title={
        'text': 'Daily emissions in CO2e per persona across scenarios',
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
st.altair_chart(chart_emis_ind, use_container_width=False)

# Energy calculation
st.subheader('Energy demand')
ener_ind_list = []
for i in range(no_scen):
    ener_ind = dist_mode_list[i].copy()
    for mod in mods:
        ener_ind[mod] = ener_ind[mod] * emissions_energy[mod][1]
    ener_ind[scen_names[i]] = ener_ind.sum(axis=1)
    ener_ind = ener_ind[[scen_names[i]]]
    ener_ind_list.append(ener_ind)
    ener_ind_concat = pd.concat(ener_ind_list, ignore_index=False, join='outer')
    ener_ind_concat = ener_ind_concat.groupby(level=0).sum()
ener_ind_concat = ener_ind_concat.stack().reset_index()
ener_ind_concat.columns = ['Persona', 'Scenario', 'Energy']

# Define the chart
chart_ener_ind = alt.Chart(ener_ind_concat).mark_bar().encode(
    x=alt.X('Scenario:N', sort=[],
            axis=alt.Axis(title=None, labelAngle=0, labelPadding=5, labelFlush=False, tickCount=4, labels=False)),
    y=alt.Y('Energy:Q', axis=alt.Axis(title='Energy in mega joule')),
    color=alt.Color('Scenario:N',
                    scale=alt.Scale(domain=scen_names,
                                    range=['#f39c12', '#16a085', '#f1c40f', '#34495e', '#e74c3c', '#2ecc71'])),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=160,
    title={
        'text': 'Daily energy demand in MJ per persona across scenarios',
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
st.altair_chart(chart_ener_ind, use_container_width=False)

# Calories calculation
st.subheader('Calories burned')
cal_ind_list = []

for i in range(no_scen):
    dist_mode_list_cal = dist_mode_list[i].copy()
    cal_ind = dist_mode_list_cal
    cal_ind[scen_names[i]] = round((cal_ind['Bike'].multiply(pers_chars['Weight (kg)'], axis=0) *
                                    bike_calories_input) + (cal_ind['Walk'].multiply(pers_chars['Weight (kg)'],
                                                                                     axis=0) * walk_calories_input),0)
    cal_ind = cal_ind[[scen_names[i]]]
    cal_ind_list.append(cal_ind)
    cal_ind_concat = pd.concat(cal_ind_list, ignore_index=False, join='outer')
    cal_ind_concat = cal_ind_concat.groupby(level=0).sum()
cal_ind_concat = cal_ind_concat.stack().reset_index()
cal_ind_concat.columns = ['Persona', 'Scenario', 'Calories']

# Define the chart
chart_cal_ind = alt.Chart(cal_ind_concat).mark_bar().encode(
    x=alt.X('Scenario:N', sort=[],
            axis=alt.Axis(title=None, labelAngle=0, labelPadding=5, labelFlush=False, tickCount=4, labels=False)),
    y=alt.Y('Calories:Q', axis=alt.Axis(title='Calories burned during commute')),
    color=alt.Color('Scenario:N',
                    scale=alt.Scale(domain=scen_names,
                                    range=['#f39c12', '#16a085', '#f1c40f', '#34495e', '#e74c3c', '#2ecc71'])),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=160,
    title={
        'text': 'Daily calories burned per persona across scenarios',
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
st.altair_chart(chart_cal_ind, use_container_width=False)

# Step 9
st.header('Impacts considering population size and persona distribution')
st.subheader('Emissions')
emis_group_list = []

for i in range(no_scen):
    emis_group = emis_ind_list[i].copy()
    # Divided by 100 for percentage of population, by 1000 for emissions in tons instead of kg
    emis_group = round((emis_group.multiply(pers_weights, axis=0)) * no_people / 100000)
    emis_group = emis_group[[scen_names[i]]]
    emis_group_list.append(emis_group)
    emis_group_concat = pd.concat(emis_group_list, ignore_index=False, join='outer')
    emis_group_concat = emis_group_concat.groupby(level=0).sum()
emis_group_concat = emis_group_concat.stack().reset_index()
emis_group_concat.columns = ['Persona', 'Scenario', 'CO2e']

# Define the chart
chart_emis_group = alt.Chart(emis_group_concat).mark_bar().encode(
    x=alt.X('Scenario:N', sort=[],
            axis=alt.Axis(title=None, labelAngle=0, labelPadding=5, labelFlush=False, tickCount=4, labels=False)),
    y=alt.Y('CO2e:Q', axis=alt.Axis(title='CO2e per group and scenario in tons (t)')),
    color=alt.Color('Scenario:N',
                    scale=alt.Scale(domain=scen_names,
                                    range=['#f39c12', '#16a085', '#f1c40f', '#34495e', '#e74c3c', '#2ecc71'])),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=160,
    title={
        'text': 'CO2 equivalent in tons for aggregated persona group',
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
st.altair_chart(chart_emis_group, use_container_width=False)

st.subheader('Energy demand')
ener_group_list = []

for i in range(no_scen):
    ener_group = ener_ind_list[i].copy()
    # Divided by 100 for percentage of population, by 1000 for energy in giga joule
    ener_group = round((ener_group.multiply(pers_weights, axis=0)) * no_people / 100000)
    ener_group = ener_group[[scen_names[i]]]
    ener_group_list.append(ener_group)
    ener_group_concat = pd.concat(ener_group_list, ignore_index=False, join='outer')
    ener_group_concat = ener_group_concat.groupby(level=0).sum()
ener_group_concat = ener_group_concat.stack().reset_index()
ener_group_concat.columns = ['Persona', 'Scenario', 'Energy']

# Define the chart
chart_ener_group = alt.Chart(ener_group_concat).mark_bar().encode(
    x=alt.X('Scenario:N', sort=[],
            axis=alt.Axis(title=None, labelAngle=0, labelPadding=5, labelFlush=False, tickCount=4, labels=False)),
    y=alt.Y('Energy:Q', axis=alt.Axis(title='Energy demand per group and scenario in tons (t)')),
    color=alt.Color('Scenario:N',
                    scale=alt.Scale(domain=scen_names,
                                    range=['#f39c12', '#16a085', '#f1c40f', '#34495e', '#e74c3c', '#2ecc71'])),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=160,
    title={
        'text': 'Energy demand in giga joule (MJ*1000)',
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
st.altair_chart(chart_ener_group, use_container_width=False)

st.subheader('Calories burned')
cal_group_list = []

for i in range(no_scen):
    cal_group = cal_ind_list[i].copy()
    # Divided by 100 for percentage of population and 1000 for pizza
    cal_group = round((cal_group.multiply(pers_weights, axis=0)) * no_people / 100000)
    cal_group = cal_group[[scen_names[i]]]
    cal_group_list.append(cal_group)
    cal_group_concat = pd.concat(cal_group_list, ignore_index=False, join='outer')
    cal_group_concat = cal_group_concat.groupby(level=0).sum()
cal_group_concat = cal_group_concat.stack().reset_index()
cal_group_concat.columns = ['Persona', 'Scenario', 'Calories']

# Define the chart
chart_cal_group = alt.Chart(cal_group_concat).mark_bar().encode(
    x=alt.X('Scenario:N', sort=[],
            axis=alt.Axis(title=None, labelAngle=0, labelPadding=5, labelFlush=False, tickCount=4, labels=False)),
    y=alt.Y('Calories:Q', axis=alt.Axis(title='Calories burned per group and scenario')),
    color=alt.Color('Scenario:N',
                    scale=alt.Scale(domain=scen_names,
                                    range=['#f39c12', '#16a085', '#f1c40f', '#34495e', '#e74c3c', '#2ecc71'])),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=160,
    title={
        'text': 'Pizzas burned per persona group (1 pizza = 1000 cal)',
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
st.altair_chart(chart_cal_group, use_container_width=False)

# Step 10
st.header('Aggregated impacts considering scenario likelihood')
emis_aggr = emis_group_concat.groupby('Scenario').sum().copy()
emis_aggr = round((emis_aggr.multiply(scen_likelihood_list, axis=0)) / 100)
indic_aggr = emis_aggr.sum()

ener_aggr = ener_group_concat.groupby('Scenario').sum().copy()
ener_aggr = round((ener_aggr.multiply(scen_likelihood_list, axis=0)) / 100)
ener_aggr = ener_aggr.sum()
indic_aggr = indic_aggr.append(ener_aggr, ignore_index=False)

cal_aggr = cal_group_concat.groupby('Scenario').sum().copy()
cal_aggr = round((cal_aggr.multiply(scen_likelihood_list, axis=0)) / 100)
cal_aggr = cal_aggr.sum()
indic_aggr = indic_aggr.append(cal_aggr, ignore_index=False)

st.write('Taking the earlier established probability of each scenario in consideration, we have an anticipated daily'
         ' footprint of ' + str(indic_aggr[0]) + ' tons CO2 equivalent. This makes it '+ str(indic_aggr[0] * 365) +
         ' tons per year. Furthermore, we have an energy demand of '  + str(indic_aggr[1]) + ' giga joule per day and ' \
         'about ' + str(indic_aggr[1] * 365) + ' giga joules per year. On the positive side, the commutes help to burn '
         'a total of '+ str(indic_aggr[2]) + ' calories per day or ' + str(indic_aggr[1] * 365) + ' per year.')

# Step 11: Defining Potential Interventions
st.header('Defining a potential intervention')
st.write('For inspiration on possible interventions, have a look at our '
         '<a href="https://urban-mobility-futures.notion.site/3b4cb3e4fccd48a38cda6149a0d6ffa1?v=8ce1115a24e7436f8c31bdd58a3c74ef">Urban Mobility Solution Database.</a>', unsafe_allow_html=True)

default_name = 'On demand shuttles'
default_desc = 'Shared electric on demand shuttles that move on demand between key destinations.'
st.text_input(f'Intervention name:', value=default_name, key='intervention-name')
st.text_area(f'Intervention description (max. 250 characters):', value=default_desc, max_chars=250, key='intervention-description')


# Step 12: Intervention impacts
st.subheader('Impact of the intervention')
st.write('Set the impact you assume you intervention to have across scenario and personas. The values go from -2 to +2.'
         ' -2 means that after the intervention, a certain mode is much less likely. 0 means nothing changes. +2'
         ' means that the likelihood to use a certain mode increases strongly.')

interv_impact_list = []

for i in range(no_scen):
    # Create editabe dataframe for inputs on emissions and energy demand per passenger kilometer
    interv_impact = {
        'MoD': ['-2','+2','+1','0','0','0','0','0'],
        'Car': ['-2','+2','+1','0','0','0','0','0'],
        'Bike': ['-2','+2','+1','0','0','0','0','0'],
        'Walk': ['-2','+2','+1','0','0','0','0','0'],
        'MM': ['0','0','0','0','0','0','0','0'],
        'PT-MoD': ['0','0','0','0','0','0','0','0'],
        'PT-Bike': ['0','0','0','0','0','0','0','0'],
        'PT-Walk': ['0','0','0','0','0','0','0','0'],
        'PT-MM': ['0','0','0','0','0','0','0','0'],
        'MoD-Walk': ['0','0','0','0','0','0','0','0'],
        'MoD-MM': ['0','0','0','0','0','0','0','0'],
        'Car-Walk': ['0','0','0','0','0','0','0','0'],
        'MM-Walk': ['0','0','0','0','0','0','0','0'],
    }
    interv_impact = pd.DataFrame(interv_impact)
    interv_impact = interv_impact[:no_pers]
    interv_impact.set_index(pd.Index(pers_name), inplace=True)
    interv_impact = interv_impact.apply(lambda col: pd.Categorical(col, categories=['-2', '-1', '0', '+1', '+2'], ordered=True))
    st.write('Define the estimated impact for scenario ' + scen_names[i])
    interv_impact = st.experimental_data_editor(interv_impact, key=f'interv_imact{i + 1}')
    interv_impact_list.append(interv_impact)

interv_impact_result_list = []
for i in range(no_scen):
    # Add corresponding values from both dataframes
    df1 = mode_pref_list[i].astype(int)
    df2 = interv_impact_list[i].astype(int)
    result = pd.DataFrame(index=df1.index, columns=df2.columns)
    for p in range(no_pers):
        for j in range(13):
            value = df1.iloc[p, j] + df2.iloc[p, j]
            result.iloc[p, j] = max(min(value, 4), 0)
    interv_impact_result_list.append(result)

# Step 13: Repeating previous steps with new numbers
st.header('Updated impacts taking intervention in consideration')

st.subheader('With intervention: Distribution of travel distances by mode and persona')
# Calculate kilometers per mode for each persona in scenario 1
dist_mode_list_interv = []

for i in range(no_scen):
    dist_mode = interv_impact_result_list[i].copy()
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
    dist_mode_list_interv.append(dist_mode)

# Transform the dataframe to long format
for i in range(no_scen):
    dist_mode = dist_mode_list_interv[i]
    dist_mode = dist_mode.stack().reset_index()
    dist_mode.columns = ['persona', 'Mode', 'km']

    # Define the chart
    chart_dist_mode = alt.Chart(dist_mode).mark_bar().encode(
        x=alt.X('Mode:N', sort=["PT","Car","MoD", "MM", "Bike", "Walk"],
            axis=alt.Axis(title=None, labelAngle=0, labelPadding=5, labelFlush=False, tickCount=4,labels=False)),
        y=alt.Y('km:Q', axis=alt.Axis(title='Kilometres')),
        color=alt.Color('Mode:N',
                        scale=alt.Scale(domain=["PT","Car","MoD", "MM", "Bike", "Walk"],
                                        range=['#d35400', '#2980b9', '#2c3e50', '#c0392b', '#27ae60', '#8e44ad'])),
        column=alt.Column('persona:N', header=alt.Header(labelOrient='bottom', title=None))
    ).properties(
        width=160,
        title={
            'text': 'With intervention: Modal shift in km for ' + scen_names[i],
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

# Step 8
st.header('With intervention: CO2e, energy demand, and calories burned per individual persona')
mods = ['PT','Car','MoD','MM','Bike','Walk']

# Emissions calculation
st.subheader('CO2e emissions')

emis_ind_list = []
for i in range(no_scen):
    emis_ind = dist_mode_list_interv[i].copy()
    for mod in mods:
        emis_ind[mod] = emis_ind[mod] * emissions_energy[mod][0]/1000
    emis_ind[scen_names[i]] = emis_ind.sum(axis=1)
    emis_ind = emis_ind[[scen_names[i]]]
    emis_ind_list.append(emis_ind)
    emis_ind_concat = pd.concat(emis_ind_list, ignore_index=False, join='outer')
    emis_ind_concat = emis_ind_concat.groupby(level=0).sum()
emis_ind_concat = emis_ind_concat.stack().reset_index()
emis_ind_concat.columns = ['Persona', 'Scenario', 'CO2e']

# Define the chart
chart_emis_ind_interv = alt.Chart(emis_ind_concat).mark_bar().encode(
    x=alt.X('Scenario:N', sort=[],
            axis=alt.Axis(title=None, labelAngle=0, labelPadding=5, labelFlush=False, tickCount=4, labels=False)),
    y=alt.Y('CO2e:Q', axis=alt.Axis(title='CO2 equivalent in kg')),
    color=alt.Color('Scenario:N',
                    scale=alt.Scale(domain=scen_names,
                                    range=['#d35400', '#2980b9', '#2c3e50', '#c0392b', '#27ae60', '#8e44ad'])),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=160,
    title={
        'text': 'With intervention: Daily emissions in CO2e per persona across scenarios',
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
st.altair_chart(chart_emis_ind, use_container_width=False)
st.altair_chart(chart_emis_ind_interv, use_container_width=False)

# Energy calculation
st.subheader('Energy demand')
ener_ind_list = []
for i in range(no_scen):
    ener_ind = dist_mode_list_interv[i].copy()
    for mod in mods:
        ener_ind[mod] = ener_ind[mod] * emissions_energy[mod][1]
    ener_ind[scen_names[i]] = ener_ind.sum(axis=1)
    ener_ind = ener_ind[[scen_names[i]]]
    ener_ind_list.append(ener_ind)
    ener_ind_concat = pd.concat(ener_ind_list, ignore_index=False, join='outer')
    ener_ind_concat = ener_ind_concat.groupby(level=0).sum()
ener_ind_concat = ener_ind_concat.stack().reset_index()
ener_ind_concat.columns = ['Persona', 'Scenario', 'Energy']

# Define the chart
chart_ener_ind_interv = alt.Chart(ener_ind_concat).mark_bar().encode(
    x=alt.X('Scenario:N', sort=[],
            axis=alt.Axis(title=None, labelAngle=0, labelPadding=5, labelFlush=False, tickCount=4, labels=False)),
    y=alt.Y('Energy:Q', axis=alt.Axis(title='Energy in mega joule')),
    color=alt.Color('Scenario:N',
                    scale=alt.Scale(domain=scen_names,
                                    range=['#d35400', '#2980b9', '#2c3e50', '#c0392b', '#27ae60', '#8e44ad'])),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=160,
    title={
        'text': 'With intervention: Daily energy demand in MJ per persona across scenarios',
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
st.altair_chart(chart_ener_ind, use_container_width=False)
st.altair_chart(chart_ener_ind_interv, use_container_width=False)

# Calories calculation
st.subheader('Calories burned')
cal_ind_list = []

for i in range(no_scen):
    dist_mode_list_cal = dist_mode_list_interv[i].copy()
    cal_ind = dist_mode_list_cal
    cal_ind[scen_names[i]] = round((cal_ind['Bike'].multiply(pers_chars['Weight (kg)'], axis=0) *
                                    bike_calories_input) + (cal_ind['Walk'].multiply(pers_chars['Weight (kg)'],
                                                                                     axis=0) * walk_calories_input),0)
    cal_ind = cal_ind[[scen_names[i]]]
    cal_ind_list.append(cal_ind)
    cal_ind_concat = pd.concat(cal_ind_list, ignore_index=False, join='outer')
    cal_ind_concat = cal_ind_concat.groupby(level=0).sum()
cal_ind_concat = cal_ind_concat.stack().reset_index()
cal_ind_concat.columns = ['Persona', 'Scenario', 'Calories']

# Define the chart
chart_cal_ind_interv = alt.Chart(cal_ind_concat).mark_bar().encode(
    x=alt.X('Scenario:N', sort=[],
            axis=alt.Axis(title=None, labelAngle=0, labelPadding=5, labelFlush=False, tickCount=4, labels=False)),
    y=alt.Y('Calories:Q', axis=alt.Axis(title='Calories burned during commute')),
    color=alt.Color('Scenario:N',
                    scale=alt.Scale(domain=scen_names,
                                    range=['#d35400', '#2980b9', '#2c3e50', '#c0392b', '#27ae60', '#8e44ad'])),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=160,
    title={
        'text': 'Daily calories burned per persona across scenarios',
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
st.altair_chart(chart_cal_ind, use_container_width=False)
st.altair_chart(chart_cal_ind_interv, use_container_width=False)

# Step 9
st.header('With intervention: Impacts considering population size and persona distribution')
st.subheader('Emissions')
emis_group_list = []

for i in range(no_scen):
    emis_group = emis_ind_list[i].copy()
    # Divided by 100 for percentage of population, by 1000 for emissions in tons instead of kg
    emis_group = round((emis_group.multiply(pers_weights, axis=0)) * no_people / 100000)
    emis_group = emis_group[[scen_names[i]]]
    emis_group_list.append(emis_group)
    emis_group_concat = pd.concat(emis_group_list, ignore_index=False, join='outer')
    emis_group_concat = emis_group_concat.groupby(level=0).sum()
emis_group_concat = emis_group_concat.stack().reset_index()
emis_group_concat.columns = ['Persona', 'Scenario', 'CO2e']

# Define the chart
chart_emis_group_interv = alt.Chart(emis_group_concat).mark_bar().encode(
    x=alt.X('Scenario:N', sort=[],
            axis=alt.Axis(title=None, labelAngle=0, labelPadding=5, labelFlush=False, tickCount=4, labels=False)),
    y=alt.Y('CO2e:Q', axis=alt.Axis(title='CO2e per group and scenario in tons (t)')),
    color=alt.Color('Scenario:N',
                    scale=alt.Scale(domain=scen_names,
                                    range=['#d35400', '#2980b9', '#2c3e50', '#c0392b', '#27ae60', '#8e44ad'])),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=160,
    title={
        'text': 'With intervention: CO2 equivalent in tons for aggregated persona group',
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
st.altair_chart(chart_emis_group, use_container_width=False)
st.altair_chart(chart_emis_group_interv, use_container_width=False)

st.subheader('Energy demand')
ener_group_list = []

for i in range(no_scen):
    ener_group = ener_ind_list[i].copy()
    # Divided by 100 for percentage of population, by 1000 for energy in giga joule
    ener_group = round((ener_group.multiply(pers_weights, axis=0)) * no_people / 100000)
    ener_group = ener_group[[scen_names[i]]]
    ener_group_list.append(ener_group)
    ener_group_concat = pd.concat(ener_group_list, ignore_index=False, join='outer')
    ener_group_concat = ener_group_concat.groupby(level=0).sum()
ener_group_concat = ener_group_concat.stack().reset_index()
ener_group_concat.columns = ['Persona', 'Scenario', 'Energy']

# Define the chart
chart_ener_group_interv = alt.Chart(ener_group_concat).mark_bar().encode(
    x=alt.X('Scenario:N', sort=[],
            axis=alt.Axis(title=None, labelAngle=0, labelPadding=5, labelFlush=False, tickCount=4, labels=False)),
    y=alt.Y('Energy:Q', axis=alt.Axis(title='Energy demand per group and scenario in tons (t)')),
    color=alt.Color('Scenario:N',
                    scale=alt.Scale(domain=scen_names,
                                    range=['#d35400', '#2980b9', '#2c3e50', '#c0392b', '#27ae60', '#8e44ad'])),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=160,
    title={
        'text': 'With intervention: Energy demand in giga joule (MJ*1000)',
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
st.altair_chart(chart_ener_group, use_container_width=False)
st.altair_chart(chart_ener_group_interv, use_container_width=False)

st.subheader('Calories burned')
cal_group_list = []

for i in range(no_scen):
    cal_group = cal_ind_list[i].copy()
    # Divided by 100 for percentage of population and 1000 for pizza
    cal_group = round((cal_group.multiply(pers_weights, axis=0)) * no_people / 100000)
    cal_group = cal_group[[scen_names[i]]]
    cal_group_list.append(cal_group)
    cal_group_concat = pd.concat(cal_group_list, ignore_index=False, join='outer')
    cal_group_concat = cal_group_concat.groupby(level=0).sum()
cal_group_concat = cal_group_concat.stack().reset_index()
cal_group_concat.columns = ['Persona', 'Scenario', 'Calories']

# Define the chart
chart_cal_group_interv = alt.Chart(cal_group_concat).mark_bar().encode(
    x=alt.X('Scenario:N', sort=[],
            axis=alt.Axis(title=None, labelAngle=0, labelPadding=5, labelFlush=False, tickCount=4, labels=False)),
    y=alt.Y('Calories:Q', axis=alt.Axis(title='Calories burned per group and scenario')),
    color=alt.Color('Scenario:N',
                    scale=alt.Scale(domain=scen_names,
                                    range=['#d35400', '#2980b9', '#2c3e50', '#c0392b', '#27ae60', '#8e44ad'])),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=160,
    title={
        'text': 'With intervention: Pizzas burned per persona group (1 pizza = 1000 cal)',
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
st.altair_chart(chart_cal_group, use_container_width=False)
st.altair_chart(chart_cal_group_interv, use_container_width=False)

# Step 10
st.header('With intervention: Aggregated impacts considering scenario likelihood')
emis_aggr = emis_group_concat.groupby('Scenario').sum().copy()
emis_aggr = round((emis_aggr.multiply(scen_likelihood_list, axis=0)) / 100)
indic_aggr_interv = emis_aggr.sum()

ener_aggr = ener_group_concat.groupby('Scenario').sum().copy()
ener_aggr = round((ener_aggr.multiply(scen_likelihood_list, axis=0)) / 100)
ener_aggr = ener_aggr.sum()
indic_aggr_interv = indic_aggr_interv.append(ener_aggr, ignore_index=False)

cal_aggr = cal_group_concat.groupby('Scenario').sum().copy()
cal_aggr = round((cal_aggr.multiply(scen_likelihood_list, axis=0)) / 100)
cal_aggr = cal_aggr.sum()
indic_aggr_interv = indic_aggr_interv.append(cal_aggr, ignore_index=False)

st.write('Taking the earlier established probability of each scenario in consideration, we have an anticipated daily'
         ' footprint of ' + str(indic_aggr[0]) + ' tons CO2 equivalent without intervention and '  + str(indic_aggr_interv[0]) + ' with intervention. '
         'We had previously an energy demand of ' + str(indic_aggr[1]) + ' giga joule per day and '
         'now ' + str(indic_aggr_interv[1]) + '. The commutes helped to burn a total of '+ str(indic_aggr[2]) + ' calories per day previously '
         'and now burn ' + str(indic_aggr_interv[2]) + ' calories per day.')
