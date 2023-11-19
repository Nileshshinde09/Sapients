import streamlit as st
import pandas as pd
import re
import os
# import pdfconvert
from streamlit_option_menu import option_menu

if __name__=="__main__":

    st.set_page_config(
        page_title="Sapients",
        page_icon="📚",
            layout="wide",
            initial_sidebar_state="collapsed",
            menu_items={
                'Get Help': 'https://www.extremelycoolapp.com/help',
                'Report a bug': "https://www.extremelycoolapp.com/bug",
                'About': "# This is a header. This is an *extremely* cool app!"}
    )
    hide_menu_style ="""
            <style>
             #MainMenu {visibility: hidden;}
             </style>
             """

    st.markdown(hide_menu_style, unsafe_allow_html=True)
    no_sidebar_style = """
    <style>
        div[data-testid="collapsedControl"] {display: none;}
    </style>
    """
    st.markdown(no_sidebar_style, unsafe_allow_html=True)
    def streamlit_menu1():
        selected = option_menu(
        menu_title=None,  # required
        options=["Home", "Update","Admin"],  # required
        icons=["house", "update","admin"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
        orientation="horizontal",
        )
        return selected


    menu= streamlit_menu1()

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

        def checkexistance(phone_number):
            if int(phone_number) in df['mobile_no'].values:
                st.warning("Number already exist,Try another one..")
                return False
            else:
                return True

        if not phone_number_valid:
            st.warning("Please enter a valid 10-digit phone number.")
        
        # Add member to DataFrame
        if st.button("Add Number") and phone_number_valid and checkexistance(phone_number):
            df.at[df[df['members']==name].index[0],'mobile_no']=int(phone_number)
            df.to_csv('df.csv',index=False)
            st.success("Number added successfully!")

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
                newname=str(st.text_input("Enter New Name",value=df[df['members']==name]['members'].values[0]))
                phone_number = str(st.number_input("Enter Phone Number:",step=1,value=df[df['members']==name]['mobile_no'].values[0]))

            # Check if the phone number follows a specific format
            def strlen():
                if len(newname) <5:
                    st.warning("The length of the input name should be greater than 2 characters.")
                    return False
                else:
                    return True
            if st.button("Update Name") and strlen():
                df.at[df[df['members']==name].index[0],'members']=newname
                df.to_csv('df.csv',index=False)

                st.success("Name Updated successfully!")
            phone_format_regex = r'^\d{10}$'  # Assumes a 10-digit phone number format
            phone_number_valid = re.match(phone_format_regex, phone_number) is not None
            def checkexistance(phone_number):
                if int(phone_number) in df['mobile_no'].values:
                    st.warning("Number already exist,Try another one..")
                    return False
                else:
                    return True
  
            if not phone_number_valid:
                st.warning("Please enter a valid 10-digit phone number.")

            # Add member to DataFrame
            if st.button("Update Number") and phone_number_valid and checkexistance(phone_number):
                df.at[df[df['members']==name].index[0],'mobile_no']=int(phone_number)
                df.to_csv('df.csv',index=False)
                st.success("Number Updated successfully!")

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
