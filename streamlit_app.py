# Load required packages
import altair as alt
import pandas as pd
import streamlit as st
from PIL import Image
from itertools import islice

# Introduction
st.title('Urban Mobility Impact Assessment and Comparison Tool')
st.write('This is a prototype of a tool to compare impacts of potential interventions on a local urban mobility '
         'system. It provides an interface to compare impacts across user groups (personas) and across '
         'future scenarios. Standard values are defined as reference values. This '
         'application compares the impact of an intervention (e.g., policy/technology) for different '
         'persona groups and across 2030 scenarios, measured by CO2 equivalent (CO2e) emissions, energy demand in '
         'megajoules (MJ), and calories burned.')
st.write('As a prototype, some of the input fields are not as intuitive as they should be in a final version. We hope '
         'that it is clear nevertheless and are looking forward to any feedback.')

# Information
st.subheader('Information')
st.write('You can reset the form by refreshing the website. No values or uploaded images are stored. The code is '
         'available on Github: https://github.com/TjarkGall/decision-tool-interface')
st.write('The concept was developed as part of the Institute Pascal research programme 2022 and has been continued as '
         'part of the work of the <a href="http://www.chaire-anthropolis.fr/">Anthropolis Chair.</a>',
         unsafe_allow_html=True)
st.subheader('Questions?')
st.write('Contact Tjark Gall | tjark.gall@irt-systemx.fr')

# Anthropolis logo
image = Image.open('data/images/Anthropolis_logo_colour.png')
st.image(image, use_column_width=True)

# Defining Future Scenarios
st.header('Step 1: Defining future scenarios')

# Number of scenarios
st.subheader('Number of scenarios')
no_scen = st.slider('With how many scenarios do you want to work?', min_value=2, max_value=8, value=4)

# Scenario names and descriptions
st.subheader('Scenario names and descriptions')
st.write('You can keep the standard scenario names and descriptions or change them. If you chose more scenarios, '
         'you should name and describe them.')
scen_names = []
scen_desc = []
for i in range(no_scen):
    default_name = f'S{i + 1}: '
    if i == 0:
        default_name += '2030 | Saclay 2.0'
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
        default_name += '2030 | Paris 2.0'
        default_desc = 'High-density, mixed-use neighbourhood. The second scenario is more optimistic on the ' \
                       'integrated development of the plateau. It assumes that a large number of residential' \
                       ' developments, going further than only student and international researcher housing, ' \
                       'adds a critical mass of population density to allow for a variety of other functions to ' \
                       'arise and remain active even in holiday seasons or weekends.'
    elif i == 2:
        default_name += '2030 | Rural Campus'
        default_desc = 'Low-density, low diversity rural district. This scenario describes mostly the plateau as it ' \
                       'has been since the 1970s. While more offices and universities are added, its functions and ' \
                       'character remains primarily rural. Residential functions, as well as the accompanying ' \
                       'other functions, remain limited and their growth stagnates, maintaining primarily the status ' \
                       'quo of activity and functional mix.'
    elif i == 3:
        default_name += '2030 | Village Campus'
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
st.write('Scenarios help to integrate future uncertainties (= unknown developments). They shall be distinct from each '
         'other. To ensure this, four uncertainties are defined as examples here: Intermodality, Mixed Use, '
         'Density, and Public Transport. For each of the scenarios, they are ranked between low to very high. '
         'While these numbers are not taken into consideration in the calculation, they shall help to distinguish '
         'the scenarios during the following steps.')

uncert_names = []
uncert_desc = []

uncert_names.append(st.text_input('Uncertainty 1 (U1):', value='Intermodality'))
uncert_desc.append(st.text_area('U1 description (max. 250 characters):',
                              value='Ability to use various modes, e.g., metro, bus, and shared bikes.', max_chars=250))

uncert_names.append(st.text_input('Uncertainty 2 (U2):', value='Mixed Use'))
uncert_desc.append(st.text_area('U2 description (max. 250 characters):',
                              value='Mix of functions, e.g., only universities or a mix with shops, bars, housing.', max_chars=250))

uncert_names.append(st.text_input('Uncertainty 3 (U3):', value='Density'))
uncert_desc.append(st.text_area('U3 description (max. 250 characters):',
                              value='Population density, i.e. how many people live and work close to each other.', max_chars=250))

uncert_names.append(st.text_input('Uncertainty 4 (U4):', value='Public Transport'))
uncert_desc.append(st.text_area('U4 description (max. 250 characters):',
                              value='Refers to the service level, e.g., schedule frequency, network density.', max_chars=250))

scen_chars_prep = [{"U1": "3: high", "U2": "1: low", "U3": "4: very high", "U4": "3: high", },
                   {"U1": "4: very high", "U2": "4: very high", "U3": "4: very high", "U4": "4: very high", },
                   {"U1": "2: medium", "U2": "1: low", "U3": "1: low", "U4": "2: medium", },
                   {"U1": "2: medium", "U2": "4: very high", "U3": "2: medium", "U4": "3: high"},
                   {"U1": "2: medium", "U2": "2: medium", "U3": "2: medium", "U4": "2: medium", },
                   {"U1": "2: medium", "U2": "2: medium", "U3": "2: medium", "U4": "2: medium", },
                   {"U1": "2: medium", "U2": "2: medium", "U3": "2: medium", "U4": "2: medium", },
                   {"U1": "2: medium", "U2": "2: medium", "U3": "2: medium", "U4": "2: medium", },]
scen_chars_prep = scen_chars_prep[0:no_scen]

scen_chars = pd.DataFrame(scen_chars_prep, index=scen_names)
scen_chars.U1 = scen_chars.U1.astype("category")
scen_chars.U2 = scen_chars.U2.astype("category")
scen_chars.U3 = scen_chars.U3.astype("category")
scen_chars.U4 = scen_chars.U4.astype("category")

cols = ["U1", "U2", "U3", "U4"]

for col in cols:
    categories = list(scen_chars[col].cat.categories)
    for cat in ["1: low", "2: medium", "3: high", "4: very high"]:
        if cat not in categories:
            scen_chars[col] = scen_chars[col].cat.add_categories(cat)

scen_chars.U1 = scen_chars.U1.cat.set_categories(["1: low", "2: medium", "3: high", "4: very high"])
scen_chars.U2 = scen_chars.U2.cat.set_categories(["1: low", "2: medium", "3: high", "4: very high"])
scen_chars.U3 = scen_chars.U3.cat.set_categories(["1: low", "2: medium", "3: high", "4: very high"])
scen_chars.U4 = scen_chars.U4.cat.set_categories(["1: low", "2: medium", "3: high", "4: very high"])

scen_chars = scen_chars.rename(columns={'U1': uncert_names[0], 'U2': uncert_names[1],
                                        'U3': uncert_names[2], 'U4': uncert_names[3]})
scen_chars = st.experimental_data_editor(scen_chars)

# Scenario images
st.subheader('Scenario images')
st.write('You can upload photos (in format JPG/JPEG/PNG) for each of the scenarios as visual support. The '
         'sample images were created with the scenario description as prompt for Midjourney, a free text-to-image generator.')
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
st.write('Below, the defined scenarios are shown as reference for the next steps. You can also show them in the sidebar '
         'to have them always visible. If you still want to change them, you need to go back to the previous section.')
for i in range(no_scen):
    st.write(f'### {scen_names[i]}')
    if scen_images[i] is not None:
        st.image(scen_images[i], width=300)
    st.write(scen_desc[i])
    st.write(scen_chars.loc[scen_names[i]])

# Defining Future Personas
st.header('Step 2: Defining future personas')
st.write('Next, you can choose with how many personas you want to work, how they are called, and how they are described.'
         ' The descriptions are important as they permit to image their specific needs and preferences. The sample '
         'personas have been developed during a workshop. You can refer to a set of 16 personas developed on the '
         'basis of the 2019 census, as well as their distributions, by clicking here <a href="https://urban-mobility-futures.notion.site/Personas-aa3b30f47c354220bc025dd7edb207cd?pvs=25">here.</a>',
         unsafe_allow_html=True)

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
        st.text_area(f'Description of persona {i + 1} (max. 250 char.):', value=default_desc, max_chars=450))

# Persona characteristics
st.subheader('Persona characteristics')
st.write('Set the number of home-work-home kilometres for a normal day for each persona and their bodyweight in '
         'kilograms. These values are the basis for the later impact assessment of emissions, energy use, and calories burnt.')

# Define default values for all personas
default_values = {pers_name[0]: [60, 57], pers_name[1]: [40, 84], pers_name[2]: [10, 72], pers_name[3]: [4, 53]}
for i in range(4, no_pers):
    default_values[pers_name[i]] = [0, 0]
default_values = dict(islice(default_values.items(), no_pers))

