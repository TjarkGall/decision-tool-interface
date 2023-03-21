import streamlit as st

# Set the page config
st.set_page_config(
    page_title="Scenario-based policy and intervention evaluation tool",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="auto",
)

# Define the main function
def main():
    st.title('Scenario-based policy and intervention evaluation tool')

    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")

    num_scenarios = st.slider("Choose the number of scenarios", 2, 8, 4)

    scenario_names = []
    for i in range(num_scenarios):
        scenario_name = st.text_input(f"Scenario {i + 1} name", f"Scenario {i + 1}")
        scenario_names.append(scenario_name)

    probabilities = []
    for i, name in enumerate(scenario_names):
        probability = st.slider(f"Probability of {name}", 0.0, 1.0, 0.25)
        probabilities.append(probability)

    st.header("Personas")

    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")

    persona_weights = []
    for i in range(4):
        weight = st.slider(f"Weight of Persona {i + 1}", 0.0, 1.0)
        persona_weights.append(weight)

    st.header("CO2e per mode")

    modes = ["Car", "Public transport", "E-bike/Scooter", "Biking/walking"]
    co2e_per_mode = {}

    for mode in modes:
        co2e = st.number_input(f"{mode} CO2e (kg)", min_value=0.0)
        co2e_per_mode[mode] = co2e

    st.header("Likelihood of each mode per scenario and persona")

    likelihoods = []
    for i, name in enumerate(scenario_names):
        st.subheader(name)
        for j in range(4):
            mode_likelihoods = {}
            for mode in modes:
                likelihood = st.slider(f"Persona {j + 1} {mode} likelihood in {name}", 0.0, 1.0)
                mode_likelihoods[mode] = likelihood
            likelihoods.append(mode_likelihoods)

if __name__ == "__main__":
    main()
