
import streamlit as st
import pandas as pd
import plotly.express as px
import qrcode
from PIL import Image
from datetime import date

import os


def load_database():

    return pd.read_csv("weld_database.csv")


def save_database(df):

    df.to_csv(
        "weld_database.csv",
        index=False
    )

st.set_page_config(
    page_title="SmartRail WeldGuard",
    layout="wide"
)


# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("🚆 SmartRail WeldGuard")

menu = st.sidebar.radio(
    "",
    [
        "🏠 Dashboard",
        "🔧 Weld Registration",
        "📋 Inspection Checklist",
        "⚠️ Defect Reporting",
        "🤖 Risk Prediction",
        "📁 Weld Database",
        "📈 QA/QC Analytics",
        "🚨 Maintenance Alerts",
        "🔧 Maintenance Action"
    ]
)

# ==========================
# DASHBOARD
# ==========================

st.write("Dashboard loaded")

if menu == "🏠 Dashboard":

    st.title("🚆 SmartRail WeldGuard Dashboard")

    st.subheader("Dashboard Information")

    try:

        data = load_database()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Welds",
            len(data)
        )

        col2.metric(
            "UT Pass",
            len(data[data["UT Result"]=="PASS"])
        )

        col3.metric(
            "Approved",
            len(data[data["Inspection Status"]=="Approved"])
        )

        col4.metric(
            "Rework Required",
            len(data[data["Inspection Status"]=="Rework Required"])
        )

    except:

        st.warning("No weld records found.")

        data = pd.DataFrame()

    st.divider()

    st.subheader("Information Recorded")

    search = st.text_input(
        "🔍 Search Weld ID"
    )

    col1, col2 = st.columns(2)

    method_filter = col1.selectbox(
        "Filter Welding Method",
        [
            "All",
            "Flash Butt Welding",
            "Alumino Thermit Welding"
        ]
    )

    status_filter = col2.selectbox(
        "Filter Inspection Status",
        [
            "All",
            "Approved",
            "Pending Inspection",
            "Rework Required",
            "Maintenance Completed"
        ]
    )

    filtered_data = data.copy()

    if search:

        filtered_data = filtered_data[
            filtered_data["Weld ID"]
            .astype(str)
            .str.contains(search, case=False)
        ]

    if method_filter != "All":

        filtered_data = filtered_data[
            filtered_data["Welding Method"]
            == method_filter
        ]

    if status_filter != "All":

        filtered_data = filtered_data[
            filtered_data["Inspection Status"]
            == status_filter
        ]

    st.dataframe(
        filtered_data,
        use_container_width=True
    )

    st.divider()

    st.subheader("🔍 View Weld Details")

    if len(filtered_data) > 0:

        selected_weld = st.selectbox(
            "Select Weld ID",
            filtered_data["Weld ID"]
        )

        weld_info = filtered_data[
            filtered_data["Weld ID"] == selected_weld
        ].iloc[0]

        st.write("### Weld Information")

        st.write(
            f"**Weld ID:** {weld_info['Weld ID']}"
        )

        st.write(
            f"**GPS Location:** {weld_info['GPS Location']}"
        )

        st.write(
            f"**Date of Installation:** {weld_info['Date of Installation']}"
        )

        st.write(
            f"**Welder Name:** {weld_info['Welder Name']}"
        )

        st.write(
            f"**Welding Method:** {weld_info['Welding Method']}"
        )

        st.write(
            f"**UT Result:** {weld_info['UT Result']}"
        )

        st.write(
            f"**Inspection Status:** {weld_info['Inspection Status']}"
        )

        st.write(
            f"**Maintenance History:** {weld_info['Maintenance History']}"
        )

    st.divider()

    st.subheader("📱 Weld QR Code")

    qr_file = f"{selected_weld}.png"

    import os

    if os.path.exists(qr_file):

        st.image(
            qr_file,
            width=250
        )

        with open(qr_file, "rb") as file:

            st.download_button(
                label="⬇ Download QR Code",
                data=file,
                file_name=qr_file,
                mime="image/png"
            )

    else:

        st.warning(
            "QR Code not found for this weld."
        )

# ==========================
# REGISTER WELD
# ==========================