# Create the DataFrame with the default values
pers_chars = pd.DataFrame.from_dict(default_values, orient='index', columns=['Distance (km)', 'Bodyweight (kg)']).fillna(0)

pers_chars = st.experimental_data_editor(pers_chars)

# Persona images
st.subheader('Persona images')
st.write('You can upload photos (in format JPG/JPEG/PNG) for each of the personas as visual support. The '
         'sample images were created with the persona description as prompt for Midjourney, a free text-to-image generator.')

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
st.write('Below, the established personas are shown as reference for the next steps. You can also show them in the sidebar '
         'to have them always visible. If you still want to change them, you need to go back to the previous section.')
for i in range(no_pers):
    st.write(f'### {pers_name[i]}')
    if pers_images[i] is not None:
        st.image(pers_images[i], width=300)
    st.write(pers_desc[i])
    st.write(pers_chars.loc[pers_name[i]])

# Likelihood of scenarios
st.header('Step 3: Set likelihood of scenarios')

# Scenario description
st.write('Define for each of the scenarios the probability in % between 0 and 100. The sum must add up to 100. '
         'A higher percentage means that the scenario will have a higher weight in the impact assessment.')

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
st.header('Step 4: Define population size')
no_people = st.number_input('How many people move to/on the plateau per day in the future?', value=50000, step=1000)

# Persona weights likelihood sliders
st.header('Step 5: Set persona weights')
st.write('Define for each of the personas the weight in percent between 0 and 100. 10 means that 10% of the overall '
         'population defined above are similar to the defined persona. The weights must add up to 100.')
pers_weights = []
for i in range(no_pers):
    default_weights = [20, 20, 15, 45]
    if no_pers > 4:
        default_weights += [0] * (no_pers - 4)
    pers_weights.append(st.slider(f'Weight in percent of {pers_name[i]} in overall population:', min_value=0,
                                  max_value=100, step=5, value=default_weights[i], key=f"pers_weight_{i}"))
total_weights = sum(pers_weights)
st.write(f'Total weight: {total_weights}%')
if total_weights != 100:
    st.error('Total weight must be 100%')

# Mode likelihoods
st.header('Step 6: Set likelihood to use mode per scenario/persona')

# Text description
st.write('In this section, we define for each of the scenarios the likelihood for each persona to use a certain mode. '
         'The range of likelihood to take a mode is 0 = unlikely, 1 = rather unlikely, 2 = rather likely, 3 = likely, '
         'and 4 = very likely. The modes are Mobility on Demand (MoD), Car, Bike, Walk, Micromobility (MM), Public '
         'Transport and MoD (PT-MoD), Public Transport and Bike (PT-Bike), Public Transport and Walk (PT-Walk), '
         'Public Transport and Micromobility (PT-MM), Car-Walk and Micromobility and Walk (MM-Walk). For multimodal '
         'trips, we assume 80% to be done with the first-mentioned mode and 20% by the second.')
st.write('This is the most time-consuming but also the most important step. You see the scenario image for reference. '
         'Use the sidebar to retrieve the descriptions and to show the personas.')

