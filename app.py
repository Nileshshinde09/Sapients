import streamlit as st
import pandas as pd
import re
import os
# import pdfconvert
menu=st.sidebar.radio(
    'Select Option',
    ('Home','Update Number','Admin')
)
if menu=='Home':
    # Create empty DataFrame
    # df = pd.DataFrame(columns=['Name', 'Semester', 'Phone Number'])
    df=pd.read_csv('df.csv')
    # Streamlit app
    st.title("Sapients")
    st.header("Add Number")

    # Input form to add members
    semester = st.selectbox("Select Semester:", ['I', 'III','V'])
    # name = st.text_input("Enter First Name:")
    # lname = st.text_input("Enter Last Name:")
    try:
        if semester == 'I':
            stdlist = df[(df['semester'] == 'I') & (df['mobile_no'] == 0)]['members'].unique()
        elif semester == 'III':
            stdlist = df[(df['semester'] == 'III') & (df['mobile_no'] == 0)]['members'].unique()
        elif semester == 'V':
            stdlist = df[(df['semester'] == 'V') & (df['mobile_no'] == 0)]['members'].unique()
    except Exception as e:
        print(e)
    name=st.selectbox("Select Name:", stdlist)
    phone_number = str(st.number_input("Enter Phone Number:",step=1))

    # Check if the phone number follows a specific format
    phone_format_regex = r'^\d{10}$'  # Assumes a 10-digit phone number format
    phone_number_valid = re.match(phone_format_regex, phone_number) is not None

    if not phone_number_valid:
        st.warning("Please enter a valid 10-digit phone number.")

    # Add member to DataFrame
    if st.button("Add Member") and phone_number_valid:
        df[df['members']==name]['mobile_no']=phone_number
        df.to_csv('df.csv')
        st.success("Member added successfully!")

if menu=='Update Number':
    # Create empty DataFrame
    # df = pd.DataFrame(columns=['Name', 'Semester', 'Phone Number'])
    df=pd.read_csv('df.csv')
    # Streamlit app
    st.title("Sapients")
    st.header("Update Number")
    # Input form to add members
    semester = st.selectbox("Select Semester:", ['I', 'III','V'])
    # name = st.text_input("Enter First Name:")
    # lname = st.text_input("Enter Last Name:")
    try:
        if semester == 'I':
            stdlist = df[(df['semester'] == 'I') & (df['mobile_no'] != 0)]['members'].unique()
        elif semester == 'III':
            stdlist = df[(df['semester'] == 'III') & (df['mobile_no'] != 0)]['members'].unique()
        elif semester == 'V':
            stdlist = df[(df['semester'] == 'V') & (df['mobile_no'] != 0)]['members'].unique()
    except Exception as e:
        print(e)
    st.text("If your name is not listed, it means you haven't added your mobile number yet. Please do so by entering your details in the Home Page.")
    name=st.selectbox("Select Name:", stdlist)
    try:
        if name:
            phone_number = str(st.number_input("Enter Phone Number:",step=1,value=df[df['members']==name]['mobile_no'].values[0]))

        # Check if the phone number follows a specific format
        phone_format_regex = r'^\d{10}$'  # Assumes a 10-digit phone number format
        phone_number_valid = re.match(phone_format_regex, phone_number) is not None

        if not phone_number_valid:
            st.warning("Please enter a valid 10-digit phone number.")

        # Add member to DataFrame
        if st.button("Update Member") and phone_number_valid:
            df[df['members']==name]['mobile_no']=phone_number
            df.to_csv('df.csv')
            st.success("Member added successfully!")
    except Exception:
        pass



if menu=='Admin':
    password=st.text_input("Enter Password:")
    if st.button("Submit"):
        if password==os.environ["realpass1"] or password==os.environ["realpass2"]:
            df=pd.read_csv('df.csv')
            st.header(f"Remaining Members : {df[df['mobile_no']==0].shape[0]}")
            df['mobile_no'].isnull().sum()
            # Display DataFrame
            st.subheader("Group Members' Data:")
            st.table(df)

            with open('df.csv') as f:
                st.download_button('Download CSV',
        data=f,
        file_name='group_members_report.csv',)  
            
        #     filename=pdfconvert.convert_df_to_pdf(df)
        #     with open(filename) as f:
        #         st.download_button('Download PDF',
        # data=f,
        # file_name='group_members_report.pdf',)            
        if password!=os.environ["realpass1"] or password!=os.environ["realpass2"]:
            st.warning("Wrong Password")