elif menu == "🔧 Weld Registration":

    st.title("🔧 Register New Weld")

    import pandas as pd
    import qrcode
    from datetime import date

    # Load Database

    try:
        df = load_database()
    except:
        df = pd.DataFrame(columns=[
            "Weld ID",
            "GPS Location",
            "Date of Installation",
            "Welder Name",
            "Welding Method",
            "UT Result",
            "Inspection Status",
            "Maintenance History"
        ])

    # Auto Generate Weld ID

    weld_number = len(df) + 1

    weld_id = f"WLD-CN-{weld_number:04d}"

    st.text_input(
        "Weld ID",
        value=weld_id,
        disabled=True
    )

    location = st.text_input(
        "GPS / Track Location"
    )

    rail_type = st.selectbox(
        "Rail Type",
        [
            "UIC54",
            "UIC60"
        ]
    )

    method = st.selectbox(
        "Welding Method",
        [
            "Flash Butt Welding",
            "Alumino Thermit Welding"
        ]
    )

    welder = st.text_input(
        "Welder Name"
    )

    install_date = st.date_input(
        "Installation Date",
        date.today()
    )

    if st.button("Register Weld"):

        new_record = pd.DataFrame({

            "Weld ID":[weld_id],

            "GPS Location":[location],

            "Date of Installation":[install_date],

            "Welder Name":[welder],

            "Welding Method":[method],

            "UT Result":["PENDING"],

            "Inspection Status":["Pending Inspection"],

            "Maintenance History":["None"]

        })

        df = pd.concat(
            [df,new_record],
            ignore_index=True
        )

        save_database(df)

        st.success(
            f"{weld_id} Registered Successfully"
        )

        # Generate QR

        qr = qrcode.make(weld_id)

        qr_file = f"{weld_id}.png"

        qr.save(qr_file)

        st.image(
            qr_file,
            caption="Generated QR Code"
        )

        with open(qr_file, "rb") as file:

            st.download_button(
                label="⬇ Download QR Code",
                data=file,
                file_name=qr_file,
                mime="image/png"
       )

# ==========================
# INSPECTION
# ==========================

elif menu == "📋 Inspection Checklist":

    st.title("📋 Inspection Checklist")

    import pandas as pd
    from datetime import date

    # Load Database

    df = load_database()

    # Select Weld

    weld_id = st.selectbox(
        "Select Weld ID",
        df["Weld ID"]
    )

    inspector = st.text_input(
        "Inspector Name"
    )

    inspection_date = st.date_input(
        "Inspection Date",
        date.today()
    )

    st.subheader("Pre-Welding")

    rail_type = st.checkbox("Rail Type Verified")
    alignment = st.checkbox("Rail Alignment Checked")
    rail_gap = st.checkbox("Rail Gap Measured")
    surface = st.checkbox("Rail Surface Cleaned")

    st.subheader("During Welding")

    temperature = st.checkbox("Temperature Verified")
    material = st.checkbox("Material Valid")
    procedure = st.checkbox("Procedure Followed")

    st.subheader("Post-Welding")

    visual = st.checkbox("Visual Inspection")
    grinding = st.checkbox("Grinding Completed")
    ut = st.checkbox("UT Completed")

    result = st.selectbox(
        "Inspection Result",
        [
            "PASS",
            "FAIL"
        ]
    )

    remarks = st.text_area(
        "Remarks"
    )

    if st.button("Submit Inspection"):

        weld_index = df[
            df["Weld ID"] == weld_id
        ].index[0]

        df.loc[
            weld_index,
            "UT Result"
        ] = result

        if result == "PASS":

            df.loc[
                weld_index,
                "Inspection Status"
            ] = "Approved"

        else:

            df.loc[
                weld_index,
                "Inspection Status"
            ] = "Rework Required"

        save_database(df)

        st.success(
            f"Inspection for {weld_id} submitted successfully."
        )

# ==========================
# DEFECT REPORT
# ==========================