# Default values for persona likelihoods to use certain types of transport
mode_prep_s1 = [
    # Jacqueline
    {'MoD': "2: Rather likely", 'Car': "3: Likely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely", 'MM': "0: Unlikely", 'PT-MoD': "3: Likely", 'PT-Bike': "1: Rather unlikely", 'PT-Walk': "3: Likely",
     'PT-MM': "1: Rather unlikely", 'MoD-Walk': "1: Rather unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "3: Likely", 'MM-Walk': "0: Unlikely"},
    # Thierry
    {'MoD': "3: Likely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "3: Likely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "2: Rather likely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "3: Likely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "1: Rather unlikely", 'MM-Walk': "0: Unlikely"},
    # Adrian
    {'MoD': "3: Likely", 'Car': "3: Likely", 'Bike': "1: Rather unlikely", 'Walk': "1: Rather unlikely",
     'MM': "2: Rather likely", 'PT-MoD': "2: Rather likely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "1: Rather unlikely", 'MoD-Walk': "3: Likely", 'MoD-MM': "3: Likely", 'Car-Walk': "4: Very likely", 'MM-Walk': "0: Unlikely"},
    # Rui
    {'MoD': "3: Likely", 'Car': "0: Unlikely", 'Bike': "4: Very likely", 'Walk': "4: Very likely",
     'MM': "3: Likely", 'PT-MoD': "1: Rather unlikely", 'PT-Bike': "4: Very likely", 'PT-Walk': "4: Very likely",
     'PT-MM': "4: Very likely", 'MoD-Walk': "1: Rather unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "4: Very likely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"}
]
mode_prep_s2 = [
    # Jacqueline
    {'MoD': "0: Unlikely", 'Car': "2: Rather likely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "4: Very likely", 'PT-Bike': "2: Rather likely", 'PT-Walk': "4: Very likely",
     'PT-MM': "2: Rather likely", 'MoD-Walk': "1: Rather unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "1: Rather unlikely", 'MM-Walk': "0: Unlikely"},
    # Thierry
    {'MoD': "2: Rather likely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "4: Very likely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "3: Likely",
     'PT-MM': "1: Rather unlikely", 'MoD-Walk': "3: Likely", 'MoD-MM': "1: Rather unlikely", 'Car-Walk': "1: Rather unlikely", 'MM-Walk': "0: Unlikely"},
    # Adrian
    {'MoD': "4: Very likely", 'Car': "3: Likely", 'Bike': "1: Rather unlikely", 'Walk': "1: Rather unlikely",
     'MM': "2: Rather likely", 'PT-MoD': "2: Rather likely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "1: Rather unlikely", 'MoD-Walk': "3: Likely", 'MoD-MM': "4: Very likely", 'Car-Walk': "4: Very likely", 'MM-Walk': "0: Unlikely"},
    # Rui
    {'MoD': "3: Likely", 'Car': "0: Unlikely", 'Bike': "4: Very likely", 'Walk': "4: Very likely",
     'MM': "3: Likely", 'PT-MoD': "1: Rather unlikely", 'PT-Bike': "4: Very likely", 'PT-Walk': "4: Very likely",
     'PT-MM': "4: Very likely", 'MoD-Walk': "1: Rather unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "4: Very likely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"}
]
mode_prep_s3 = [
    # Jacqueline
    {'MoD': "3: Likely", 'Car': "4: Very likely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "1: Rather unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "2: Rather likely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "4: Very likely", 'MM-Walk': "0: Unlikely"},
    # Thierry
    {'MoD': "1: Rather unlikely", 'Car': "1: Rather unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "2: Rather likely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "1: Rather unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "2: Rather likely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "2: Rather likely", 'MM-Walk': "0: Unlikely"},
    # Adrian
    {'MoD': "3: Likely", 'Car': "4: Very likely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "1: Rather unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "2: Rather likely", 'MoD-MM': "2: Rather likely", 'Car-Walk': "4: Very likely", 'MM-Walk': "0: Unlikely"},
    # Rui
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "4: Very likely", 'Walk': "3: Likely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "2: Rather likely", 'PT-Walk': "3: Likely",
     'PT-MM': "1: Rather unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "1: Rather unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"}
]
mode_prep_s4 = [
    # Jacqueline
    {'MoD': "1: Rather unlikely", 'Car': "3: Likely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "3: Likely", 'PT-Bike': "1: Rather unlikely", 'PT-Walk': "3: Likely",
     'PT-MM': "3: Likely", 'MoD-Walk': "1: Rather unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "4: Very likely", 'MM-Walk': "0: Unlikely"},
    # Thierry
    {'MoD': "1: Rather unlikely", 'Car': "1: Rather unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "2: Rather likely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "2: Rather likely",
     'PT-MM': "1: Rather unlikely", 'MoD-Walk': "3: Likely", 'MoD-MM': "1: Rather unlikely", 'Car-Walk': "2: Rather likely", 'MM-Walk': "0: Unlikely"},
    # Adrian
    {'MoD': "4: Very likely", 'Car': "4: Very likely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "1: Rather unlikely", 'PT-MoD': "1: Rather unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "3: Likely", 'MoD-MM': "2: Rather likely", 'Car-Walk': "4: Very likely", 'MM-Walk': "0: Unlikely"},
    # Rui
    {'MoD': "3: Likely", 'Car': "2: Rather likely", 'Bike': "4: Very likely", 'Walk': "3: Likely",
     'MM': "2: Rather likely", 'PT-MoD': "2: Rather likely", 'PT-Bike': "3: Likely", 'PT-Walk': "3: Likely",
     'PT-MM': "2: Rather likely", 'MoD-Walk': "2: Rather likely", 'MoD-MM': "1: Rather unlikely", 'Car-Walk': "1: Rather unlikely", 'MM-Walk': "3: Likely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"}
]
mode_prep_s5 = [
    # Persona n
    {'MoD': "1: Rather unlikely", 'Car': "1: Rather unlikely", 'Bike': "1: Rather unlikely", 'Walk': "1: Rather unlikely",
     'MM': "1: Rather unlikely", 'PT-MoD': "1: Rather unlikely", 'PT-Bike': "1: Rather unlikely", 'PT-Walk': "1: Rather unlikely",
     'PT-MM': "1: Rather unlikely", 'MoD-Walk': "1: Rather unlikely", 'MoD-MM': "1: Rather unlikely", 'Car-Walk': "1: Rather unlikely", 'MM-Walk': "1: Rather unlikely"},
    # Persona n
    {'MoD': "1: Rather unlikely", 'Car': "1: Rather unlikely", 'Bike': "1: Rather unlikely", 'Walk': "1: Rather unlikely",
     'MM': "1: Rather unlikely", 'PT-MoD': "1: Rather unlikely", 'PT-Bike': "1: Rather unlikely", 'PT-Walk': "1: Rather unlikely",
     'PT-MM': "1: Rather unlikely", 'MoD-Walk': "1: Rather unlikely", 'MoD-MM': "1: Rather unlikely", 'Car-Walk': "1: Rather unlikely", 'MM-Walk': "1: Rather unlikely"},
    # Persona n
    {'MoD': "1: Rather unlikely", 'Car': "1: Rather unlikely", 'Bike': "1: Rather unlikely", 'Walk': "1: Rather unlikely",
     'MM': "1: Rather unlikely", 'PT-MoD': "1: Rather unlikely", 'PT-Bike': "1: Rather unlikely", 'PT-Walk': "1: Rather unlikely",
     'PT-MM': "1: Rather unlikely", 'MoD-Walk': "1: Rather unlikely", 'MoD-MM': "1: Rather unlikely", 'Car-Walk': "1: Rather unlikely", 'MM-Walk': "1: Rather unlikely"},
    # Persona n
    {'MoD': "1: Rather unlikely", 'Car': "1: Rather unlikely", 'Bike': "1: Rather unlikely", 'Walk': "1: Rather unlikely",
     'MM': "1: Rather unlikely", 'PT-MoD': "1: Rather unlikely", 'PT-Bike': "1: Rather unlikely", 'PT-Walk': "1: Rather unlikely",
     'PT-MM': "1: Rather unlikely", 'MoD-Walk': "1: Rather unlikely", 'MoD-MM': "1: Rather unlikely", 'Car-Walk': "1: Rather unlikely", 'MM-Walk': "1: Rather unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"},
    # Persona n
    {'MoD': "0: Unlikely", 'Car': "0: Unlikely", 'Bike': "0: Unlikely", 'Walk': "0: Unlikely",
     'MM': "0: Unlikely", 'PT-MoD': "0: Unlikely", 'PT-Bike': "0: Unlikely", 'PT-Walk': "0: Unlikely",
     'PT-MM': "0: Unlikely", 'MoD-Walk': "0: Unlikely", 'MoD-MM': "0: Unlikely", 'Car-Walk': "0: Unlikely", 'MM-Walk': "0: Unlikely"}
]
mode_prep_s6 = mode_prep_s5.copy()
mode_prep_s7 = mode_prep_s5.copy()
mode_prep_s8 = mode_prep_s5.copy()

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
        missing_categories = [cat for cat in ["0: Unlikely", "1: Rather unlikely", "2: Rather likely", "3: Likely", "4: Very likely"] if cat not in categories]
        mode_pref[mode] = mode_pref[mode].cat.add_categories(missing_categories)
        mode_pref[mode] = mode_pref[mode].cat.set_categories(["0: Unlikely", "1: Rather unlikely", "2: Rather likely", "3: Likely", "4: Very likely"])
        mode_pref[mode] = mode_pref[mode].cat.reorder_categories(sorted(mode_pref[mode].cat.categories))
    st.write(f'### {scen_names[i]}')
    if scen_images[i] is not None:
        st.image(scen_images[i], width=300)
    st.write(
        f'How likely is it that each persona uses each mode in the scenario {scen_names[i]}?')
    mode_pref = st.experimental_data_editor(mode_pref, key=f'mode_pref{i + 1}')
    mode_pref_list.append(mode_pref)

# Set values for impact assessment
st.header('Step 7: Set values for impact assessment')

# Create the input fields for individual values
walk_calories_input = st.number_input('Adapt the value for calories burned per kg per km while walking. The standard is '
                                      'that one calorie is burned per kilometre per kg bodyweight.', value=1)
bike_calories_input = st.number_input('Adapt the value for calories burned per kg per km while cycling. The standard is '
                                      'that 0.4 calories are burned per kilometre per kg bodyweight.', value=0.4)

# Create editabe dataframe for inputs on emissions and energy demand per passenger kilometer
emissions_energy = {
    'CO2e': [15, 50, 150, 10, 0, 0],
    'MJ': [0.2, 0.8, 1.8, 0.5, 0, 0]
}

# Create the dataframe
emissions_energy = pd.DataFrame(emissions_energy, index=['PT', 'Car', 'MoD', 'MM', 'Bike', 'Walk']).T

# Add a title above the dataframe
st.write('Adapt the assumed future CO2 equivalent emissions in g/passenger km and energy demand in MJ/passenger km. You can '
         'find reference values for emissions from [ADEME](https://impactco2.fr/transport) and for '
         'energy from [IEA](https://www.iea.org/data-and-statistics/charts/energy-intensity-of-passenger-transport-modes-2018).')
emissions_energy = st.experimental_data_editor(emissions_energy)


# Mode likelihoods
st.header('Step 8a: Impacts per persona group')
st.write('In this section, you see the distances by mode for each scenario and individual persona.')
st.subheader('Distribution of travel distances by mode and persona')
# Calculate kilometers per mode for each persona in scenario 1
dist_mode_list = []

for i in range(no_scen):
    dist_mode = mode_pref_list[i]
    dist_mode = dist_mode.apply(lambda x: x.str[0])
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

# Colours
colours_ind = ['#193f5a', '#db666e', '#eca83e', '#62548e', '#e18054', '#c65a86', '#344c79', '#975792']

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
                                        range=colours_ind)),
        column=alt.Column('persona:N', header=alt.Header(labelOrient='bottom', title=None))
    ).properties(
        width=140,
        title={
            'text': 'Modal share in km for ' + scen_names[i],
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


st.header('CO2e, energy demand, and calories burned per individual persona')
st.write('In this section, you can see the impacts by scenario for each individual persona.')
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
                                    range=colours_ind)),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=140,
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
                                    range=colours_ind)),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=140,
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
    cal_ind[scen_names[i]] = round((cal_ind['Bike'].multiply(pers_chars['Bodyweight (kg)'], axis=0) *
                                    bike_calories_input) + (cal_ind['Walk'].multiply(pers_chars['Bodyweight (kg)'],
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
                                    range=colours_ind)),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=140,
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

# Impacts considering population size and persona distribution
st.header('Step 8b: Impacts considering population size and persona distribution')
st.write('In this section, you can see the impacts by scenario for each persona. Compared to above, the values are '
         f'multiplied by the set population size of {no_people} and the set weight for each persona.')
st.subheader('Emissions')
emis_group_list = []

for i in range(no_scen):
    emis_group = emis_ind_list[i].copy()
    emis_group = emis_group[0:no_pers]
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
                                    range=colours_ind)),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=140,
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
    ener_group = ener_group[0:no_pers]
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
                                    range=colours_ind)),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=140,
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
    cal_group = cal_group[0:no_pers]
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
                                    range=colours_ind)),
    column=alt.Column('Persona:N', header=alt.Header(labelOrient='bottom', title=None))
).properties(
    width=140,
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

# Aggregated impacts considering scenario likelihood
st.header('Step 8c: Analysis of results')

emis_aggr = emis_group_concat.groupby('Scenario').sum().copy()
emis_aggr = round((emis_aggr.multiply(scen_likelihood_list, axis=0)) / 100)

indic_aggr = {}
indic_aggr = emis_aggr.sum()

ener_aggr = ener_group_concat.groupby('Scenario').sum().copy()
ener_aggr = round((ener_aggr.multiply(scen_likelihood_list, axis=0)) / 100)
ener_aggr = ener_aggr.sum()
indic_aggr = indic_aggr.append(ener_aggr, ignore_index=False)

cal_aggr = cal_group_concat.groupby('Scenario').sum().copy()
cal_aggr = round((cal_aggr.multiply(scen_likelihood_list, axis=0)) / 100)
cal_aggr = cal_aggr.sum()
indic_aggr = indic_aggr.append(cal_aggr, ignore_index=False)

# individual scenario values
emis_scen_max_name = emis_aggr.sort_values('CO2e', ascending=False).reset_index()['Scenario'].iloc[0]
emis_scen_max_val = emis_aggr.sort_values('CO2e', ascending=False).reset_index()['CO2e'].iloc[0]

emis_scen_min_name = emis_aggr.sort_values('CO2e', ascending=True).reset_index()['Scenario'].iloc[0]
emis_scen_min_val = emis_aggr.sort_values('CO2e', ascending=True).reset_index()['CO2e'].iloc[0]

# Individual for personas
emis_pers_ind_max_name_group = emis_ind_concat.groupby('Persona').mean().sort_values('CO2e', ascending=False).reset_index()['Persona'].iloc[0]
emis_pers_ind_max_val_group = emis_ind_concat.groupby('Persona').mean().sort_values('CO2e', ascending=False).reset_index()['CO2e'].iloc[0].round(1)

emis_pers_ind_min_name_group = emis_ind_concat.groupby('Persona').mean().sort_values('CO2e').reset_index()['Persona'].iloc[0]
emis_pers_ind_min_val_group = emis_ind_concat.groupby('Persona').mean().sort_values('CO2e').reset_index()['CO2e'].iloc[0].round(1)

max_emitter_ind_name = emis_ind_concat.sort_values('CO2e', ascending=False).reset_index()['Persona'].iloc[0]
max_emitter_ind_scen = emis_ind_concat.sort_values('CO2e', ascending=False).reset_index()['Scenario'].iloc[0]
max_emitter_ind_max_value = emis_ind_concat.sort_values('CO2e', ascending=False).reset_index()['CO2e'].iloc[0].round(1)
max_emitter_ind_min_value = emis_ind_concat[emis_ind_concat['Persona'] == max_emitter_ind_name].sort_values('CO2e')['CO2e'].iloc[0].round(1)
max_emitter_ind_scen_min = emis_ind_concat[emis_ind_concat['Persona'] == max_emitter_ind_name].sort_values('CO2e')['Scenario'].iloc[0]

min_emitter_ind_name = emis_ind_concat.sort_values('CO2e').reset_index()['Persona'].iloc[0]
min_emitter_ind_max_value = emis_ind_concat[emis_ind_concat['Persona'] == min_emitter_ind_name].sort_values('CO2e', ascending=False)['CO2e'].iloc[0].round(2)
min_emitter_ind_min_value = emis_ind_concat[emis_ind_concat['Persona'] == min_emitter_ind_name].sort_values('CO2e')['CO2e'].iloc[0].round(2)

# Aggregated by personas
emis_pers_aggr_max_name_group = emis_group_concat.groupby('Persona').mean().sort_values('CO2e', ascending=False).reset_index()['Persona'].iloc[0]
emis_pers_aggr_max_val_group = emis_group_concat.groupby('Persona').mean().sort_values('CO2e', ascending=False).reset_index()['CO2e'].iloc[0].round(1)

emis_pers_aggr_min_name_group = emis_group_concat.groupby('Persona').mean().sort_values('CO2e').reset_index()['Persona'].iloc[0]
emis_pers_aggr_min_val_group = emis_group_concat.groupby('Persona').mean().sort_values('CO2e').reset_index()['CO2e'].iloc[0].round(1)

max_emitter_aggr_name = emis_group_concat.sort_values('CO2e', ascending=False).reset_index()['Persona'].iloc[0]
max_emitter_aggr_scen = emis_group_concat.sort_values('CO2e', ascending=False).reset_index()['Scenario'].iloc[0]
max_emitter_aggr_max_value = emis_group_concat.sort_values('CO2e', ascending=False).reset_index()['CO2e'].iloc[0].round(1)
max_emitter_aggr_min_value = emis_group_concat[emis_group_concat['Persona'] == max_emitter_aggr_name].sort_values('CO2e')['CO2e'].iloc[0].round(1)
max_emitter_aggr_scen_min = emis_group_concat[emis_group_concat['Persona'] == max_emitter_aggr_name].sort_values('CO2e')['Scenario'].iloc[0]

min_emitter_aggr_name = emis_group_concat.sort_values('CO2e').reset_index()['Persona'].iloc[0]
min_emitter_aggr_max_value = emis_group_concat[emis_group_concat['Persona'] == min_emitter_aggr_name].sort_values('CO2e', ascending=False)['CO2e'].iloc[0].round(2)
min_emitter_aggr_min_value = emis_group_concat[emis_group_concat['Persona'] == min_emitter_aggr_name].sort_values('CO2e')['CO2e'].iloc[0].round(2)

st.write('Building on the earlier established likelihood of each scenario, we can anticipate a daily '
         f'footprint of __{round(indic_aggr[0])} tons CO2 equivalent__. This makes it about __{round(indic_aggr[0] * 0.365)} '
         f'kilotons__ per year. Further, we assume an energy demand of __{round(indic_aggr[1])} gigajoules per day__ and '
         f'about __{round(indic_aggr[1] * 0.365)} terajoules per year__. On the positive side, the commutes help to burn '
         f'a total of __{round(indic_aggr[2])} pizzas (=1000 calories) per day__ or __{round(indic_aggr[1] * 365)} pizzas__ per year.')

st.write('More interesting insights can be generated when we look at the differences between the scenarios. '
         f'The highest emitting scenario is __{emis_scen_max_name}__ with __{int(emis_scen_max_val)} tons CO2e per day__. '
         f'This is __{int(emis_scen_max_val-emis_scen_min_val)} tons CO2e__ more than the most sustainable scenario '
         f'__{emis_scen_min_name}__ which only emits __{int(emis_scen_min_val)} tons CO2e per day__.')

st.write(f'The highest emitter (average across scenarios) is __{emis_pers_ind_max_name_group}__ with '
         f'__{emis_pers_ind_max_val_group} kg CO2e per day__ compared to __{emis_pers_ind_min_name_group}__ who only '
         f'emits __{emis_pers_ind_min_val_group} kg CO2e per day__. When zooming in on the scenarios, the differences '
         f'become even stronger. For example, __{max_emitter_ind_name}__ has the highest overall emissions for the '
         f'scenario __{max_emitter_ind_scen}__ with __{max_emitter_ind_max_value} kg CO2e__, '
         f'__{(max_emitter_ind_max_value/max_emitter_ind_min_value).round(1)} times__ more than the same persona for scenario '
         f'__{max_emitter_ind_scen_min}__. On the other extreme, __{min_emitter_ind_name}__ emits only between '
         f' __{min_emitter_ind_min_value} and {min_emitter_ind_max_value} kg CO2e per day__.')

st.write(f'Finally, we can look at the emissions taking into consideration the population size and persona occurrence. '
         f'The highest emitter in this case (average across scenarios) is all __{emis_pers_aggr_max_name_group}s__ with '
         f'__{emis_pers_aggr_max_val_group} tons CO2e per day__ compared to all __{emis_pers_aggr_min_name_group}s__ who only '
         f'emit __{emis_pers_aggr_min_val_group} tons CO2e per day__. When zooming in on the scenarios, the differences '
         f'become even stronger. For example, all__{max_emitter_aggr_name}s__ have the highest overall emissions for the '
         f'scenario __{max_emitter_aggr_scen}__ with __{max_emitter_aggr_max_value} tons CO2e__, '
         f'__{(max_emitter_aggr_max_value/max_emitter_aggr_min_value).round(1)} times__ more than the same persona for scenario '
         f'__{max_emitter_aggr_scen_min}__. On the other extreme, all __{min_emitter_aggr_name}s__ emit only between '
         f' __{min_emitter_aggr_min_value} and {min_emitter_aggr_max_value} tons CO2e per day__.')

# Defining potential interventions
st.header('Step 9a: Defining potential interventions')
st.write('You can use this tool to compare the impact of two interventions. For inspiration, have a look at our '
         '<a href="https://urban-mobility-futures.notion.site/3b4cb3e4fccd48a38cda6149a0d6ffa1?v=8ce1115a24e7436f8c31bdd58a3c74ef">Urban Mobility Solution Database.</a>', unsafe_allow_html=True)

interv_name_1 = 'On demand shuttles'
interv_acr_1 = 'MoD'
interv_desc_1 = 'Shared electric on demand shuttles that move on demand between key destinations.'
st.text_input(f'Intervention 1:', value=interv_name_1, key='intervention-name-1')
st.text_input(f'Intervention 1 acronym:', value=interv_acr_1, max_chars=5, key='intervention-acronym-1')
st.text_area(f'Intervention 1 description (max. 250 characters):', value=interv_desc_1, max_chars=250, key='intervention-description-1')

interv_name_2 = 'E-Bike sharing service'
interv_acr_2 = 'eBike'
interv_desc_2 = 'Affordable e-bikes for rent connecting the plateau, stations, the villages in the valley, and Massy-Palaiseau.'
st.text_input(f'Intervention 2:', value=interv_name_2, key='intervention-name-2')
st.text_input(f'Intervention 2 acronym:', value=interv_acr_2, max_chars=5, key='intervention-acronym-2')
st.text_area(f'Intervention 2 description (max. 250 characters):', value=interv_desc_2, max_chars=250, key='intervention-description-2')


# Estimating impact of interventions
st.header('Step 9b: Estimating impact of interventions')
st.write('Set the assumed impact the two interventions might have across scenarios and personas. The values go from -2 to +2.'
         ' -2 means that after the intervention, a certain mode is much less likely. 0 means nothing changes. +2'
         ' means that the likelihood to use a certain mode increases strongly. The acronyms stand for: MoD: Mobility '
         'on Demand, MM: Micromobility, PT: Public Transport.')

# Input collection for intervention 1 and 2
interv_1_impact = {
        0:{
        'MoD': ['+1: Slight increase','+2: Strong increase','+1: Slight increase','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['-1: Slight decrease','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','+2: Strong increase','+1: Slight increase','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['+1: Slight increase','+1: Slight increase','+1: Slight increase','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        1:{
        'MoD': ['+1: Slight increase','+1: Slight increase','+1: Slight increase','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','+1: Slight increase','+1: Slight increase','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['+2: Strong increase','+2: Strong increase','+2: Strong increase','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        2:{
        'MoD': ['+1: Slight increase','+2: Strong increase','+1: Slight increase','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['-1: Slight decrease','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','+1: Slight increase','0: No change','+1: Slight increase','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['0: No change','0: No change','+1: Slight increase','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        3:{
        'MoD': ['+1: Slight increase','+1: Slight increase','+1: Slight increase','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['+1: Slight increase','+2: Strong increase','+1: Slight increase','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['+2: Strong increase','+1: Slight increase','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        4:{
        'MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        5:{
        'MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        6:{
        'MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        7:{
        'MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        }

interv_2_impact = {
        0:{
        'MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['+2: Strong increase','0: No change','+1: Slight increase','+1: Slight increase','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['+2: Strong increase','0: No change','+1: Slight increase','+1: Slight increase','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['-1: Slight decrease','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        1:{
        'MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['+1: Slight increase','0: No change','+1: Slight increase','+1: Slight increase','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['+1: Slight increase','0: No change','0: No change','+1: Slight increase','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['0: No change','0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        2:{
        'MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['+2: Strong increase','0: No change','+1: Slight increase','+2: Strong increase','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['+2: Strong increase','0: No change','+1: Slight increase','+1: Slight increase','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['-1: Slight decrease','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        3:{
        'MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['-1: Slight decrease','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['+1: Slight increase','0: No change','+1: Slight increase','+1: Slight increase','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['+2: Strong increase','0: No change','0: No change','+1: Slight increase','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['0: No change','0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','-1: Slight decrease','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        4:{
        'MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        5:{
        'MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        6:{
        'MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        7:{
        'MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MoD': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Bike': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'PT-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MoD-MM': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'Car-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        'MM-Walk': ['0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change','0: No change'],
        },
        }

# Set df to be used below
interv_1_impact_list = []
interv_1_impact_result_list = []
interv_2_impact_list = []
interv_2_impact_result_list = []

#### START WORKING AREA

# st.write('Two methods are available to evaluate the impact of interventions across scenarios and personas. The checkbox '
#          'below allows you to switch on the simplified mode.')
# # Create the button
button_state = False
# button_state = st.checkbox('Simplified method')
#

if button_state == False:
    st.subheader(f'Impact of intervention 1: {interv_name_1}')
    for i in range(no_scen):
        # Create editabe dataframe for inputs on emissions and energy demand per passenger kilometer
        interv_1_impact_temp = interv_1_impact[i]
        interv_1_impact_temp = pd.DataFrame(interv_1_impact_temp)
        interv_1_impact_temp = interv_1_impact_temp[:no_pers]
        interv_1_impact_temp.set_index(pd.Index(pers_name), inplace=True)
        interv_1_impact_temp = interv_1_impact_temp.apply(lambda col: pd.Categorical(col, categories=['-2: Strong decrease', '-1: Slight decrease', '0: No change', '+1: Slight increase', '+2: Strong increase'], ordered=True))
        st.write('Define the estimated impact for scenario ' + scen_names[i])
        interv_1_impact_temp = st.experimental_data_editor(interv_1_impact_temp, key=f'interv_1_impact{i + 1}')
        interv_1_impact_list.append(interv_1_impact_temp)

    # Editable df for intervention 1
    for i in range(no_scen):
        # Add corresponding values from both dataframes
        df1 = mode_pref_list[i]
        df1 = df1.apply(lambda x: x.str[0])
        df1 = df1.astype(int)
        df2 = interv_1_impact_list[i]
        df2 = df2.apply(lambda x: x.str.split(':', 1).str[0])
        df2 = df2.astype(int)
        result = pd.DataFrame(index=df1.index, columns=df2.columns)
        for p in range(no_pers):
            for j in range(13):
                value = df1.iloc[p, j] + df2.iloc[p, j]
                result.iloc[p, j] = max(min(value, 4), 0)
        interv_1_impact_result_list.append(result)

    st.subheader(f'Impact of intervention 2: {interv_name_2}')

    # Editable df for intervention 2
    for i in range(no_scen):
        # Create editabe dataframe for inputs on emissions and energy demand per passenger kilometer
        interv_2_impact_temp = interv_2_impact[i]
        interv_2_impact_temp = pd.DataFrame(interv_2_impact_temp)
        interv_2_impact_temp = interv_2_impact_temp[:no_pers]
        interv_2_impact_temp.set_index(pd.Index(pers_name), inplace=True)
        interv_2_impact_temp = interv_2_impact_temp.apply(lambda col: pd.Categorical(col, categories=['-2: Strong decrease', '-1: Slight decrease', '0: No change', '+1: Slight increase', '+2: Strong increase'], ordered=True))
        st.write('Define the estimated impact for scenario ' + scen_names[i])
        interv_2_impact_temp = st.experimental_data_editor(interv_2_impact_temp, key=f'interv_2_impact{i + 1}')
        interv_2_impact_list.append(interv_2_impact_temp)

    for i in range(no_scen):
        # Add corresponding values from both dataframes
        df1 = mode_pref_list[i]
        df1 = df1.apply(lambda x: x.str[0])
        df1 = df1.astype(int)
        df2 = interv_2_impact_list[i]
        df2 = df2.apply(lambda x: x.str.split(':', 1).str[0])
        df2 = df2.astype(int)
        result = pd.DataFrame(index=df1.index, columns=df2.columns)
        for p in range(no_pers):
            for j in range(13):
                value = df1.iloc[p, j] + df2.iloc[p, j]
                result.iloc[p, j] = max(min(value, 4), 0)
        interv_2_impact_result_list.append(result)

else:
    st.write("<span style='color:red'>Not finalised yet. Please change back to the extended one.</span>", unsafe_allow_html=True)
    st.subheader(f'Impact of intervention 1: {interv_name_1}')
    # Create an empty DataFrame to store the results
    results_dict = {}
    for i in range(no_scen):
        st.subheader(scen_names[i])
        for p in range(no_pers):
            st.write(f"__Estimate the impact of {interv_name_1} on {pers_name[p]}__")
            # Create a slider with range -2 to 2 and default value 0
            slider_value = st.slider(f"Choose between more individual car use and micromobility on the left (-2) and "
                                     f"more active modes and public transport on the right (+2)",
                                     -2, 2, 0, key=f"{i}-{p}")

            # Store the result in the dictionary
            results_dict[f"({i}, {p})"] = slider_value

    # Display the results
    st.write(results_dict)
    st.write(mode_pref_list)
    st.write(interv_1_impact_result_list)

##### END WORKING AREA


# Preparation for charts
scen_acr = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']
scen_acr_temp = scen_acr[:no_scen]
scen_acr_interv = [f'{s}a' for s in scen_acr_temp] + [f'{s}b: {interv_acr_1}' for s in scen_acr_temp] + [f'{s}c: {interv_acr_2}' for s in scen_acr_temp]
scen_acr_interv.sort()

# Colours + color scale for chart
colours_int = ['#193f5a', '#45667b', '#8b9eab',
               '#db666e', '#e1858b', '#ebb2b7',
               '#eca83e', '#f1b964', '#f6d49e',
               '#62548e', '#8177a5', '#afa9c5',
               '#e18054', '#e79a76', '#f0bfa9',
               '#c65a86', '#d37ba0', '#e2acc2',
               '#344c79', '#596f95', '#97a5bb',
               '#975792', '#ac79a8', '#cbaac8']
color_scale = alt.Scale(domain=scen_acr_interv, range=colours_int)

# New modal shares
# Intervention 1
# Calculate kilometers per mode for each persona in scenario 1
dist_mode_list_interv_1 = []
for i in range(no_scen):
    dist_mode = interv_1_impact_result_list[i].copy()
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
    dist_mode_list_interv_1.append(dist_mode)
# Transform the dataframe to long format
for i in range(no_scen):
    dist_mode_interv_1 = dist_mode_list_interv_1[i]
    dist_mode_interv_1 = dist_mode_interv_1.stack().reset_index()
    dist_mode_interv_1.columns = ['persona', 'Mode', 'km']

# Intervention 2
dist_mode_list_interv_2 = []
for i in range(no_scen):
    dist_mode = interv_2_impact_result_list[i].copy()
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
    dist_mode_list_interv_2.append(dist_mode)

# Transform the dataframe to long format
for i in range(no_scen):
    dist_mode_interv_2 = dist_mode_list_interv_2[i]
    dist_mode_interv_2 = dist_mode_interv_2.stack().reset_index()
    dist_mode_interv_2.columns = ['persona', 'Mode', 'km']

# New emissions
# Intervention 1
emis_ind_list_interv_1 = []
for i in range(no_scen):
    emis_ind = dist_mode_list_interv_1[i].copy()
    for mod in mods:
        emis_ind[mod] = emis_ind[mod] * emissions_energy[mod][0]/1000
    emis_ind[scen_names[i]] = emis_ind.sum(axis=1)
    emis_ind = emis_ind[[scen_names[i]]]
    emis_ind_list_interv_1.append(emis_ind)
    emis_ind_concat_interv_1 = pd.concat(emis_ind_list_interv_1, ignore_index=False, join='outer')
    emis_ind_concat_interv_1 = emis_ind_concat_interv_1.groupby(level=0).sum()
emis_ind_concat_interv_1 = emis_ind_concat_interv_1.stack().reset_index()
emis_ind_concat_interv_1.columns = ['Persona', 'Scenario', 'CO2e']

# Intervention 2
emis_ind_list_interv_2 = []
for i in range(no_scen):
    emis_ind = dist_mode_list_interv_2[i].copy()
    for mod in mods:
        emis_ind[mod] = emis_ind[mod] * emissions_energy[mod][0]/1000
    emis_ind[scen_names[i]] = emis_ind.sum(axis=1)
    emis_ind = emis_ind[[scen_names[i]]]
    emis_ind_list_interv_2.append(emis_ind)
    emis_ind_concat_interv_2 = pd.concat(emis_ind_list_interv_2, ignore_index=False, join='outer')
    emis_ind_concat_interv_2 = emis_ind_concat_interv_2.groupby(level=0).sum()
emis_ind_concat_interv_2 = emis_ind_concat_interv_2.stack().reset_index()
emis_ind_concat_interv_2.columns = ['Persona', 'Scenario', 'CO2e']

# Dataframe preparation combining base and intervention scenarios
emis_ind_concat['Scenario'] = emis_ind_concat['Scenario'].str[:2] + 'a'
emis_ind_concat_interv_1['Scenario'] = emis_ind_concat_interv_1['Scenario'].str[:2] + f'b: {interv_acr_1}'
emis_ind_concat_interv_2['Scenario'] = emis_ind_concat_interv_2['Scenario'].str[:2] + f'c: {interv_acr_2}'

emis_ind_interv = pd.concat([emis_ind_concat, emis_ind_concat_interv_1, emis_ind_concat_interv_2])
emis_ind_interv = emis_ind_interv.sort_values(by=['Persona','Scenario'])

# New energy calculation
# Intervention 1
ener_ind_list_interv_1 = []
for i in range(no_scen):
    ener_ind = dist_mode_list_interv_1[i].copy()
    for mod in mods:
        ener_ind[mod] = ener_ind[mod] * emissions_energy[mod][1]
    ener_ind[scen_names[i]] = ener_ind.sum(axis=1)
    ener_ind = ener_ind[[scen_names[i]]]
    ener_ind_list_interv_1.append(ener_ind)
    ener_ind_concat_interv_1 = pd.concat(ener_ind_list_interv_1, ignore_index=False, join='outer')
    ener_ind_concat_interv_1 = ener_ind_concat_interv_1.groupby(level=0).sum()
ener_ind_concat_interv_1 = ener_ind_concat_interv_1.stack().reset_index()
ener_ind_concat_interv_1.columns = ['Persona', 'Scenario', 'Energy']
# Intervention 2
ener_ind_list_interv_2 = []
for i in range(no_scen):
    ener_ind = dist_mode_list_interv_2[i].copy()
    for mod in mods:
        ener_ind[mod] = ener_ind[mod] * emissions_energy[mod][1]
    ener_ind[scen_names[i]] = ener_ind.sum(axis=1)
    ener_ind = ener_ind[[scen_names[i]]]
    ener_ind_list_interv_2.append(ener_ind)
    ener_ind_concat_interv_2 = pd.concat(ener_ind_list_interv_2, ignore_index=False, join='outer')
    ener_ind_concat_interv_2 = ener_ind_concat_interv_2.groupby(level=0).sum()
ener_ind_concat_interv_2 = ener_ind_concat_interv_2.stack().reset_index()
ener_ind_concat_interv_2.columns = ['Persona', 'Scenario', 'Energy']

# Dataframe preparation combining base and intervention scenarios
ener_ind_concat['Scenario'] = ener_ind_concat['Scenario'].str[:2] + 'a'
ener_ind_concat_interv_1['Scenario'] = ener_ind_concat_interv_1['Scenario'].str[:2] + f'b: {interv_acr_1}'
ener_ind_concat_interv_2['Scenario'] = ener_ind_concat_interv_2['Scenario'].str[:2] + f'c: {interv_acr_2}'

ener_ind_interv = pd.concat([ener_ind_concat, ener_ind_concat_interv_1, ener_ind_concat_interv_2])
ener_ind_interv = ener_ind_interv.sort_values(by=['Persona','Scenario'])

# New calories calculation
# Intervention 1
cal_ind_list_interv_1 = []
for i in range(no_scen):
    dist_mode_list_cal = dist_mode_list_interv_1[i].copy()
    cal_ind = dist_mode_list_cal
    cal_ind[scen_names[i]] = round((cal_ind['Bike'].multiply(pers_chars['Bodyweight (kg)'], axis=0) *
                                    bike_calories_input) + (cal_ind['Walk'].multiply(pers_chars['Bodyweight (kg)'],
                                                                                     axis=0) * walk_calories_input),0)
    cal_ind = cal_ind[[scen_names[i]]]
    cal_ind_list_interv_1.append(cal_ind)
    cal_ind_concat_interv_1 = pd.concat(cal_ind_list_interv_1, ignore_index=False, join='outer')
    cal_ind_concat_interv_1 = cal_ind_concat_interv_1.groupby(level=0).sum()
cal_ind_concat_interv_1 = cal_ind_concat_interv_1.stack().reset_index()
cal_ind_concat_interv_1.columns = ['Persona', 'Scenario', 'Calories']
# Intervention 2
cal_ind_list_interv_2 = []
for i in range(no_scen):
    dist_mode_list_cal = dist_mode_list_interv_2[i].copy()
    cal_ind = dist_mode_list_cal
    cal_ind[scen_names[i]] = round((cal_ind['Bike'].multiply(pers_chars['Bodyweight (kg)'], axis=0) *
                                    bike_calories_input) + (cal_ind['Walk'].multiply(pers_chars['Bodyweight (kg)'],
                                                                                     axis=0) * walk_calories_input),0)
    cal_ind = cal_ind[[scen_names[i]]]
    cal_ind_list_interv_2.append(cal_ind)
    cal_ind_concat_interv_2 = pd.concat(cal_ind_list_interv_2, ignore_index=False, join='outer')
    cal_ind_concat_interv_2 = cal_ind_concat_interv_2.groupby(level=0).sum()
cal_ind_concat_interv_2 = cal_ind_concat_interv_2.stack().reset_index()
cal_ind_concat_interv_2.columns = ['Persona', 'Scenario', 'Calories']

# Dataframe preparation combining base and intervention scenarios
cal_ind_concat['Scenario'] = cal_ind_concat['Scenario'].str[:2] + 'a'
cal_ind_concat_interv_1['Scenario'] = cal_ind_concat_interv_1['Scenario'].str[:2] + f'b: {interv_acr_1}'
cal_ind_concat_interv_2['Scenario'] = cal_ind_concat_interv_2['Scenario'].str[:2] + f'c: {interv_acr_2}'

cal_ind_interv = pd.concat([cal_ind_concat, cal_ind_concat_interv_1, cal_ind_concat_interv_2])
cal_ind_interv = cal_ind_interv.sort_values(by=['Persona','Scenario'])

# New emissions with pop size
# Intervention 1
emis_group_list_interv_1 = []
for i in range(no_scen):
    emis_group = emis_ind_list_interv_1[i].copy()
    emis_group = emis_group[0:no_pers]
    # Divided by 100 for percentage of population, by 1000 for emissions in tons instead of kg
    emis_group = (emis_group.multiply(pers_weights, axis=0)) * no_people / 100000
    emis_group = emis_group[[scen_names[i]]]
    emis_group_list_interv_1.append(emis_group)
    emis_group_concat_interv_1 = pd.concat(emis_group_list_interv_1, ignore_index=False, join='outer')
    emis_group_concat_interv_1 = emis_group_concat_interv_1.groupby(level=0).sum()
emis_group_concat_interv_1 = emis_group_concat_interv_1.stack().reset_index()
emis_group_concat_interv_1.columns = ['Persona', 'Scenario', 'CO2e']

# Intervention 2
emis_group_list_interv_2 = []
for i in range(no_scen):
    emis_group = emis_ind_list_interv_2[i].copy()
    emis_group = emis_group[0:no_pers]
    # Divided by 100 for percentage of population, by 1000 for emissions in tons instead of kg
    emis_group = (emis_group.multiply(pers_weights, axis=0)) * no_people / 100000
    emis_group = emis_group[[scen_names[i]]]
    emis_group_list_interv_2.append(emis_group)
    emis_group_concat_interv_2 = pd.concat(emis_group_list_interv_2, ignore_index=False, join='outer')
    emis_group_concat_interv_2 = emis_group_concat_interv_2.groupby(level=0).sum()
emis_group_concat_interv_2 = emis_group_concat_interv_2.stack().reset_index()
emis_group_concat_interv_2.columns = ['Persona', 'Scenario', 'CO2e']

# Dataframe preparation combining base and intervention scenarios
emis_group_concat['Scenario'] = emis_group_concat['Scenario'].str[:2] + 'a'
emis_group_concat_interv_1['Scenario'] = emis_group_concat_interv_1['Scenario'].str[:2] + f'b: {interv_acr_1}'
emis_group_concat_interv_2['Scenario'] = emis_group_concat_interv_2['Scenario'].str[:2] + f'c: {interv_acr_2}'

emis_group_interv = pd.concat([emis_group_concat, emis_group_concat_interv_1, emis_group_concat_interv_2])
emis_group_interv = emis_group_interv.sort_values(by=['Persona','Scenario'])

# New energy with pop size
# Intervention 1
ener_group_list_interv_1 = []
for i in range(no_scen):
    ener_group = ener_ind_list_interv_1[i].copy()
    ener_group = ener_group[0:no_pers]
    # Divided by 100 for percentage of population, by 1000 for energy in giga joule
    ener_group = round((ener_group.multiply(pers_weights, axis=0)) * no_people / 100000)
    ener_group = ener_group[[scen_names[i]]]
    ener_group_list_interv_1.append(ener_group)
    ener_group_concat_interv_1 = pd.concat(ener_group_list_interv_1, ignore_index=False, join='outer')
    ener_group_concat_interv_1 = ener_group_concat_interv_1.groupby(level=0).sum()
ener_group_concat_interv_1 = ener_group_concat_interv_1.stack().reset_index()
ener_group_concat_interv_1.columns = ['Persona', 'Scenario', 'Energy']
# Intervention 2
ener_group_list_interv_2 = []
for i in range(no_scen):
    ener_group = ener_ind_list_interv_2[i].copy()
    ener_group = ener_group[0:no_pers]
    # Divided by 100 for percentage of population, by 1000 for energy in giga joule
    ener_group = round((ener_group.multiply(pers_weights, axis=0)) * no_people / 100000)
    ener_group = ener_group[[scen_names[i]]]
    ener_group_list_interv_2.append(ener_group)
    ener_group_concat_interv_2 = pd.concat(ener_group_list_interv_2, ignore_index=False, join='outer')
    ener_group_concat_interv_2 = ener_group_concat_interv_2.groupby(level=0).sum()
ener_group_concat_interv_2 = ener_group_concat_interv_2.stack().reset_index()
ener_group_concat_interv_2.columns = ['Persona', 'Scenario', 'Energy']

# Dataframe preparation combining base and intervention scenarios
ener_group_concat['Scenario'] = ener_group_concat['Scenario'].str[:2] + 'a'
ener_group_concat_interv_1['Scenario'] = ener_group_concat_interv_1['Scenario'].str[:2] + f'b: {interv_acr_1}'
ener_group_concat_interv_2['Scenario'] = ener_group_concat_interv_2['Scenario'].str[:2] + f'c: {interv_acr_2}'

ener_group_interv = pd.concat([ener_group_concat, ener_group_concat_interv_1, ener_group_concat_interv_2])
ener_group_interv = ener_group_interv.sort_values(by=['Persona','Scenario'])

# New calories with pop size
# Intervention 1
cal_group_list_interv_1 = []
for i in range(no_scen):
    cal_group = cal_ind_list_interv_1[i].copy()
    cal_group = cal_group[0:no_pers]
    # Divided by 100 for percentage of population and 1000 for pizza
    cal_group = round((cal_group.multiply(pers_weights, axis=0)) * no_people / 100000)
    cal_group = cal_group[[scen_names[i]]]
    cal_group_list_interv_1.append(cal_group)
    cal_group_concat_interv_1 = pd.concat(cal_group_list_interv_1, ignore_index=False, join='outer')
    cal_group_concat_interv_1 = cal_group_concat_interv_1.groupby(level=0).sum()
cal_group_concat_interv_1 = cal_group_concat_interv_1.stack().reset_index()
cal_group_concat_interv_1.columns = ['Persona', 'Scenario', 'Calories']
# Intervention 2
cal_group_list_interv_2 = []
for i in range(no_scen):
    cal_group = cal_ind_list_interv_2[i].copy()
    cal_group = cal_group[0:no_pers]
    # Divided by 100 for percentage of population and 1000 for pizza
    cal_group = round((cal_group.multiply(pers_weights, axis=0)) * no_people / 100000)
    cal_group = cal_group[[scen_names[i]]]
    cal_ind_list_interv_2.append(cal_group)
    cal_group_concat_interv_2 = pd.concat(cal_ind_list_interv_2, ignore_index=False, join='outer')
    cal_group_concat_interv_2 = cal_group_concat_interv_2.groupby(level=0).sum()
cal_group_concat_interv_2 = cal_group_concat_interv_2.stack().reset_index()
cal_group_concat_interv_2.columns = ['Persona', 'Scenario', 'Calories']

# Dataframe preparation combining base and intervention scenarios
cal_group_concat['Scenario'] = cal_group_concat['Scenario'].str[:2] + 'a'
cal_group_concat_interv_1['Scenario'] = cal_group_concat_interv_1['Scenario'].str[:2] + f'b: {interv_acr_1}'
cal_group_concat_interv_2['Scenario'] = cal_group_concat_interv_2['Scenario'].str[:2] + f'c: {interv_acr_2}'

cal_group_interv = pd.concat([cal_group_concat, cal_group_concat_interv_1, cal_group_concat_interv_2])
cal_group_interv = cal_group_interv.sort_values(by=['Persona','Scenario'])

# Graphs
st.header('Step 10a: Impacts per persona group with interventions')
st.write('The following charts show for each persona and scenario the emissions, energy demand, and calories burned.'
         f'Each time, the base scenario is compared to the interventions {interv_name_1} and {interv_name_2}.')
st.subheader('CO2e emissions')
# Chart for emissions comparison
chart_emis_ind_interv = alt.Chart(emis_ind_interv).mark_bar().encode(
    x=alt.X('Scenario', title='Scenario'),
    y=alt.Y('CO2e', title='CO2e in kg per day'),
    color=alt.Color('Scenario', scale=color_scale),
    column='Persona'
).properties(width=600 / no_pers)
chart_emis_ind_interv

st.subheader('Energy demand')
# Chart for energy comparison
chart_ener_ind_interv = alt.Chart(ener_ind_interv).mark_bar().encode(
    x=alt.X('Scenario', title='Scenario'),
    y=alt.Y('Energy', title='Energy demand in MJ per day'),
    color=alt.Color('Scenario', scale=color_scale),
    column='Persona'
).properties(width=600 / no_pers)
chart_ener_ind_interv

st.subheader('Calories burned')
# Chart for energy comparison
chart_cal_ind_interv = alt.Chart(cal_ind_interv).mark_bar().encode(
    x=alt.X('Scenario', title='Scenario'),
    y=alt.Y('Calories', title='Calories burned per day'),
    color=alt.Color('Scenario', scale=color_scale),
    column='Persona'
).properties(width=600 / no_pers)
chart_cal_ind_interv

st.header('Step 10b: Impacts considering population size and persona distribution with interventions')
st.write('The following charts show for each scenario the emissions, energy demand, and calories burned. '
         'Compared to the previous charts, the numbers are scaled by the population size and the persona weights. '
         f'Each time, the base scenario is compared to the interventions {interv_name_1} and {interv_name_2}.')
st.subheader('Emissions')
# Chart for aggregated emissions comparison
chart_emis_group_interv = alt.Chart(emis_group_interv).mark_bar().encode(
    x=alt.X('Scenario', title='Scenario'),
    y=alt.Y('CO2e', title='CO2e per group and scenario in tons (t)'),
    color=alt.Color('Scenario', scale=color_scale),
    column='Persona'
).properties(width=600 / no_pers)
chart_emis_group_interv

st.subheader('Energy demand')
# Chart for aggregated energy comparison
chart_ener_group_interv = alt.Chart(ener_group_interv).mark_bar().encode(
    x=alt.X('Scenario', title='Scenario'),
    y=alt.Y('Energy', title='Energy demand per group and scenario in Gigajoule (MJ*1000)'),
    color=alt.Color('Scenario', scale=color_scale),
    column='Persona'
).properties(width=600 / no_pers)
chart_ener_group_interv

st.subheader('Calories burned')
# Chart for aggregated calories comparison
chart_cal_group_interv = alt.Chart(cal_group_interv).mark_bar().encode(
    x=alt.X('Scenario', title='Scenario'),
    y=alt.Y('Calories', title='Pizzas burned per persona group (1 pizza = 1000 cal)'),
    color=alt.Color('Scenario', scale=color_scale),
    column='Persona'
).properties(width=600 / no_pers)
chart_cal_group_interv

# Last step, written summary
st.header('Step 10c: Analysis of results with interventions')
# Emissions aggregation
emis_aggr = emis_group_concat.groupby('Scenario').sum().copy()
emis_aggr = ((emis_aggr.multiply(scen_likelihood_list, axis=0)) / 100).sum()
# Intervention 1
emis_aggr_interv_1 = emis_group_concat_interv_1.groupby('Scenario').sum().copy()
emis_aggr_interv_1 = ((emis_aggr_interv_1.multiply(scen_likelihood_list, axis=0)) / 100).sum()
emis_aggr = emis_aggr.append(emis_aggr_interv_1)
# Intervention 2
emis_aggr_interv_2 = emis_group_concat_interv_2.groupby('Scenario').sum().copy()
emis_aggr_interv_2 = ((emis_aggr_interv_2.multiply(scen_likelihood_list, axis=0)) / 100).sum()
emis_aggr = emis_aggr.append(emis_aggr_interv_2)

# Energy aggregation
ener_aggr = ener_group_concat.groupby('Scenario').sum().copy()
ener_aggr = ((ener_aggr.multiply(scen_likelihood_list, axis=0)) / 100).sum()
# Intervention 1
ener_aggr_interv_1 = ener_group_concat_interv_1.groupby('Scenario').sum().copy()
ener_aggr_interv_1 = ((ener_aggr_interv_1.multiply(scen_likelihood_list, axis=0)) / 100).sum()
ener_aggr = ener_aggr.append(ener_aggr_interv_1)
# Intervention 2
ener_aggr_interv_2 = ener_group_concat_interv_2.groupby('Scenario').sum().copy()
ener_aggr_interv_2 = ((ener_aggr_interv_2.multiply(scen_likelihood_list, axis=0)) / 100).sum()
ener_aggr = ener_aggr.append(ener_aggr_interv_2)

# Calories aggregation
cal_aggr = cal_group_concat.groupby('Scenario').sum().copy()
cal_aggr = ((cal_aggr.multiply(scen_likelihood_list, axis=0)) / 100).sum()
# Intervention 1
cal_aggr_interv_1 = cal_group_concat_interv_1.groupby('Scenario').sum().copy()
cal_aggr_interv_1 = ((cal_aggr_interv_1.multiply(scen_likelihood_list, axis=0)) / 100).sum()
cal_aggr = cal_aggr.append(cal_aggr_interv_1)
# Intervention 2
cal_aggr_interv_2 = cal_group_concat_interv_2.groupby('Scenario').sum().copy()
cal_aggr_interv_2 = ((cal_aggr_interv_2.multiply(scen_likelihood_list, axis=0)) / 100).sum()
cal_aggr = cal_aggr.append(cal_aggr_interv_2)

st.write('Considering the likelihood of each scenario, we have an anticipated daily'
         f' footprint of __{round((emis_aggr[0]))} tons CO2e__ without intervention, '
         f'__{round(emis_aggr[1])} tons CO2e__ with the intervention __"{interv_name_1}"__ and '
         f'__{round(emis_aggr[2])} tons CO2e__ with the intervention __"{interv_name_2}"__. '
         f'Without any intervention, we have a daily energy demand of __{round(ener_aggr[0])}__ giga joule per day. '
         f'With the intervention __"{interv_name_1}"__, the enery demand changes to __{round(ener_aggr[1])}__ giga joule per day '
         f'and with __"{interv_name_2}"__ to __{round(ener_aggr[2])}__ giga joule per day. '
         f'Currently, __{round(cal_aggr[0])}__ pizzas (1000 calories) are burned. After the intervention __"{interv_name_1}"__, __{round(cal_aggr[1])}__ '
         f'are burned while __"{interv_name_2}"__ changes it to __{round(cal_aggr[2])}__.'
         )

st.write('Similar as before, we can zoom in on the detailed differences and impacts. This allows us to say, for example, '
         f'which intervention has the highest impact for which scenario and by how much it can reduce the emissions. '
         f'Lastly, we can use the graphs to analyse which personas are affected how to see if the interventions '
         f'serve those which are targeted.')

# Sidebar
# Set the title and description
st.sidebar.title("Info Sidebar")
st.sidebar.write("You can use this sidebar to show key info during the process. Everything is also included in the "
                 "main text on the right. The width of the sidebar can changed by dragging its border.")

# Create the dropdown menu with options
selected_option = st.sidebar.selectbox("I want to see the:", ("Process & Glossary",
                                                             "Scenario overview",
                                                             "Persona overview"))
st.sidebar.markdown("---")

# Display the corresponding code based on the selected option
if selected_option == "Process & Glossary":
   with st.sidebar:
       st.sidebar.markdown('''
       # Process steps
       - [Step 1: Defining future scenarios](#step-1-defining-future-scenarios)
       - [Step 2: Defining future personas](#step-2-defining-future-personas)
       - [Step 3: Set likelihood of scenarios](#step-3-set-likelihood-of-scenarios)
       - [Step 4: Define population size](#step-4-define-population-size)
       - [Step 5: Set persona weights](#step-5-set-persona-weights)
       - [Step 6: Set likelihood to use mode per scenario/persona](#step-6-set-likelihood-to-use-mode-per-scenario-persona)
       - [Step 7: Set values for impact assessment](#step-7-set-values-for-impact-assessment)
       - [Step 8a: Impacts per persona group](#step-8a-impacts-per-persona-group)
       - [Step 8b: Impacts considering population size and persona distribution](#step-8b-impacts-considering-population-size-and-persona-distribution)
       - [Step 8c: Analysis of results](#step-8c-analysis-of-results)
       - [Step 9a: Defining potential interventions](#step-9a-defining-potential-interventions)
       - [Step 9b: Estimating impact of interventions](#step-9b-estimating-impact-of-interventions)
       - [Step 10a: Impacts per persona group with interventions](#step-10a-impacts-per-persona-group-with-interventions)
       - [Step 10b: Impacts considering population size and persona distribution with interventions](#step-10b-impacts-considering-population-size-and-persona-distribution-with-interventions)
       - [Step 10c: Analysis of results with interventions](#step-10c-analysis-of-results-with-interventions)
       ''', unsafe_allow_html=True)
       st.header("Glossary")
       st.write("Scenarios are distinct alternative futures that help considering uncertain future developments.")
       st.write("Personas are archetypical representations of a population to reduce reality's complexity while maintaining variety.")

elif selected_option == "Scenario overview":
    with st.sidebar:
        for i in range(no_scen):
            st.write(f'### {scen_names[i]}')
            if scen_images[i] is not None:
                st.image(scen_images[i], width=300)
            st.write(scen_desc[i])
            st.write(scen_chars.loc[scen_names[i]])

elif selected_option == "Persona overview":
    with st.sidebar:
        for i in range(no_pers):
            st.write(f'### {pers_name[i]}')
            if pers_images[i] is not None:
                st.image(pers_images[i], width=300)
            st.write(pers_desc[i])
            st.write(pers_chars.loc[pers_name[i]])