elif menu == "⚠️ Defect Reporting":

    st.title("⚠️ Defect Reporting")

    import pandas as pd

    df = load_database()

    # Select Weld

    weld_id = st.selectbox(
        "Select Weld ID",
        df["Weld ID"]
    )

    defect = st.selectbox(
        "Defect Type",
        [
            "Gauge Corner Cracking",
            "Rail Corrugation",
            "Weld Porosity",
            "Sudden Rail Fracture"
        ]
    )

    severity = st.selectbox(
        "Severity Level",
        [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]
    )

    # Auto Recommended Action

    action_dict = {

        "Gauge Corner Cracking":
        "Rail Grinding and Lubrication",

        "Rail Corrugation":
        "Preventive Rail Grinding",

        "Weld Porosity":
        "Reweld Affected Section",

        "Sudden Rail Fracture":
        "Immediate Rail Replacement"
    }

    recommended_action = action_dict[defect]

    st.info(
        f"Recommended Action: {recommended_action}"
    )

    gps = st.text_input(
        "GPS / Track Location"
    )

    uploaded = st.file_uploader(
        "Upload Defect Image",
        type=["jpg","jpeg","png"]
    )

    notes = st.text_area(
        "Defect Description / Inspector Notes"
    )

    if st.button("Submit Defect Report"):

        # Update Database

        weld_index = df[
            df["Weld ID"] == weld_id
        ].index[0]

        df.loc[
            weld_index,
            "Defect Type"
        ] = defect

        df.loc[
            weld_index,
            "Severity Level"
        ] = severity

        df.loc[
            weld_index,
            "Recommended Action"
        ] = recommended_action

        save_database(df)

        st.success(
            f"Defect report for {weld_id} submitted successfully."
        )

        st.write("### Report Summary")

        st.write(
            f"**Weld ID:** {weld_id}"
        )

        st.write(
            f"**Defect Type:** {defect}"
        )

        st.write(
            f"**Severity:** {severity}"
        )

        st.write(
            f"**Recommended Action:** {recommended_action}"
        )

        if uploaded:

            st.image(
                uploaded,
                caption="Uploaded Defect Image"
            )

# ==========================
# AI RISK
# ==========================

elif menu == "🤖 Risk Prediction":

    st.title("🤖 Smart Risk Prediction")

    import pandas as pd

    df = load_database()

    # Select Weld

    weld_id = st.selectbox(
        "Select Weld ID",
        df["Weld ID"]
    )

    age = st.slider(
        "Weld Age (Years)",
        0,
        20,
        5
    )

    defects = st.slider(
        "Number of Previous Defects",
        0,
        10,
        1
    )

    traffic = st.slider(
        "Traffic Load (%)",
        0,
        100,
        50
    )

    ut_result = st.selectbox(
        "UT Result",
        [
            "PASS",
            "PENDING",
            "FAIL"
        ]
    )

    inspection_status = st.selectbox(
        "Inspection Status",
        [
            "Approved",
            "Pending Inspection",
            "Rework Required"
        ]
    )

    score = age * 2
    score += defects * 5
    score += traffic * 0.2

    if ut_result == "FAIL":
        score += 20

    elif ut_result == "PENDING":
        score += 10

    if inspection_status == "Rework Required":
        score += 15

    elif inspection_status == "Pending Inspection":
        score += 5

    st.subheader(
        f"Risk Score: {round(score,1)}%"
    )

    if score < 30:

        st.success("🟢 LOW RISK")

        st.info(
            "Recommended Action: Continue routine inspection schedule."
        )

    elif score < 60:

        st.warning("🟡 MEDIUM RISK")

        st.info(
            "Recommended Action: Schedule inspection within 30 days."
        )

    elif score < 80:

        st.warning("🟠 HIGH RISK")

        st.info(
            "Recommended Action: Schedule inspection within 7 days."
        )

    else:

        st.error("🔴 CRITICAL RISK")

        st.info(
            "Recommended Action: Immediate maintenance intervention required."
        )

# ==========================
# WELD DATABASE
# ==========================

elif menu == "📁 Weld Database":

    st.title("📁 Weld Database")

    import pandas as pd

    df = load_database()

    st.subheader("Search & Filter")

    search = st.text_input(
        "Search Weld ID"
    )

    status_filter = st.selectbox(
        "Inspection Status",
        [
            "All",
            "Approved",
            "Pending Inspection",
            "Rework Required",
            "Maintenance Completed"
        ]
    )

    severity_filter = st.selectbox(
        "Severity Level",
        [
            "All",
            "None",
            "Low",
            "Medium",
            "High",
            "Critical"
        ]
    )

    filtered_df = df.copy()

    if search:

        filtered_df = filtered_df[
            filtered_df["Weld ID"]
            .astype(str)
            .str.contains(
                search,
                case=False
            )
        ]

    if status_filter != "All":

        filtered_df = filtered_df[
            filtered_df["Inspection Status"]
            == status_filter
        ]

    if severity_filter != "All":

        filtered_df = filtered_df[
            filtered_df["Severity Level"]
            == severity_filter
        ]

    st.subheader("Weld Records")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# ==========================
# QA/QC ANALYTICS
# ==========================

elif menu == "📈 QA/QC Analytics":

    st.title("📈 QA/QC Analytics Dashboard")

    import pandas as pd

    df = load_database()

    # ==========================
    # KPI SECTION
    # ==========================

    total_welds = len(df)

    approved = len(
        df[
            df["Inspection Status"]
            == "Approved"
        ]
    )

    pending = len(
        df[
            df["Inspection Status"]
            == "Pending Inspection"
        ]
    )

    rework = len(
        df[
            df["Inspection Status"]
            == "Rework Required"
        ]
    )

    maintenance_completed = len(
        df[
            df["Inspection Status"]
            == "Maintenance Completed"
        ]
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total Welds",
        total_welds
    )

    col2.metric(
        "Approved",
        approved
    )

    col3.metric(
        "Pending",
        pending
    )

    col4.metric(
        "Rework",
        rework
    )

    col5.metric(
        "Maintenance Completed",
        maintenance_completed
    )

    st.divider()

    # ==========================
    # UT RESULT
    # ==========================

    st.subheader(
        "UT Result Distribution"
    )

    ut_counts = df[
        "UT Result"
    ].value_counts()

    st.bar_chart(
        ut_counts
    )

    # ==========================
    # INSPECTION STATUS
    # ==========================

    st.subheader(
        "Inspection Status Distribution"
    )

    status_counts = df[
        "Inspection Status"
    ].value_counts()

    st.bar_chart(
        status_counts
    )

    # ==========================
    # DEFECT TYPES
    # ==========================

    st.subheader(
        "Defect Type Distribution"
    )

    defect_counts = df[
        "Defect Type"
    ].value_counts()

    st.bar_chart(
        defect_counts
    )

    # ==========================
    # SEVERITY LEVEL
    # ==========================

    st.subheader(
        "Severity Level Distribution"
    )

    severity_counts = df[
        "Severity Level"
    ].value_counts()

    st.bar_chart(
        severity_counts
    )

# ==========================
# MAINTENANCE ALERTS
# ==========================

elif menu == "🚨 Maintenance Alerts":

    st.title("🚨 Maintenance Alert System")

    import pandas as pd

    df = load_database()

    critical_alerts = df[
    (
        (df["Severity Level"] == "Critical")
        |
        (df["Inspection Status"] == "Rework Required")
    )
    &
    (
        df["Inspection Status"]
        != "Maintenance Completed"
    )
]

    high_alerts = df[
        df["Severity Level"] == "High"
    ]

    st.subheader("🔴 Critical Alerts")

    if len(critical_alerts) > 0:

        for _, row in critical_alerts.iterrows():

            st.error(
                f"""
Weld ID: {row['Weld ID']}

Defect: {row['Defect Type']}

Severity: {row['Severity Level']}

Action: {row['Recommended Action']}
"""
            )

    else:

        st.success(
            "No Critical Alerts"
        )

    st.divider()

    st.subheader("🟡 High Priority Alerts")

    if len(high_alerts) > 0:

        for _, row in high_alerts.iterrows():

            st.warning(
                f"""
Weld ID: {row['Weld ID']}

Defect: {row['Defect Type']}

Severity: {row['Severity Level']}

Action: {row['Recommended Action']}
"""
            )

    else:

        st.success(
            "No High Priority Alerts"
        )

# ==========================
# MAINTENANCE ACTION
# ==========================

elif menu == "🔧 Maintenance Action":

    st.title("🔧 Maintenance Action")

    import pandas as pd
    from datetime import date

    df = load_database()

    weld_id = st.selectbox(
        "Select Weld ID",
        df["Weld ID"]
    )

    maintenance_type = st.selectbox(
        "Maintenance Performed",
        [
            "Rail Grinding",
            "Rewelding",
            "Lubrication",
            "Rail Replacement",
            "Preventive Inspection"
        ]
    )

    engineer = st.text_input(
        "Maintenance Engineer"
    )

    maintenance_date = st.date_input(
        "Maintenance Date",
        date.today()
    )

    if st.button("Complete Maintenance"):

        weld_index = df[
            df["Weld ID"] == weld_id
        ].index[0]

        df.loc[
            weld_index,
            "Maintenance History"
        ] = maintenance_type

        df.loc[
            weld_index,
            "Maintenance Date"
        ] = maintenance_date

        df.loc[
            weld_index,
            "Maintenance Engineer"
        ] = engineer

        df.loc[
            weld_index,
            "Inspection Status"
        ] = "Maintenance Completed"

        save_database(df)

        st.success(
            f"{weld_id} maintenance record updated successfully."
        )
