# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 11:51:52 2021

@author: reb00762
"""

from variables import leapfrog_variables
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
from numpy import nan
import warnings
warnings.filterwarnings("ignore")

(grade_cutoffs, facilities, calculation_metrics) = leapfrog_variables()

#initialize repository dictionary for points

st.markdown('''
    ## Instructions for the Leapfrog Hospital Safety Grade Calculator											

    All means, standard deviations, measure weights, and letter grade cut-scores 
    are Spring 2022 data. These parameters will change.	  
					
    The purpose of this calculator is to estimate safety grade based on past data
    and current entries to understand possible opportunities for a potential higher points.						
    However, the points/grade calculated on this calculator will not be your exact future points/grade.						
    
    As you calculate points for your individual measures, the points will appear next to their respective
    measure in the points bank at left.
    										
    Spring 2022 survey required sections are:	 					
    - Section 1: Basic Hospital Information  						
    - Section 2: Medication Safety – CPOE  						
    - Section 4: Maternity Care  						
    - Section 5: ICU Physician Staffing  						
    - Section 6: Patient Safety Practices  
  						
    Not required to submit, but needed for hospital safety grade:  						
    - Section 7: Managing Serious Errors						
    - Section 8: Medication Safety - BCMA  

    ''')

st.markdown('''---''')

#%% section 1

st.header('Hospital Information')

facility = st.selectbox('Facility', options=facilities, key = 'facility')

st.markdown('''---''')

#%% CPOE
st.header('Medication Safety-Computerized Physician Order (CPOE)')

with st.expander(''):
    
    #initialize demonstration and implementation status
    st.session_state.demonstration = 'Insufficient Evaluation'
    st.session_state.implementation_status = np.nan

    cpoe2_c1, cpoe2_c2 = st.columns([2,1])
    
    with cpoe2_c1:
        
        st.markdown('''
                    2) Does your hospital have a functioning CPOE system in one or more inpatient units of the hospital that:    
                     - includes decision support software to reduce prescribing errors; and,   
                     - is linked  to pharmacy, laboratory, and admitting-discharge-transfer 
                     (ADT) information in your hospital? 
                    ''')
            
    with cpoe2_c2:
        
        cpoe_q2 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'cpoe_q2')

    st.info('''*If No to question #2, skip the remaining questions in Section 2, and go to the Affirmation of Accuracy. The hospital will be 
                scored as Limited Achievement.*''')

    st.markdown('''----''') 

    if cpoe_q2 == '':
        
        cpoe_survey_score = 'Unable to Calculate Score'
        cpoe_survey_points = -1
        
    elif cpoe_q2 == 'No':
        
        cpoe_survey_score = 'Limited Achievement'
        cpoe_survey_points = 15
        
    elif cpoe_q2 == 'Yes':
    
        cpoe3_c1, cpoe3_c2 = st.columns([2,1]) 
        
        with cpoe3_c1:    
            
            st.markdown('''3) Total number of inpatient medication orders, including 
                        orders made in units which do NOT have a functioning CPOE system. **-1 indicates a missing or not applicable value.**''')
       
        with cpoe3_c2:
            
            cpoe_q3 = st.number_input('', min_value = -1, key = 'cpoe_q3')

        st.markdown('''----''')    
        
        cpoe4_c1, cpoe4_c2 = st.columns([2,1])
        
        with cpoe4_c1:
            
            st.markdown('''4) Number of inpatient medication orders in question #3 that licensed prescribers entered via 
                       a CPOE system that meets the criteria outlined in question #2. **-1 indicates a missing or not applicable value.**
                       ''')
                
        with cpoe4_c2:
            
            cpoe_q4 = st.number_input('', min_value = -1, key = 'cpoe_q4')
        
        #-----------------------------------------------------------------#
        #IMPLEMENTATION STATUS
        
        # if q3 & q4 are not 0, implementation status is q4/q
        implementation_status = cpoe_q4/cpoe_q3 if (cpoe_q3 > 0) & (cpoe_q4 > 0) else np.nan

        st.session_state.implementation_status = implementation_status

        st.markdown('''----''')   

        cpoe5_c1, cpoe5_c2 = st.columns([2,1])
        
        with cpoe5_c1:
            
            st.markdown('''5) Is your hospital using the Leapfrog CPOE Evaluation Tool to test?''')
        
        with cpoe5_c2:
            
            cpoe_q5 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'cpoe_q5')
 
        st.info('''*If not, skip question 6.*''')   
           
        if cpoe_q5 == 'Yes':
            
            st.markdown('''----''')
        
            cpoe6_c1, cpoe6_c2 = st.columns([2,1]) 
            
            with cpoe6_c1:
                
                st.markdown('''6) What was your hospital’s points when it tested its CPOE system using the Leapfrog CPOE Evaluation Tool?  
                            Adult Inpatient Test must be completed between April 1 – November 30, 2021. **-1 indicates a missing or not applicable value.**''')
            
            with cpoe6_c2:
                
                cpoe_q6 = st.number_input('', 
                                          min_value = -1.0, 
                                          step = 1.,
                                          format = '%.2f')
            
             #-----------------------------------------------------------------#
            #DEMONSTRATION
            #from input to q6 (CPOE Tool points)
            #input is percentage x 100, e.g. 60 = 60%
            
            #greater than or equal to 60
            if cpoe_q6 >= 60: 
                st.session_state.demonstration = 'Full Demonstration'    
            
            #between 50 and less than 60
            elif (cpoe_q6 < 60) & (cpoe_q6 >= 50):
                st.session_state.demonstration = 'Substantial Demonstration'  
                
            #between 40 and less than 50
            elif (cpoe_q6 < 50) & (cpoe_q6 >= 40): 
                st.session_state.demonstration = 'Some Demonstration'   
        
            #less than 40
            elif cpoe_q6 < 40: 
               st.session_state.demonstration = 'Completed the Demonstration'
                
            #otherwise
            else: 
                st.session_state.demonstration = 'Insufficient Evaluation'

        elif cpoe_q5 != 'Yes':
            
            st.session_state.demonstration = 'Insufficient Evaluation'

        st.markdown('''----''')

    #%% CPOE Logic
    
    if st.button('Calculate CPOE'):
        
        #section timestamp
        cpoe_timestamp = datetime.now().strftime('%m-%d-%Y %H:%M %p')
       
        if (cpoe_q2 == '') | ('No' in cpoe_q2): 
            cpoe_survey_score = 'Limited Achievement'
            cpoe_survey_points = 15
        
        elif cpoe_q4 > cpoe_q3:
            
            st.error('Please double check questions 3 and 4. The value for question 4 (numerator) cannot be higher than the value for question 3.')
            st.stop()
        
        elif cpoe_q3 > 0 and cpoe_q4 == -1:
            
            st.error('Please double check question 4. It is possible a value is needed for the denominator.')
            st.stop()
        
        elif cpoe_q5 == 'Yes' and cpoe_q6 == -1:
            st.error('Are your Leapfrog CPOE Evaluation Tool points missing?')
            st.stop()

        else:
    
            #-----------------------------------------------------------------#
            # INPUT VARIABLES TO MAKE BELOW LOGIC MORE CONCISE
        
            # full in demonstration
            full = 'Full' in st.session_state.demonstration
            
            #substantial in demonstration
            substantial = 'Substantial' in st.session_state.demonstration
            
            #some in demonstration
            some = 'Some' in st.session_state.demonstration
            
            #completed in demonstration
            completed = 'Completed' in st.session_state.demonstration
        
            # q5 was answered Yes
            q5 = 'Yes' in cpoe_q5 
            
            #q5 was answered No
            q5_False = 'No' in cpoe_q5 or '' in cpoe_q5
            
            #q2 was answered Yes
            q2_True = 'Yes' in cpoe_q2 
            
            # implementation status greater than or equal to .85 isA
            isA = st.session_state.implementation_status >= .85
            
            # implementation status greater than or equal to .75 but less than .85 isB
            isB = (st.session_state.implementation_status < .85) & (st.session_state.implementation_status >= .75)
            
            # implementation status greater than or equal to .55 but less than .75 isC
            isC = (st.session_state.implementation_status < .75) & (st.session_state.implementation_status >= .50)
            
            # implementation status less than .50 isD
            isD = st.session_state.implementation_status < .50
            
            #-----------------------------------------------------------------#
            # CPOE MAIN LOGIC
            
            #logic for Achieved the Standard/points of 100
            if (q2_True & q5_False & isA) | (q2_True & q5 & isA & full) | (q2_True & q5 & isB & full):
                cpoe_survey_score = 'Achieved the Standard'
                cpoe_survey_points = 100  
             
            # logic for Considerable Achievement/points of 70
            elif (q2_True & q5_False & isB) | (q2_True & q5 & isA & substantial) | (q2_True & q5 & isA & some) | (q2_True & q5 & isB & substantial) | (q2_True & q5 & isC & full) | (q2_True & q5 & isC & substantial) | (q2_True & q5 & isD & full):
                cpoe_survey_score = 'Considerable Achievement'
                cpoe_survey_points = 70
         
            #logic for Some Achievement/points of 40
            elif (q2_True & q5_False & isC) | (q2_True & q5 & isA & completed) | (q2_True & q5 & isB & some) | (q2_True & q5 & isB & completed) | (q2_True & q5 & isC & some) | (q2_True & q5 & isD & substantial) | (q2_True & q5 & isD & some):
                cpoe_survey_score = 'Some Achievement'
                cpoe_survey_points = 40
            
            #logic for Limited Achievement/points of 15
            #Q2 No automatically Limited Achievement
            elif (cpoe_q2 == '') | ('No' in cpoe_q2) | (q2_True & q5_False & isD) | (q2_True & q5 & isC & completed) | (q2_True & q5 & isD & completed): 
                cpoe_survey_score = 'Limited Achievement'
                cpoe_survey_points = 15
        
            else:
                cpoe_survey_score = 'Unable to Calculate Score'
                cpoe_survey_points = -1

        #save to bank
        st.session_state.cpoe_scores = cpoe_survey_score
        st.session_state.cpoe_points = cpoe_survey_points
        st.session_state.CPOE = cpoe_survey_points
        
        st.markdown('''----''') 
        
        #display points
        cpoe_points_col1, cpoe_points_col2 = st.columns(2)
        
        with cpoe_points_col1:
            
            st.write('Score')
            st.success(cpoe_survey_score)
        
        with cpoe_points_col2:
            
            st.write('Points')
            
            if cpoe_survey_points == -1:
                st.success('Not Applicable')
            else:
                st.success(cpoe_survey_points)
        
st.markdown('''----''')

#%% BCMA

st.header('Bar Code Medication Administration (BCMA)')

with st.expander(''):
    
    bcma2_col1, bcma2_col2 = st.columns(2)

    with bcma2_col1:
        
        st.write('''2) Does your hospital use a Bar Code Medication Administration (BCMA) system that is linked to the electronic medication
                 administration record (eMAR) when administering medications at the bedside in at least one inpatient unit?''')
                
    with bcma2_col2:
        
        bq2 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq2')

    st.info('''*If No to question #2, skip questions #3-15 and continue on to the next subsection*.''')
                 
    st.markdown('''----''')
    
    if bq2 == 'Yes':

        bcma3_col1, bcma3_col2 = st.columns(2)
    
        with bcma3_col1:
            
            st.write('''3) Does your hospital operate Intensive Care Units (adult, pediatric, and/or neonatal)?''')
    
        with bcma3_col2:  
            
            bq3 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq3')

        st.markdown('''----''')
        
        st.info('''*If No to question #3, skip questions #4-5 and continue on to question #6*.''')
    
        st.markdown('''----''')
    
        if bq3 == 'Yes':
        
            bcma4_col1, bcma4_col2 = st.columns(2)
        
            with bcma4_col1:
                
                st.write('''4) If Yes, how many of this type of unit are open and staffed in the hospital? **-1 indicates a missing or not applicable value.**''')
        
            with bcma4_col2:
                
                bq4 = st.number_input('', min_value = -1, key = 'bq4')

            st.markdown('''----''')
      
            bcma5_col1, bcma5_col2 = st.columns(2)
        
            with bcma5_col1:
                
                st.write('''5) How many of the units in question #4 utilized the BCMA/eMAR system when 
                        administering medications at the bedside? **-1 indicates a missing or not applicable value.**''')
        
            with bcma5_col2:
                
                bq5 = st.number_input('', min_value = -1, key = 'bq5')
 
            st.markdown('''----''')

        bcma6_col1, bcma6_col2 = st.columns(2)
    
        with bcma6_col1:
            
            st.write('''6) Does your hospital operate Medical and/or Surgical Units (including telemetry units) (adult and/or pediatric)?''')
    
        with bcma6_col2:
            
            bq6 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq6')
  
        st.markdown('''----''')
        
        st.info('''*If No to question #6, skip questions #7-8 and continue on to question #9.*''')
        
        st.markdown('''----''')
        
        if bq6 == 'Yes':
    
            bcma7_col1, bcma7_col2 = st.columns(2)
        
            with bcma7_col1:
                
                st.write('''7) If Yes, how many of this type of unit were open and staffed in the hospital? **-1 indicates a missing or not applicable value.**''')
        
            with bcma7_col2:
                
                bq7 = st.number_input('', min_value = -1, key = 'bq7')

            st.markdown('''----''')
        
            bcma8_col1, bcma8_col2 = st.columns(2)
        
            with bcma8_col1:
                
                st.write('''8) How many of the units in question #7 utilized the BCMA/eMAR system when 
                            administering medications at the bedside? **-1 indicates a missing or not applicable value.**''')
        
            with bcma8_col2:
                
                bq8 = st.number_input('', min_value = -1, key = 'bq8')

            st.markdown('''----''')    

        bcma9_col1, bcma9_col2 = st.columns(2)
    
        with bcma9_col1:
            
            st.write('''9) Does your hospital operate a Labor and Delivery Unit?''')

        with bcma9_col2:
            
            bq9 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq9')
 
        st.info('''*If No to question #9, skip questions #10-11 and continue on to question #12.*''')
        
        st.markdown('''----''')
        
        # if Q9 is Yes, allow Qs 10-11
        if bq9 == 'Yes':
            
            bcma10_col1, bcma10_col2 = st.columns(2)
        
            with bcma10_col1:
                
                st.write('''10) If Yes, how many of this type of unit were open and staffed in the hospital? **-1 indicates a missing or not applicable value.**''')
        
            with bcma10_col2:
                
                bq10 = st.number_input('', min_value = -1,  key = 'bq10')

            st.markdown('''----''')
        
            bcma11_col1, bcma11_col2 = st.columns(2)
        
            with bcma11_col1:
                
                st.write('''11) How many of the units in question #10 utilized the BCMA/eMAR system when administering medications at the bedside?
                             **-1 indicates a missing or not applicable value.**''')
        
            with bcma11_col2:
                
                bq11 = st.number_input('', min_value = -1,  key = 'bq11')

            st.info('''*If No to questions #3, #6, and #9 above, skip questions #12-15 and continue on to the next subsection. Your hospital will be scored as **Does Not Apply**.*''')

            st.markdown('''----''')
                
        # if Q9 was not Yes but Q3 and/or Q6 were Yes, then skip Q10-11 and continue on to Q12  -OR- if Q9 is Yes, continue on to Q12
        if (bq9 != 'Yes' and (bq3 == 'Yes' or bq6 == 'Yes')):

            bcma12_col1, bcma12_col2 = st.columns(2)
    
            with bcma12_col1:
                
                st.write('''12) The number of scannable inpatient medication administrations during the reporting 
                            period in those units that utilize BCMA as indicated in questions #5, #8, and #11 above? **-1 indicates a missing or not applicable value.**''')
        
            with bcma12_col2:
                
                bq12 = st.number_input('', min_value = -1, key = 'bq12')

            st.markdown('''----''')
        
            bcma13_col1, bcma13_col2 = st.columns(2)
        
            with bcma13_col1:
                
                st.write('''13) The number of medication administrations from question #12 that had both the patient 
                            and the medication scanned during administration with a BCMA system that is linked to 
                            the electronic medication administration record (eMAR)? **-1 indicates a missing or not applicable value.**''')
        
            with bcma13_col2:
                
                bq13 = st.number_input('', min_value = -1, key = 'bq13')

            if bq13 > bq12:
            
                st.error('Please double check questions 12 and 13. The value for question 13 (numerator) cannot be higher than the value for question 12.')
                st.stop()

            st.markdown('''----''')
        
            st.write('''*14) What types of decision support does your hospital’s BCMA system provide to users of the system?*''')
            
            st.info('''*Do not leave any questions blank*.''')
            
            st.markdown('''----''')
            
            bcma14a_col1, bcma14a_col2 = st.columns(2)
        
            with bcma14a_col1:
                
                st.write('''14a) Wrong patient''')
        
            with bcma14a_col2:
                
                bq14a = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq14a')

            st.markdown('''----''')
        
            bcma14b_col1, bcma14b_col2 = st.columns(2)
        
            with bcma14b_col1:
                
                st.write('''14b) Wrong medication''')
        
            with bcma14b_col2:
                
                bq14b = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq14b')

            st.markdown('''----''')
        
            bcma14c_col1, bcma14c_col2 = st.columns(2)
        
            with bcma14c_col1:
                
                st.write('''14c) Wrong dose''')
        
            with bcma14c_col2:
                
                bq14c = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq14c')

            st.markdown('''----''')
        
            bcma14d_col1, bcma14d_col2 = st.columns(2)
        
            with bcma14d_col1:
                
                st.write('''14d) Wrong time (e.g., early/late error; error that medication cannot be administered twice within a given window of time)''')
        
            with bcma14d_col2:
                
                bq14d = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq14d')

            st.markdown('''----''')
        
            bcma14e_col1, bcma14e_col2 = st.columns(2)
        
            with bcma14e_col1:
                
                st.write('''14e) Second nurse check needed''')
        
            with bcma14e_col2:
                
                bq14e = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq14e')

            st.markdown('''----''')
        
            st.markdown('''*15) Which of the following mechanisms does your hospital use to reduce and understand potential BCMA system “workarounds”?*''')

            st.info('''*Do not leave any questions blank.*''')
            
            st.markdown('''----''')
            
            bcma15a_col1, bcma15a_col2 = st.columns(2)
        
            with bcma15a_col1:
                
                st.write('''15a) Has a formal committee that meets routinely to review data reports on BCMA system use''')
        
            with bcma15a_col2:
                
                bq15a = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq15a')

            st.markdown('''----''')
        
            bcma15b_col1, bcma15b_col2 = st.columns(2)
        
            with bcma15b_col1:
                
                st.write('''15b) Has back-up systems for BCMA hardware failures''')
        
            with bcma15b_col2:
                
                bq15b = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq15b')

            st.markdown('''----''')
        
            bcma15c_col1, bcma15c_col2 = st.columns(2)
        
            with bcma15c_col1:
                
                st.write('''15c) Has a Help Desk that provides timely responses to urgent BCMA issues in real-time''')
        
            with bcma15c_col2:
                
                bq15c = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq15c')

            st.markdown('''----''')
        
            bcma15d_col1, bcma15d_col2 = st.columns(2)
        
            with bcma15d_col1:
                
                st.write('''15d) Conducts real-time observations of users at the unit level using the BCMA system''')
        
            with bcma15d_col2:
                
                bq15d = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq15d')

            st.markdown('''----''')
        
            bcma15e_col1, bcma15e_col2 = st.columns(2)
        
            with bcma15e_col1:
                
                st.write('''15e) Engages nursing leadership at the unit level on BCMA use''')
        
            with bcma15e_col2:
                
                bq15e = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq15e')

            st.markdown('''----''')
        
            bcma15f_col1, bcma15f_col2 = st.columns(2)
        
            with bcma15f_col1:
                
                st.markdown('''15f) In the past 12 months used the data and information obtained through items a-e 
                            to implement quality improvement projects that have focused on improving the hospital’s BCMA performance  
                            **OR**  
                            In the past 12 months used the data and information obtained through items a-e to monitor a 
                            previously implemented quality improvement project focused on improving the hospital’s BCMA performance.''')
                            
            with bcma15f_col2:
                
                bq15f = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq15f')

            st.info('''*Cannot respond Yes to this question, unless Yes to either 15a, b, c, d, or e.*''')
            
            #sums number of Yes answers for questions 15a, b, c, d, and e
            bq15f_yeses = sum(['Yes' in s for s in [bq15a, bq15b, bq15c, bq15d, bq15e]])

            st.markdown('''----''')
        
            bcma15g_col1, bcma15g_col2 = st.columns(2)
        
            with bcma15g_col1:
                
                st.markdown('''15g) In the past 12 months evaluated the results of the quality improvement projects (from f) 
                            and demonstrated that these projects have resulted in higher adherence to your hospital’s 
                            standard medication administration process  
                            **OR**  
                            In the past 12 months evaluated the results of the quality improvement projects (from f) and 
                            demonstrated continued adherence to your hospital’s standard medication administration process.''')
    
            with bcma15g_col2:
                
                bq15g = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq15g')
    
            st.info('''*Cannot respond Yes to this question, unless Yes to 15f.*''')

            st.markdown('''----''')
        
            bcma15h_col1, bcma15h_col2 = st.columns(2)
        
            with bcma15h_col1:
                
                st.write('''15h) Communicated back to end users the resolution of any system deficiencies and/or problems that may have contributed to workarounds.''')
        
            with bcma15h_col2:
                
                bq15h = st.selectbox('', options = ['', 'Yes', 'No'], key = 'bq15h')

            st.info('''*Cannot respond Yes to this question, unless Yes to either 15a, b, c, d, or e.*''')
            
            st.markdown('''----''')
        
        elif (bq3 == 'No') and (bq6 == 'No') and (bq9 == 'No'):
            pass
        
    #%% Begin BCMA Calculation Logic

    if st.button('Calculate BCMA'):
        
        #section timestamp
        bcma_timestamp = datetime.now().strftime('%m-%d-%Y %H:%M %p')
        
        if bq2 != 'Yes':
            
            bcma_survey_scores = 'Limited Achievement'
            bcma_leapfrog_points = 25
            
        else:
            
            if (bq3 != 'No' or bq3 != '') and (bq6 != 'No' or bq6 != '') and (bq9 != 'No' or bq9 != ''):
    
                # BCMA error handling variables & logic
                bq14_answers = sum(['Yes' in s for s in [bq14a, bq14b, bq14c, bq14d, bq14e]]) + sum(['No' in s for s in [bq14a, bq14b, bq14c, bq14d, bq14e]])
                bq15_answers = sum(['Yes' in s for s in [bq15a, bq15b, bq15c, bq15d, bq15e, bq15f, bq15g, bq15h]]) + sum(['No' in s for s in [bq15a, bq15b, bq15c, bq15d, bq15e, bq15f, bq15g, bq15h]])
                bq15f_yeses = sum(['Yes' in s for s in [bq15a, bq15b, bq15c, bq15d, bq15e]])
        
                if (bq15f_yeses == 0 and bq15f == 'Yes') and (bq15g == 'Yes' and bq15f != 'Yes') and (bq15f_yeses == 0 and bq15h == 'Yes') and (bq14_answers < 5) and (bq15_answers < 16) and (bq12 > 0 and bq13 == -1):
                    
                    st.error('Please double check question 13. It is possible a value is needed for the denominator.')
                    st.error('Cannot answer Yes to 15f unless Yes to either 15a, b, c, d, or e.')
                    st.error('Cannot answer Yes to 15h unless Yes to either 15a, b, c, d, or e.')
                    st.error('One or more of questions 14a through 14e are missing answers.')
                    st.error('One or more of questions 15a through 15e are missing answers.')
                    st.error('Cannot answer Yes to 15g unless Yes to 15f.')
                    st.stop()
        
                elif (bq15f_yeses == 0 and bq15f == 'Yes') and (bq15g == 'Yes' and bq15f != 'Yes') and (bq15f_yeses == 0 and bq15h == 'Yes') and (bq15_answers < 16) and (bq12 > 0 and bq13 == -1):
                    
                    st.error('Please double check question 13. It is possible a value is needed for the denominator.')
                    st.error('Cannot answer Yes to 15f unless Yes to either 15a, b, c, d, or e.')
                    st.error('Cannot answer Yes to 15h unless Yes to either 15a, b, c, d, or e.')
                    st.error('One or more of questions 15a through 15e are missing answers.')
                    st.error('Cannot answer Yes to 15g unless Yes to 15f.')
                    st.stop()
               
                elif (bq15f_yeses == 0 and bq15f == 'Yes') and (bq15g == 'Yes' and bq15f != 'Yes') and (bq15f_yeses == 0 and bq15h == 'Yes') and (bq14_answers < 5) and (bq12 > 0 and bq13 == -1):
                        
                    st.error('Please double check question 13. It is possible a value is needed for the denominator.')
                    st.error('Cannot answer Yes to 15f unless Yes to either 15a, b, c, d, or e.')
                    st.error('Cannot answer Yes to 15h unless Yes to either 15a, b, c, d, or e.')
                    st.error('One or more of questions 14a through 14e are missing answers.')
                    st.error('Cannot answer Yes to 15g unless Yes to 15f.')
                    st.stop() 
        
                elif (bq14_answers < 5) and (bq15_answers < 16):
                    
                    st.error('One or more of questions 14a through 14e are missing answers.')
                    st.error('One or more of questions 15a through 15e are missing answers.')
                    st.stop()
                
              
                elif (bq15f_yeses == 0 and bq15f == 'Yes') and (bq15g == 'Yes' and bq15f != 'Yes'):
                        
                    st.error('Cannot answer Yes to 15f unless Yes to either 15a, b, c, d, or e.')
                    st.error('Cannot answer Yes to 15g unless Yes to 15f.')
                    st.stop()
                    
                # check all of 14 are answered
                elif bq14_answers < 5:
                    
                    st.error('One or more of questions 14a through 14e are missing answers.')
                    st.stop()
                
                # check all of 15 are answered
                elif bq15_answers < 5:
                    
                    st.error('One or more of questions 15a through 15e are missing answers.')
                    st.stop()
        
                elif (bq15f_yeses == 0) and (bq15h == 'Yes'):
                    
                    st.error('Cannot answer Yes to 15h unless Yes to either 15a, b, c, d, or e.')
                    st.stop()
                 
                elif bq15g == 'Yes' and bq15f != 'Yes':
                    
                    st.error('Cannot answer Yes to 15g unless Yes to 15f.')
                    st.stop()   
                
                elif bq15f_yeses == 0 and bq15f == 'Yes':
                    
                    st.error('Cannot answer Yes to 15f unless Yes to either 15a, b, c, d, or e.')
                    st.stop()
                    
                elif bq12 > 0 and bq13 == -1:
                
                    st.error('Please double check question 13. It is possible a value is needed for the denominator.')
                    st.stop()
      
            else:
    
                #move forward with calculating the points
                bcma_max_points = 100
                
                # Logic
                bcma_logic_14a = 1 if bq14a == 'Yes' else 0
                bcma_logic_14b = 1 if bq14b == 'Yes' else 0
                bcma_logic_14c = 1 if bq14c == 'Yes' else 0
                bcma_logic_14d = 1 if bq14d == 'Yes' else 0
                bcma_logic_14e = 1 if bq14e == 'Yes' else 0
                
                bcma_logic_15a = 1 if bq15a == 'Yes' else 0
                bcma_logic_15b = 1 if bq15b == 'Yes' else 0
                bcma_logic_15c = 1 if bq15c == 'Yes' else 0
                bcma_logic_15d = 1 if bq15d == 'Yes' else 0
                bcma_logic_15e = 1 if bq15e == 'Yes' else 0
                bcma_logic_15f = 1 if bq15f == 'Yes' else 0
                bcma_logic_15g = 1 if bq15g == 'Yes' else 0
                bcma_logic_15h = 1 if bq15h == 'Yes' else 0
                
                # st.write("The bcma 14a output is: ",bcma_logic_14a)
                
                # Percentage units
                try:
                    bcma_percentage_unit = ((bq5+bq8+bq11) / (bq4+bq7+bq10)) * 100
                    
                except ZeroDivisionError:
                    bcma_percentage_unit = 0
                    
                # st.write("The bcma_percentage_unit output is: ",bcma_percentage_unit)
                
                bcma_percentage_unit_logic = 1 if bcma_percentage_unit == 100 else 0
                # st.write("The bcma_percentage_unit logic output is: ",bcma_percentage_unit_logic)
                
                # Percentage Compliance
                bcma_percentage_compliance = 0 if bq12 == 0 or bq13 == 0 else ((bq13/bq12)*100)
                # st.write("The bcma_percentage_compliance output is: ",bcma_percentage_compliance)
                
                bcma_percentage_compliance_logic = 1 if bcma_percentage_compliance >= 95 else 0
                # st.write("The bcma_percentage_compliance logic output is: ",bcma_percentage_compliance_logic)
                
                # Decision Support
                bcma_decision_support = bcma_logic_14a + bcma_logic_14b + bcma_logic_14c + bcma_logic_14d + bcma_logic_14e
                # st.write("The bcma_decision_support output is: ",bcma_decision_support)
                
                bcma_decision_support_logic = 1 if bcma_decision_support == 5 else 0
                # st.write("The bcma_decision_support logic output is: ",bcma_decision_support_logic)
                
                # Processes and Structures
                bcma_process_and_structure = bcma_logic_15a + bcma_logic_15b + bcma_logic_15c + bcma_logic_15d + bcma_logic_15e + bcma_logic_15f + bcma_logic_15g + bcma_logic_15h
                # st.write("The bcma_process_and_structure output is: ",bcma_process_and_structure)
                
                bcma_process_and_structure_logic = 1 if bcma_process_and_structure >= 6 else 0
                # st.write("The bcma_process_and_structure logic output is: ",bcma_process_and_structure_logic)
                
                bcma_sum = bcma_percentage_unit_logic + bcma_percentage_compliance_logic + bcma_decision_support_logic + bcma_process_and_structure_logic
                # st.write("The bcma_sum output is: ",bcma_sum)
                
                # Survey scores and Leapfrog points
                if (bcma_sum == 4):
                    bcma_survey_scores = 'Achieved the Standard'
                    bcma_leapfrog_points = 100
                
                elif (bcma_sum == 3):
                    bcma_survey_scores = 'Considerable Achievement'
                    bcma_leapfrog_points = 75
                elif (bcma_sum == 2):
                    bcma_survey_scores = 'Some Achievement'
                    bcma_leapfrog_points = 50
                
                else:
                    bcma_survey_scores = 'Limited Achievement'
                    bcma_leapfrog_points = 25
      
        # store BCMA scores here
        st.session_state.bcma_scores = bcma_survey_scores
        st.session_state.bcma_points = bcma_leapfrog_points
        st.session_state.BCMA = bcma_leapfrog_points

        st.markdown('''----''') 
        
        # display points
        bcma_points_col1, bcma_points_col2 = st.columns(2)
        
        with bcma_points_col1:
            
            st.write('Score')
            st.success(bcma_survey_scores)
        
        with bcma_points_col2:
            
            st.write('Points')
            st.success(bcma_leapfrog_points)

st.markdown('''----''')

#%% IPS
st.header('ICU Physician Staffing (IPS)')

with st.expander(''):

    ips2_col1, ips2_col2 = st.columns([2,1])
    
    with ips2_col1:
        
        st.write('''2) Does your hospital operate any adult or pediatric general medical and/or surgical ICUs or neuro ICUs?''')

    with ips2_col2:
        
        ips_q2 = st.selectbox('', options = ['', 'Yes', 'No'], key='ips_q2')

    st.info('''*If No, please skip the remaining IPS questions and go to the Affirmation of Accuracy. Hospital will be scored as **Does Not Apply**.*''')
    
    st.markdown('''---''')

    if ips_q2 == 'Yes':
        
        ips3_col1, ips3_col2 = st.columns([2,1])
        
        with ips3_col1:
            st.write('''3) Do physicians certified in critical care medicine when present on-site or via telemedicine, manage or co-manage all 
                     critical care patients in these ICUs?''')
    
        with ips3_col2:
            ips_q3 = st.selectbox('', 
                                  options = ['', 
                                             'Yes, all are certified in critical care',
                                             'Yes, based on expanded definition of certified',
                                             'No'], key='ips_q3')

        st.info('''*If No, skip questions #4-10 and continue on to question #11.*''')
       
        st.markdown('''---''') 

        if ('Yes' in ips_q3 or ips_q3 == ''):
            
            ips4_col1, ips4_col2 = st.columns([2,1])
            
            with ips4_col1:
                
                st.markdown('''4) Are all critical care patients in each of these ICUs managed or co-managed by one or more physicians certified 
                           in critical care medicine who meet all of the following criteria:     
                            - Ordinarily present on-site in each of these ICUs during daytime hours
                            - For at least 8 hours per day, 7 days per week  
                            - Providing clinical care exclusively in one ICU during these hours''') 
        
            with ips4_col2:
                ips_q4 = st.selectbox('', options = ['', 'Yes', 'No'], key='ips_q4')
    
            #Yes or No is ranked as a considerable achievement

            st.info('''*If Yes to question #4, skip question #5 and continue on to question #6. If No, continue on to question #5*.''')
                        
            st.markdown('''---''')  
    
            if ips_q4 == 'No' or ips_q4 == '':
            
                ips5_col1, ips5_col2 = st.columns([2,1])
                
                with ips5_col1: 
                    
                    st.markdown('''5) Are all critical care patients in each of these ICUs 
                                managed or co-managed by one or more physicians certified 
                                in critical care medicine who meet all of the following criteria:  
                                - Present via telemedicine, in combination with on-site 
                                intensivist coverage, for a total of 24 hours per day, 7 days per week  
                                - Meet all of Leapfrog’s ICU requirements for intensivist 
                                presence in the ICU via telemedicine  
                                - Supported by an on-site intensivist who establishes and 
                                revises the daily care plan for each ICU patient''')
                                
                with ips5_col2:
                    
                    ips_q5 = st.selectbox('', options = ['', 'Yes', 'No'], key='ips_q5')
    
                st.info('''*If No to question #4 and question #5, skip questions #6-7 and continue on to question #8*.''')
                         
                st.markdown('''----''')
    
            else:
                    
                #if question 4 is No and question 5 is not No, don't skip question 6 and 7
    
                ips6_col1, ips6_col2 = st.columns([2,1])
                
                with ips6_col1:
                    
                    st.markdown('''6) When the physicians (from question #3) are not present in these ICUs on-site or via telemedicine, do they return more 
                               than 95% of calls/pages/texts from these units within five minutes, based on a quantified analysis of notification device response time?''')
                
                with ips6_col2:
                    
                     ips_q6 = st.selectbox('', 
                                          options = ['', 'Yes', 'No', 'Not applicable; intensivists are present on-site 24/7'], 
                                          key='ips_q6')
    
                st.markdown('''----''')
                 
                ips7_col1, ips7_col2 = st.columns([2,1]) 
            
                with ips7_col1:    
                    
                    st.markdown('''7) When the physicians (from question #3) are not present on-site in the ICU or not able to physically reach an ICU patient within 5 minutes, 
                                can they rely on a physician, physician assistant, nurse practitione, or FCCS-certified nurse or intern “effector” who is in the 
                                hospital and able to reach these ICU patients within five minutes in more than 95% of the cases, based on a quantified 
                                analysis of notification device response time?''')
                
                with ips7_col2:
                
                    ips_q7 = st.selectbox('', 
                                          options = ['', 'Yes', 'No', 'Not applicable; intensivists are present on-site 24/7'], 
                                          key='ips_q7')
            
                st.info('''*If No to either question #6 or #7 in this section, please answer questions #8-14. 
                             If Yes or Not applicable; intensivists are present on-site 24/7 to questions #6 and #7, 
                             skip the remaining questions in Section 5, and go to the Affirmation of Accuracy*.''')
    
                st.markdown('''----''')
        
            if (ips_q6 == 'Yes' or 'Not' in ips_q6) and (ips_q7 == 'Yes' or 'Not' in ips_q7):
                
                pass
            
            elif (ips_q6 == '' or ips_q6 == 'No') or (ips_q7 == '' or ips_q7 == 'No'):
                
                #move on to question 8
                ips8_col1, ips8_col2 = st.columns([2,1]) 
            
                with ips8_col1:
                    
                    st.markdown('''8) Are all critical care patients in each of these ICUs managed or co-managed by one or more physicians certified in critical care medicine
                               who meet all of the following criteria:  
                                   - ordinarily present on-site in each of these units during daytime hours  
                                   - for at least 8 hours per day, 4 days per week or 4 hours per day, 7 days per week  
                                   - providing clinical care exclusively26 in one ICU during these hours?''')
                
                with ips8_col2:
                    
                    ips_q8 = st.selectbox('', options = ['', 'Yes', 'No'], key='ips_q8')
    
                st.markdown('''----''')
                
                ips9_col1, ips9_col2 = st.columns([2,1]) 
                
                with ips9_col1:
                    
                    st.markdown('''9) Are all critical care patients in each of these ICUs managed or co-managed24 by one or more physicians certified in 
                               critical care medicine25 who meet all of the following criteria:  
                                   - present via telemedicine for 24 hours per day, 7 days per week    
                                   - meet all of Leapfrog’s modified ICU requirements for intensivist presence in the ICU via telemedicine  
                                   - supported in the establishment and revision of daily care planning for each ICU patient by an on-site intensivist, hospitalist, 
                                   anesthesiologist, or physician trained in emergency medicine''')
                
                with ips9_col2:
                    
                    ips_q9 = st.selectbox('', options = ['', 'Yes', 'No'], key='ips_q9')
    
                st.markdown('''----''')
                    
                ips10_col1, ips10_col2 = st.columns([2,1]) 
            
                with ips10_col1:
                    
                    st.markdown('''10) Are all critical care patients in each of these ICUs managed or co-managed24 by one or more physicians certified in 
                               critical care medicine25 who are:  
                                   - on-site at least 4 days per week to establish or revise 
                                   daily care plans for each critical care patient in each of these ICUs?''')
                
                with ips10_col2:
                    
                    ips_q10 = st.selectbox('', options = ['', 'Yes', 'No'], key='ips_q10')     
    
                st.info('''*If Yes to question #8, #9, or #10, skip question #11 and continue on to question #12*.''')
                
                st.markdown('''----''')
    
        if ('Yes' in ips_q3 or 'No' in ips_q3) and ((ips_q6 == '' or ips_q6 == 'No') or (ips_q7 == '' or ips_q7 == 'No')) and (ips_q8 != 'Yes' and ips_q9 != 'Yes'  and ips_q10 != 'Yes'):
            
                ips11_col1, ips11_col2 = st.columns([2,1]) 
                    
                with ips11_col1:
                    
                    st.markdown('''11) If not all critical care patients are managed or co-managed by physicians certified in critical care medicine, either on-site or 
                               via telemedicine, are some patients managed or co-managed by these physicians?''')
                    
                with ips11_col2:
                    
                     ips_q11 = st.selectbox('', options = ['', 'Yes', 'No'], key='ips_q11')
    
                st.markdown('''----''')

        if ('No' not in ips_q2):
            
            if ((ips_q6 == '' or ips_q6 == 'No') or (ips_q7 == '' or ips_q7 == 'No')) or (ips_q8 == 'Yes' or ips_q9 == 'Yes'  or ips_q10 == 'Yes'):
                    
                ips12_col1, ips12_col2 = st.columns([2,1]) 
            
                with ips12_col1:
                    
                    st.markdown('''12) Does an on-site clinical pharmacist do all of the following:  
                        - At least 5 days per week, makes daily on-site rounds on all critical care patients in each of these ICUs  
                        - On the other 2 days per week, returns more than 95% of calls/pages/texts from these units within 5 minutes, based on a quantified analysis 
                        of notification device response time  
                        -OR-    
                        - Makes daily on-site rounds on all critical care patients in each of these ICUs 7 days per week''')
                
                with ips12_col2:
                    
                     ips_q12 = st.selectbox('', options = ['', 'Yes', 'No', 'Clinical pharmacist rounds 7 days per week'], key='ips_q12')
    
                st.markdown('''----''')
                
                ips13_col1, ips13_col2 = st.columns([2,1]) 
            
                with ips13_col1:
                    
                    st.markdown('''13) Does a physician certified in critical care medicine lead daily interprofessional rounds on-site on all critical care patients in each 
                               of these ICUs 7 days per week?''')
                    
                with ips13_col2:
                    
                    ips_q13 = st.selectbox('', options = ['', 'Yes', 'No'], key='ips_q13')
    
                st.markdown('''----''') 
                
                ips14_col1, ips14_col2 = st.columns([2,1])  
                
                with ips14_col1:
                    
                    st.markdown('''14) When physicians certified in critical care medicine are on-site in each of these ICUs, do they have responsibility 
                               for all ICU admission and discharge decisions?''')
                
                with ips14_col2:
                    
                     ips_q14 = st.selectbox('', options = ['', 'Yes', 'No'], key='ips_q14')
    
        st.markdown('''----''') 
    
    #%% Calculate IPS 
    
    if st.button('Calculate IPS'):
        
        #section timestamp
        ips_timestamp = datetime.now().strftime('%m-%d-%Y %H:%M %p')
        
        if ips_q2 == '' or ips_q2 == 'No':
            
            ips_survey_scores = 'Does Not Apply'   
            ips_survey_points = -1
        
        else:
    
            #-----------------------------------------------------------------#
            # Variables for Concise Logic
            
            #if q3 is Yes
            a = 'Yes' in ips_q3
            
            #if q6 is Yes or Not Applicable
            as1 = 'Yes' in ips_q6 or 'Not' in ips_q6
            
            #if q7 is Yes or Not Applicable
            as2 = 'Yes' in ips_q7 or 'Not' in ips_q7
            
            #if q4 or q5 is Yes
            as3 = 'Yes' in ips_q4 or 'Yes' in ips_q5
            
            #if q8 is Yes or q12 is either Yes or Clinical pharmacist rounds 7 days per week
            ca1 = 'Yes' in ips_q8 or ('Yes' in ips_q12 or 'Clinical' in ips_q12)
        
            #if q9 is Yes
            ca3 = 'Yes' in ips_q9 
            
            #if q10 is Yes
            sa1 = 'Yes' in ips_q10 
            
            #if q13 or q14 is Yes
            sa2 = 'Yes' in ips_q13 or 'Yes' in ips_q14
            
            #if q11 is Yes
            sa3 = 'Yes' in ips_q11
        
            #-----------------------------------------------------------------#
            # CORE LOGIC
            
            #if q3 is Yes and q6 & q7 is Yes or Not Applicable and q4 or q5 are Yes
            if (a & as1 & as2 & as3 == True):
                ips_survey_scores = 'Achieved the Standard'
                ips_survey_points = 100
                
            #if q3 is Yes and q8 is Yes or q12 is either Yes or Clinical and q13 or q14 is Yes 
            # - or - 
            # if q3 is Yes and q9 is Yes
            elif (a & ca1 & sa2 == True) | (a & ca3 == True):
                ips_survey_scores = 'Considerable Achievement'   
                ips_survey_points = 50  
             
            #if q3 is Yes and q10 is Yes and q13 or q14 is Yes and q11 is Yes
            elif (a & sa1 & sa2 == True) | (sa3 & sa2 == True): # & sa4
                ips_survey_scores = 'Some Achievement'
                ips_survey_points = 15
        
            elif (ips_q2 == 'No') | (ips_q2 == ''):
                ips_survey_scores = 'Does Not Apply'   
                ips_survey_points = np.nan  
                
            else:
                ips_survey_scores = 'Limited Achievement'  
                ips_survey_points = 5
    
        st.session_state['IPS'] = ips_survey_points    
        
        #display points
        ips_points_col1, ips_points_col2 = st.columns(2)
        
        with ips_points_col1:
            st.write('Score')
            st.success(ips_survey_scores)
        
        with ips_points_col2:
            st.write('Points')
            
            #replace nan with N/A for revealing the points only*
            if ips_survey_points == -1:
                 st.success('N/A')
                 
            else:
                st.success(ips_survey_points)
    
    st.markdown("[Return to Top - IPS](#ips)", unsafe_allow_html=True)
        
st.markdown('''----''')

#%% SP1
st.header('Safe Practice 1 (SP 1)')

with st.expander(''):

    st.markdown('''*Within the last 24 months, in regard to raising the awareness of key stakeholders to our organization’s efforts to improve patient 
                safety, the following actions related to identification and mitigation of risk and hazards have been taken: (CHECK YES to ALL THAT APPLY)*''')
    
    sp1_col1, sp1_col2 = st.columns([2,1])
    
    with sp1_col1:
        
        st.write('''1) Board (governance) minutes reflect regular communication regarding all three of the following:   
                        - risks and hazards (as defined by Safe Practice #4, Identification and Mitigation of Risks and Hazards);  
                        - culture measurement (as defined by Safe Practice #2, Culture Measurement, Feedback, and Intervention); and,  
                        - progress towards resolution of safety and quality problems.''')
                           
    with sp1_col2:
        
        sp1_q1 = st.selectbox('', options = ['', 'Yes', 'No'], key='sp1_q1')

    st.markdown('''----''')
    
    sp12_col1, sp12_col2 = st.columns([2,1])
    
    with sp12_col1:
        
        st.write('''2) Patients and/or families of patients are active participants in the hospital-wide safety and quality 
                committee that meets on a regularly scheduled basis (e.g., biannually or quarterly)''')
     
    with sp12_col2:
        
        sp1_q2 = st.selectbox('', options = ['', 'Yes', 'No'],  key='sp1_q2')

    st.markdown('''----''')
    
    sp13_col1, sp13_col2 = st.columns([2,1])   

    with sp13_col1:  
                  
        st.write('''3) Steps have been taken to report ongoing efforts to improve safety and quality in the organization and the 
                results of these efforts to the community.''')
    
    with sp13_col2:
        
        sp1_q3 = st.selectbox('', options = ['', 'Yes', 'No'], key='sp1_q3')
  
    st.markdown('''----''')
    
    sp14_col1, sp14_col2 = st.columns([2,1])    

    with sp14_col1:    
                   
        st.write('''4) All staff and independent practitioners were made aware of ongoing efforts to 
                 reduce risks and hazards and to improve patient safety and quality in the organization.''')
    
    with sp14_col2:   
              
          sp1_q4 = st.selectbox('', options = ['', 'Yes', 'No'], key='sp1_q4')

    st.markdown('''----''')
    
    st.write('''*Within the last 24 months, in regard to holding the board, senior administrative leadership, midlevel management, 
             nursing leadership, physician leadership, and frontline caregivers directly accountable for results related to identifying and 
             reducing unsafe practices, the organization has done the following:*''')   

    sp15_col1, sp15_col2 = st.columns([2,1]) 

    with sp15_col1:
          
        st.write('''5) An integrated patient safety program has been in place for the entire reporting period, providing oversight and alignment 
                of safe practice activities.''')

    with sp15_col2:  
               
          sp1_q5 = st.selectbox('', options = ['', 'Yes', 'No'], key='sp1_q5')

    st.markdown('''----''')
    
    sp16_col1, sp16_col2 = st.columns([2,1]) 

    with sp16_col1: 
        
        st.write('''6) A Patient Safety Officer (PSO) has been apscoreed and communicates regularly with the board (governance) and senior 
                administrative leadership; the PSO is the primary score of contact of the integrated patient safety program.''')
    
    with sp16_col2: 
              
          sp1_q6 = st.selectbox('', options = ['', 'Yes', 'No'], key='sp1_q6')

    st.markdown('''----''')
    
    sp17_col1, sp17_col2 = st.columns([2,1]) 

    with sp17_col1: 
        
        st.write('''Performance has been documented in performance reviews and/or compensation incentives for all levels of hospital 
                 management and hospital-employed caregivers noted above.''')
    
    with sp17_col2: 
           
          sp1_q7 = st.selectbox('', options = ['', 'Yes', 'No'], key='sp1_q7')    

    st.markdown('''----''')
    
    sp18_col1, sp18_col2 = st.columns([2,1]) 

    with sp18_col1:  
        
        st.write('''The interdisciplinary patient safety team communicated regularly with senior administrative leadership 
                 regarding both of the following and documented these communications in meeting minutes:   
                - progress in meeting safety goals; and  
                - provide team training to caregivers.''')

    with sp18_col2:  
          
          sp1_q8 = st.selectbox('', options = ['', 'Yes', 'No'], key='sp1_q8')   

    st.markdown('''----''')
     
    sp19_col1, sp19_col2 = st.columns([2,1]) 

    with sp19_col1:
        
        st.write('''The hospital reported adverse events to external mandatory or voluntary programs.''')
    
    with sp19_col2: 
          
          sp1_q9 = st.selectbox('', options = ['', 'Yes', 'No'], key='sp1_q9') 

    st.markdown('''----''')
    
    st.write('''*Within the last 24 months, in regard to implementation of the patient safety program, 
             the board (governance) and senior administrative leadership have provided resources to 
             cover the implementation as evidenced by:*''')    

    sp110_col1, sp110_col2 = st.columns([2,1]) 

    with sp110_col1:
        
        st.write('''Dedicated patient safety program budgets that support the program, staffing, and technology investment.''')
    
    with sp110_col2:     
        
        sp1_q10 = st.selectbox('', options = ['', 'Yes', 'No'], key='sp1_q10') 

    st.markdown('''----''')
    
    st.write('''*Within the last 24 months, structures and systems have been in place to ensure that senior administrative leadership is taking direct action, as evidenced by:*''') 
    
    sp111_col1, sp111_col2 = st.columns([2,1]) 
    
    with sp111_col1:
        
        st.write('''CEO and senior administrative leadership are personally engaged in reinforcing patient safety improvements, 
                 e.g., “walk-arounds,” and reporting to the board (governance). Calendars reflect allocated time.''')
        
    with sp111_col2:  
        
        sp1_q11 = st.selectbox('', options = ['', 'Yes', 'No'], key='sp1_q11')       
     
    st.markdown('''----''')
    
    sp112_col1, sp112_col2 = st.columns([2,1])   
     
    with sp112_col1:
        
         st.write('''CEO has actively engaged leaders from service lines, midlevel management, nursing leadership, and physician leadership in patient safety improvement actions.''')
        
    with sp112_col2:    
        
        sp1_q12 = st.selectbox('',  options = ['', 'Yes', 'No'], key='sp1_q12')       

    st.markdown('''----''')
    
    sp113_col1, sp113_col2 = st.columns([2,1]) 
    
    with sp113_col1:
        
        st.write('''Hospital has established a structure for input into the patient safety program by licensed independent practitioners and 
                 the organized medical staff and physician leadership. Input documented in meeting minutes or materials.''')
    
    with sp113_col2:
        
        sp1_q13 = st.selectbox('', options = ['', 'Yes', 'No'], key='sp1_q13')

    st.markdown('''----''') 
    
    #%% begin SP 1 Calculations
    if st.button('Calculate SP 1'):
    
        #section timestamp
        sp1_timestamp = datetime.now().strftime('%m-%d-%Y %H:%M %p')
        
        # st.write("The length of sp1 is: ",len())
        sp1_bank = [st.session_state.sp1_q1, st.session_state.sp1_q2, st.session_state.sp1_q3, 
                    st.session_state.sp1_q4, st.session_state.sp1_q5, st.session_state.sp1_q6, 
                    st.session_state.sp1_q7, st.session_state.sp1_q8, st.session_state.sp1_q9, 
                    st.session_state.sp1_q10, st.session_state.sp1_q11, st.session_state.sp1_q12, 
                    st.session_state.sp1_q13]
    
        sp1_max_points = 120
        
        # scores per question
        sp1_scores_per_question = round((sp1_max_points/len(sp1_bank)-1), 2)
    
        @st.cache
        def sp1_get_leapfrog_points():
            """Calculate SP1 Leapfrog points."""
            leapfrog_points = 0
    
            for sp in sp1_bank:
                if sp == "Yes":
                    leapfrog_points = leapfrog_points + sp1_scores_per_question
                else:
                    leapfrog_points = leapfrog_points
            return round(leapfrog_points, 2)
    
        # Calling the function and storing the value to a variable
        sp1_leapfrog_points = sp1_get_leapfrog_points()
        # st.write("The leapfrog points for sp1 is: ",sp1_leapfrog_points)
    
        st.session_state['SP 1'] = sp1_leapfrog_points
        
        st.markdown('''----''') 
        
        #display points
        sp1_points_col1, sp1_points_col2 = st.columns(2)
        
        with sp1_points_col1:
            st.write('Score')

        with sp1_points_col2:
            st.write('Points')
            
            #replace with N/A for revealing the points only*
            if sp1_leapfrog_points == -1:
                 st.success('N/A')
                 
            else:
                st.success(sp1_leapfrog_points)
    
    st.markdown("[Return to Top - SP 1](#sp-1)", unsafe_allow_html=True)
      
st.markdown('''---''')

#%% SP 2
st.header('Safe Practice 2 (SP 2)')
 
with st.expander(''):

    st.write('''*Within the last 36 months, in regard to culture measurement, our organization has 
             done the following:*''')
    
    sp21_col1, sp21_col2 = st.columns([2,1])

    with sp21_col1: 

        st.write('''1) Conducted a culture of safety survey of our employees using a nationally recognized tool that has demonstrated validity, 
                 consistency, and reliability. The units surveyed account for at least 50% of the aggregated care delivered to patients within 
                 the hospital and include the high patient safety risk units or departments.''')

    with sp21_col2:
        
        sp2_q1 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp2_q1')

    st.markdown('''----''')

    sp22_col1, sp22_col2 = st.columns([2,1])   

    with sp22_col1:    
        
        st.write('''2) Portrayed the results of the culture of safety survey in a report, which reflects both hospital-wide and individual unit level 
                 results, as applicable.''')
            
    with sp22_col2:
        
        sp2_q2 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp2_q2')        

    st.markdown('''----''')
    
    sp23_col1, sp23_col2 = st.columns([2,1])    
    
    with sp23_col1:
        
        st.write('''3) Benchmarked results of the culture of safety survey against external organizations, 
                 such as “like” hospitals or other hospitals within the same health system.''')
    
    with sp23_col2:
        
        sp2_q3 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp2_q3')

    st.markdown('''----''')
    
    sp24_col1, sp24_col2 = st.columns([2,1])  
    
    with sp24_col1:
        
        st.write('''4) Compared results of the culture of safety surveys across roles and staff levels.''')
    
    with sp24_col2:
        
        sp2_q4 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp2_q4')

    st.markdown('''----''')
    
    sp25_col1, sp25_col2 = st.columns([2,1])  
    
    with sp25_col1:
        
        st.write('''5) Service line, midlevel managers, or senior administrative leaders used the results of the culture of safety survey to 
                debrief at the relevant unit level, using semi-structured approaches for the debriefings and presenting results in aggregate 
                form to ensure the anonymity of survey respondents.''')

    with sp25_col2:
        
        sp2_q5 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp2_q5')
    
    st.markdown('''----''')
    
    st.write('''*Within the last 36 months, in regard to accountability for improvements in culture measurement, our organization has done the following:*''')
                    
    sp26_col1, sp26_col2 = st.columns([2,1])

    with sp26_col1:

        st.write('''1) Shared the results of the culture of safety survey with the board (governance) and senior administrative 
                    leadership in a formal report and discussion.''')

    with sp26_col2:
        
        sp2_q6 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp2_q6')

    st.markdown('''----''')

    sp27_col1, sp27_col2 = st.columns([2,1])

    with sp27_col1:
        
        st.write('''2) Included in performance evaluation criteria for senior administrative leadership both the response rates 
                    to the culture of safety survey and the use of the culture of safety survey results in the improvement efforts.''')

    with sp27_col2:
        
        sp2_q7 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp2_q7')

    st.markdown('''----''')

    st.write('''*Within the last 24 months, in regard to culture measurement, the organization has done the 
             following (or has had the following in place):*''')
                    
    sp28_col1, sp28_col2 = st.columns([2,1])

    with sp28_col1:

        st.write('''1) Conducted staff education program(s) on methods to improve the culture of safety, 
                 tailored to the organization’s culture of safety survey results.''')

    with sp28_col2:
        
        sp2_q8 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp2_q8')

    st.markdown('''----''')

    sp29_col1, sp29_col2 = st.columns([2,1])
    
    with sp29_col1:
        
        st.write('''2) Included the costs of annual culture measurement/follow-up activities in the patient safety program budget''')

    with sp29_col2:
        
        sp2_q9 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp2_q9')

    st.markdown('''----''')

    st.write('''*Within the last 24 months, in regard to culture measurement, feedback, and interventions, 
             our organization has done the following (or has had the following in place):*''')
                    
    sp210_col1, sp210_col2 = st.columns([2,1])
    
    with sp210_col1:

        st.write('''1) Developed or implemented explicit, hospital-wide organizational policies and procedures for regular culture measurement.''')

    with sp210_col2:
        
        sp2_q10 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp2_q10')

    st.markdown('''----''')

    sp211_col1, sp211_col2 = st.columns([2,1])
    
    with sp211_col1:
        
        st.write('''2) Disseminated the results of the culture of safety survey widely across the institution, 
                    and senior administrative leadership held follow-up meetings with the sampled units to discuss 
                    the unit’s results and concerns.''')

    with sp211_col2:
        
        sp2_q11 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp2_q11')

    st.markdown('''----''')

    sp212_col1, sp212_col2 = st.columns([2,1])
    
    with sp212_col1:
        
        st.write('''3) Identified performance improvement interventions based on the culture of safety survey results, 
                    which were shared with senior administrative leadership and subsequently measured and monitored.''')

    with sp212_col2:
        
        sp2_q12 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp2_q12')

    st.markdown('''----''')

    #%% Begin SP 2 Calculations
    if st.button('Calculate SP 2'):
        
        #section timestamp
        sp2_timestamp = datetime.now().strftime('%m-%d-%Y %H:%M %p')
        
        sp2_bank = [st.session_state.sp2_q2, st.session_state.sp2_q3, st.session_state.sp2_q4,     
                    st.session_state.sp2_q5, st.session_state.sp2_q6, st.session_state.sp2_q7, 
                    st.session_state.sp2_q8, st.session_state.sp2_q9,
                    st.session_state.sp2_q10, st.session_state.sp2_q11, st.session_state.sp2_q12]
        
        sp2_max_points = 120
    
        # scores per question
        sp2_scores_per_question = round((sp2_max_points/len(sp2_bank)), 2)
        # st.write("The scores per question for sp2 is : ",sp2_scores_per_question)
    
        @st.cache
        def sp2_get_leapfrog_points():
            """Calculate SP2 Leapfrog points."""
            leapfrog_points = 0
    
            for sp in sp2_bank:
                if sp == "Yes":
                    leapfrog_points = leapfrog_points + sp2_scores_per_question
                else:
                    leapfrog_points = leapfrog_points
            return round(leapfrog_points, 2)
    
        # Calling the function and storing the value to a variable
        sp2_leapfrog_points = sp2_get_leapfrog_points()
        # st.write("The leapfrog points for sp2 is: ",sp2_leapfrog_points)
    
        st.session_state['SP 2'] = sp2_leapfrog_points
                
        st.markdown('''----''') 
    
        #display points
        sp2_points_col1, sp2_points_col2 = st.columns(2)
        
        with sp2_points_col1:
            st.write('Score')

            #st.success(sp1_survey_scores)
        
        with sp2_points_col2:
            st.write('Points')
            
            #replace with N/A for revealing the points only*
            if sp2_leapfrog_points == -1:
                 st.success('N/A')
                 
            else:
                st.success(sp2_leapfrog_points)
    
    st.markdown("[Return to Top - SP 2](#sp-2)", unsafe_allow_html=True)
       
st.markdown('''----''')

#%% SP9
st.header('Safe Practice 9 (SP 9)')

with st.expander(''):

    sp9_col1, sp9_col2 = st.columns([2,1])

    with sp9_col1:
        
        st.write('''Is your hospital currently recognized as an American Nurses Credentialing Center (ANCC) Magnet® organization?''')
        
    with sp9_col2:  
        
        sp9_q0 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q0')

    st.info('''*If Yes, your hospital will receive full credit for this Safe Practice and 
        no additional boxes need to be checked. If No, please answer all of the boxes that apply*.''')

    st.markdown('''---''')
    
    if sp9_q0 != 'Yes':
    
        st.markdown('''*Within the last 24 months, in regard to ensuring adequate and competent nursing staff 
                 service and nursing leadership at all levels, our organization has done the following (or has 
                 had the following in place)*:''')
    
        sp91_col1, sp91_col2 = st.columns([2,1])  
        
        with sp91_col1:    
            
            st.write('''1) Held at least one educational meeting for senior administrative leadership, nursing 
                    leadership, midlevel management and service line management specifically related to the impact 
                    of nursing on patient safety.''')
        
        with sp91_col2:
            
            sp9_q1 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q1')

        st.markdown('''---''')
        
        sp92_col1, sp92_col2 = st.columns([2,1])  
        
        with sp92_col1:
            
            st.write('''2) Performed a risk assessment that includes a hospital-wide evaluation of the frequency 
                    and severity of adverse events that can be related to nurse staffing.''')
        
        with sp92_col2:
            
            sp9_q2 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q2')

        st.markdown('''---''')
    
        sp93_col1, sp93_col2 = st.columns([2,1]) 
        
        with sp93_col1:
            
            st.write('''3) Submitted a report to the board (governance) with recommendations for measurable improvement targets.''')
            
        with sp93_col2:
            
            sp9_q3 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q3')

        st.markdown('''----''')
        
        sp94_col1, sp94_col2 = st.columns([2,1]) 
        
        with sp94_col1:
            
            st.write('''4) Collected and analyzed data of actual unit-specific nurse staffing levels on a quarterly basis to identify and address potential patient safety-related staffing issues.''')
    
        with sp94_col2:
            
            sp9_q4 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q4')

        st.markdown('''---''')
        
        sp95_col1, sp95_col2 = st.columns([2,1]) 
        
        with sp95_col1:
            
            st.write('''6) Provided unit-specific reports of potential patient safety-related staffing issues to 
                    senior nursing leadership, senior administrative leadership and the board (governance) at 
                    least quarterly.''')
        
        with sp95_col2:
            
            sp9_q5 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q5')
 
        st.markdown('''---''')
    
        st.markdown('''*Within the last 24 months, in regard to ensuring adequate and competent nursing staff 
                     service and nursing leadership at all levels, our organization has done the following 
                     (or has had the following in place)*:''')
        
        sp96_col1, sp96_col2 = st.columns([2,1]) 
    
        with sp96_col1:		
            
            st.write('''1) Held nursing leadership directly accountable for improvements in performance through performance reviews or compensation.''')
          
        with sp96_col2:
            
            sp9_q6 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q6')  

        st.markdown('''---''')
        
        sp97_col1, sp97_col2 = st.columns([2,1]) 
    
        with sp97_col1:	
	        
            st.write('''2) Included nursing leadership as part of the hospital senior administrative leadership team.''')
        
        with sp97_col2:
            
            sp9_q7 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q7') 

        st.markdown('''---''')
        
        sp98_col1, sp98_col2 = st.columns([2,1])
        
        with sp98_col1:
            
            st.write('''3) Reported performance metrics related to this Safe Practice to the board (governance).''') 	
        
        with sp98_col2:
            
            sp9_q8 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q8')  
  
        st.markdown('''---''')
            
        sp99_col1, sp99_col2 = st.columns([2,1])
        
        with sp99_col1:
            
            st.write('''4) Held the board (governance) and senior administrative leadership accountable for the 
                    provision of financial resources to ensure adequate nurse staffing levels.''')
        
        with sp99_col2:
            
            sp9_q9 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q9') 
   
        st.markdown('''----''')
        
        st.markdown('''*Within the last 24 months, in regard to ensuring adequate and competent nursing staff service and
                 nursing leadership at all levels, our organization has done the following (or has had the following in place)*:''')
        
        sp910_col1, sp910_col2 = st.columns([2,1])
        
        with sp910_col1:
            
            st.write('''1) Conducted staff education on maintaining and improving competencies specific to assigned job duties 
                    related to the safety of the patient, with attendance documented.''')
        
        with sp910_col2:
            
            sp9_q10 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q10') 

        st.markdown('''----''')
        
        sp911_col1, sp911_col2 = st.columns([2,1])
        
        with sp911_col1:
            
            st.write('''2) Allocated protected time for direct care staff and managers to reduce adverse events related to 
                    staffing levels or competency issues.''')
        
        with sp911_col2:
            
            sp9_q11 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q11') 
  
        st.markdown('''----''')
        
        sp912_col1, sp912_col2 = st.columns([2,1])
        
        with sp912_col1:
            
            st.write('''3) Documented expenses incurred during the reporting period that are tied to quality improvement 
                    efforts around this Safe Practice.''')
        
        with sp912_col2:
            
            sp9_q12 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q12')    

        st.markdown('''----''')
        
        sp913_col1, sp913_col2 = st.columns([2,1])
        
        with sp913_col1:
            
            st.write('''4) Budgeted financial resources for balancing staffing levels and skill levels to improve performance.''')
        
        with sp913_col2:
            
             sp9_q13 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q13')    

        st.markdown('''----''')
        
        sp914_col1, sp914_col2 = st.columns([2,1])  
          
        with sp914_col1:
            
            st.write('''5) Board (governance) has approved a budget for reaching optimal nurse staffing.''')
        
        with sp914_col2:
            
            sp9_q14 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q14')    

        st.markdown('''----''')
        
        st.markdown('''*Within the last 24 months, in regard to ensuring adequate and 
                 competent nursing staff service and nursing leadership 
                 at all levels, our organization has done the following (or has had 
                 the following in place with regular updates)*:''')   
        
        sp915_col1, sp915_col2 = st.columns([2,1])  
        
        with sp915_col1:
            
            st.write('''1) Implemented a staffing plan, with input from nurses, 
                     to ensure that adequate nursing staff-to-patient ratios are achieved.''')
        
        with sp915_col2:
            
            sp9_q15 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q15')   
      
        st.markdown('''----''')   
    
        sp916_col1, sp916_col2 = st.columns([2,1])     
        
        with sp916_col1:
            
            st.write('''2) Developed policies and procedures for effective staffing targets that specify number, competency and skill mix of nursing staff.''')
        
        with sp916_col2:
            
             sp9_q16 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q16')   

        st.markdown('''----''')    
        
        sp917_col1, sp917_col2 = st.columns([2,1])
        
        with sp917_col1:
            
            st.write('''3) Implemented a performance improvement program that minimizes the risk to patients from less-than-optimal staffing 
                     levels OR monitored a previously implemented hospital-wide performance improvement program that measures, and demonstrates 
                     full achievement of, the impact of this specific Safe Practice.''')
        
        with sp917_col2:
            
             sp9_q17 = st.selectbox('', options = ['', 'Yes', 'No'], key = 'sp9_q17')

        st.markdown('''---''')
    
    #%% SP 1 Calculations
    if st.button('Calculate SP 9'):
        
        #section timestamp
        sp9_timestamp = datetime.now().strftime('%m-%d-%Y %H:%M %p')
        
        #If q0 is Yes, SP9 is Achieved the Standard and the points is 100 
        if 'Yes' not in sp9_q0: 
            
            scores_per_question = 100/17
        
            sp9_answers = [st.session_state.sp9_q1, st.session_state.sp9_q2, st.session_state.sp9_q3, 
                           st.session_state.sp9_q4, st.session_state.sp9_q5, st.session_state.sp9_q6,
                           st.session_state.sp9_q7, st.session_state.sp9_q8, st.session_state.sp9_q9, 
                           st.session_state.sp9_q10, st.session_state.sp9_q11, st.session_state.sp9_q12,
                           st.session_state.sp9_q13, st.session_state.sp9_q14, st.session_state.sp9_q15, 
                           st.session_state.sp9_q16, st.session_state.sp9_q17]
    
            #max possible points
            sp9_max_points = 100
            
            #value of each answer
            #max points divided by the length of questions less 1
            sp9_scores_per_question = sp9_max_points/(len(sp9_answers)-1)
            
            # count number of Yes answers
            sp9_yeses = sum(['Yes' in s for s in sp9_answers])
        
            #-----------------------------------------------------------------#
            #MAIN LOGIC
    
            sp9_survey_points = round(sp9_yeses*scores_per_question,2)
    
            #if points is 100, Achieved
            if sp9_survey_points == 100:
                sp9_survey_scores = 'Achieved the Standard'
             
            #if points is greater than or equal to 80 but less than 100, Considerable
            elif (sp9_survey_points < 100) & (sp9_survey_points >= 80):
                sp9_survey_scores = 'Considerable Achievement'
             
            #if points is greater than or equal to 50 but less than 80, Some
            elif (sp9_survey_points < 80) & (sp9_survey_points >= 50):
                sp9_survey_scores = 'Some Achievement'
             
            #if points is less than 50, Limited
            elif sp9_survey_points < 50:
                sp9_survey_scores = 'Limited Achievement'
    
            else:
                sp9_survey_scores = 'Unable to Calculate points'
                sp9_survey_scores = nan
                    
        elif 'Yes' in sp9_q0: 
            sp9_survey_scores = 'Achieved the Standard'
            sp9_survey_points = 100
    
        else:
            sp9_survey_scores = 'Unable to Calculate points'
            sp9_survey_scores = -1
            
        st.session_state['SP 9'] = sp9_survey_points

        st.markdown('''----''') 
        
        #display points
        sp9_points_col1, sp9_points_col2 = st.columns(2)
        
        with sp9_points_col1:
            st.write('Score')
            st.success(sp9_survey_scores)
        
        with sp9_points_col2:
            st.write('Points')
            
            #replace with N/A for revealing the points only*
            if sp9_survey_points == -1:
                 st.success('N/A')
                 
            else:
                st.success(sp9_survey_points)
    
    st.markdown("[Return to Top - SP 9](#sp-9)", unsafe_allow_html=True)
     
st.markdown('''---''')

#%% Hand Hygiene
st.header('Hand Hygiene')

with st.expander(''):

    hh1_col1, hh1_col2 = st.columns([2,1])

    with hh1_col1:
        
        st.markdown('''1) Do individuals who touch patients or who touch items that will be used by patients in your 
                    patient care units receive hand hygiene training from a professional with appropriate training and 
                    skills at both:  
                    - The time of onboarding; and  
                    - Annually thereafter?  
                   ''')
    
    with hh1_col2:
        
            hh_q1 = st.selectbox('', options = ['', 'Yes', 'No'], key='hh_q1') 

    st.info('''*If No to question #1, skip questions #2-3 and continue on to question #4.*''')
    
    st.markdown('''---''')
    
    if hh_q1 != 'No':
        
        hh2_col1, hh2_col2 = st.columns([2,1])
        
        with hh2_col1:
            
            st.write('''2) In order to pass the initial hand hygiene training, do individuals who touch patients 
                     or who touch items that will be used by patients in your patient care units need to 
                     physically demonstrate proper hand hygiene with soap and water and alcohol-based hand sanitizer?''')
                     
        with hh2_col2:
            
            hh_q2 = st.selectbox('', options = ['', 'Yes', 'No'], key='hh_q2') 

        st.markdown('''---''')
        
        hh3_col1, hh3_col2 = st.columns([2,1])
        
        with hh3_col1:
            
            st.write('''3) Are all six of the following topics included in your hospital’s initial and annual hand hygiene training?  
                        - Evidence linking hand hygiene and infection prevention  
                        - When individuals who touch patients or who touch items that will be used by patients should perform hand hygiene 
                        (e.g., WHO's 5 Moments for Hand Hygiene, CDC’s Guideline for Hand Hygiene)  
                        - How individuals who touch patients or who touch items that will be used by patients should clean their hands with 
                        alcohol-based hand sanitizer and soap and water as to ensure they cover all surfaces of hands and fingers, including thumbs and fingernails''')
        
        with hh3_col2:
            
            hh_q3 = st.selectbox('', options = ['', 'Yes', 'No'], key='hh_q3') 
   
        st.markdown('''---''')
    
    else:
        
        hh_q2 = ''
        st.session_state.hh_q2 = hh_q2
        
        hh_q3 = ''
        st.session_state.hh_q3 = hh_q3
        
    
    hh4_col1, hh4_col2 = st.columns([2,1])
    
    with hh4_col1:
     
        st.write('''4) Does your hospital have a process in place to ensure that all of the following are done, as necessary, and quarterly audits are conducted on a sample of dispensers in your patient care units to ensure 
                that the process is followed?  
                - Refill paper towels, soap dispensers, and alcohol-based hand sanitizer dispensers when they are empty or near empty  
                - Replace batteries in automated paper towel dispensers, soap dispensers, and alcohol-based hand sanitizer dispensers 
                (if automated dispensers are used in the patient care units)''')

    with hh4_col2:
        
        hh_q4 = st.selectbox('', options = ['','Yes', 'No'], key='hh_q4')
     
    st.markdown('''---''')
    
    hh5_col1, hh5_col2 = st.columns([2,1])
    
    with hh5_col1:
        
        st.write('''5) Do all rooms and bed spaces in your patient care units have:  
                - An alcohol-based hand sanitizer dispenser located at the entrance to the room or bed space; and  
                - Alcohol-based hand sanitizer dispenser(s) located inside the room or bed space that are equally accessible to the location of all patients in the room or bed space?''')

    with hh5_col2:
        
        hh_q5 = st.selectbox('', options = ['','Yes', 'No'], key='hh_q5')
     
    st.markdown('''---''')
    
    hh6_col1, hh6_col2 = st.columns([2,1])
    
    with hh6_col1:
        
        st.write('''6) Does your hospital conduct audits of the volume of alcohol-based hand sanitizer 
                 that is delivered with each activation of a wall-mounted dispenser (manual and automated) 
                on a sample of dispensers in your patient care units at all of the following times:  
                    - Upon installation;     
                    - Whenever the brand of product or system changes; and   
                    - Whenever adjustments are made to the dispensers  
                    - OR Has your hospital conducted an audit of the volume of alcohol-based hand sanitizer 
                that is delivered with each activation of a wall-mounted dispenser (manual and automated) on a 
                sample of your hospital’s existing dispensers if there have been no recent changes to any dispensers?
              ''')
                
    with hh6_col2:
        
        hh_q6 = st.selectbox('', options = ['','Yes', 'No', 'Does not apply, wall-mounted dispensers are not used'], key='hh_q6')

    st.info('''*If No or does not apply, wall-mounted dispensers are not used, skip question #7 and continue on to question #8.*''')

    st.markdown('''---''')
    
    if 'Yes' in hh_q6:
    
        hh7_col1, hh7_col2 = st.columns([2,1])  
        
        with hh7_col1:
            
            st.write('''7) Do all of the audited dispensers deliver, with one activation, a volume of alcohol-based hand sanitizer that covers the hands completely 
                     and requires 15 or more seconds for hands to dry (on average)?''')
                     
        with hh7_col2:
            
            hh_q7 = st.selectbox('', options = ['','Yes', 'No'], key='hh_q7')

        st.markdown('''---''')
    
    else:
        
        hh_q7 = ''
        st.session_state.hh_q7 = hh_q7
    
    hh8_col1, hh8_col2 = st.columns([2,1]) 
    
    with hh8_col1:
        
        st.write('''8) Does your hospital collect hand hygiene compliance data on at least 200 hand hygiene opportunities, or at least the number of hand hygiene 
                 opportunities outlined based on the unit type in Tables 1-3, each month in each patient care unit? ''')
    
    with hh8_col2:
        
        hh_q8 = st.selectbox('', 
                             options = ['',
                                        'Yes, using an electronic compliance monitoring system',
                                        'Yes, using an electronic compliance monitoring system throughout some patient care units and only direct observation in all other patient care units',
                                        'Yes, using only direct observation throughout all patient care units',
                                        'No'], 
                             key='hh_q8')

    st.info('''*If Yes to question #8, skip question #9 and continue on to question #10.*''')
    
    st.markdown('''---''')
    
    if 'Yes' not in hh_q8:
    
        hh9_col1, hh9_col2 = st.columns([2,1]) 
        
        with hh9_col1:
            
            st.write('''9) Does your hospital collect hand hygiene compliance data on at least 100 hand 
                 hygiene opportunities each quarter in each patient care unit?''')
        
        with hh9_col2:
            
            hh_q9 = st.selectbox('', 
                                 options = ['',
                                            'Yes, using an electronic compliance monitoring system',
                                            'Yes, using an electronic compliance monitoring system throughout some patient care units and only direct observation in all other patient care units',
                                            'Yes, using only direct observation throughout all patient care units',
                                            'No'], 
                                 key='hh_q9')

        st.info('''*If No to question #9, skip questions #10-18 and continue on to question #19.*''')

        st.markdown('''---''')
   
    else:
        hh_q9 = ''
        st.session_state.hh_q9 = hh_q9
    
    if hh_q9 != 'No':
 
        hh10_col1, hh10_col2 = st.columns([2,1]) 
        
        with hh10_col1:
            
            st.write('''10) Does your hospital use hand hygiene coaches or compliance observers to 
                 provide individuals who touch patients or who touch items that will be used by patients
                 in your patient care units with feedback on both when they are and are not compliant with performing hand hygiene?''')  
       
        with hh10_col2:
            
            hh_q10 = st.selectbox('', options = ['','Yes', 'No'], key='hh_q10')

        st.markdown('''---''')
        
        hh11_col1, hh11_col2 = st.columns([2,1]) 
        
        with hh11_col1:
            
            st.write('''11) In those patient care units where an electronic compliance monitoring system 
                 is used, does the monitoring system used meet both of the following criteria? 
                 - The system can identify both opportunities for hand hygiene and that hand hygiene 
                 was performed  
                 - The hospital itself has validated the accuracy of the data collected by the electronic 
                 compliance monitoring system''')
     
        with hh11_col2:
            
            hh_q11 = st.selectbox('', options = ['','Yes', 'No'], key='hh_q11')

        st.markdown('''---''')
        
        hh12_col1, hh12_col2 = st.columns([2,1]) 
        
        with hh12_col1:
            
            st.write('''12) In those patient care units where an electronic compliance monitoring system 
                 is used, are direct observations also conducted for coaching and intervention purposes 
                 that meet all of the following criteria?  
                 - Observers immediately intervene prior to any harm occurring to provide non-compliant 
                 individuals with immediate feedback  
                 - Observations identify both opportunities for hand hygiene and compliance with 
                 those opportunities  
                 - Observations determine who practiced hand hygiene, verify when they practiced it, 
                 and whether their technique was correct  
                 - Observations within a unit are conducted weekly or monthly across all shifts and on 
                 all days of the week proportional to the number of individuals who touch patients or who 
                 touch items that will be used by 
                 patients on duty for that shift  
                 - Observations capture a representative sample of the different roles of individuals 
                 who touch patients or who touch items that will be used by patients (e.g., nurses, 
                physicians, techs, environmental services workers)''')
     
        with hh12_col2:
            
            hh_q12 = st.selectbox('', options = ['','Yes', 'No'], key='hh_q12')

        st.markdown('''---''')
        
        hh13_col1, hh13_col2 = st.columns([2,1]) 
        
        with hh13_col1:
            
            st.write('''13) In those patient care units where an electronic compliance monitoring system 
                 is NOT used, do the direct observations meet all of the following criteria?  
                 - Observations identify both opportunities for hand hygiene and compliance with 
                 those opportunities  
                 - Observations determine who practiced hand hygiene, verify when they practiced it, 
                 and whether their technique was correct  
                 - Observations within a unit are conducted weekly or monthly across all shifts and on 
                 all days of the week proportional to the number of individuals who touch patients or who 
                 touch items that will be used by patients on duty 
                 for that shift
                 - Observations are conducted to capture a representative sample of the different roles 
                 of individuals who touch patients or who touch items that will be used by patients 
                 (e.g., nurses, physicians, techs, environmental services workers)''')
            
        with hh13_col2:
            
            hh_q13 = st.selectbox('', options = ['','Yes', 'No'], key='hh_q13')

        st.markdown('''---''')
        
        hh14_col1, hh14_col2 = st.columns([2,1]) 
        
        with hh14_col1:
            
            st.write('''14) Does your hospital have a system in place for both the initial and recurrent training and validation of hand hygiene compliance observers?''')
        
        with hh14_col2:
            
            hh_q14 = st.selectbox('', options = ['','Yes', 'No'], key='hh_q14')

        st.markdown('''---''')
        
        hh15_col1, hh15_col2 = st.columns([2,1]) 
        
        with hh15_col1:
            
            st.write('''15) Are unit-level hand hygiene compliance data fed back to individuals who touch 
                 patients or who touch items that will be used by patients at least monthly for improvement work?''')
                 
        with hh15_col2:
            
            hh_q15 = st.selectbox('', options = ['','Yes', 'No'], key='hh_q15')
 
        st.markdown('''---''')
        
        hh16_col1, hh16_col2 = st.columns([2,1]) 
        
        with hh16_col1:
            
            st.write('''16) Are unit-level hand hygiene compliance data used for creating unit-level action plans?''')
      
        with hh16_col2:
            
            hh_q16 = st.selectbox('', options = ['','Yes', 'No'], key='hh_q16')
  
        st.markdown('''---''')
        
        hh17_col1, hh17_col2 = st.columns([2,1]) 
        
        with hh17_col1:
            
            st.write('''17) Is regular (at least every 6 months) feedback of hand hygiene compliance data, 
                 with demonstration of trends over time, given to:   
                - Senior administrative leadership, physician leadership, and nursing leadership;  
                - The board (governance); and  
                - The medical executive committee?  
                ''')
        
        with hh17_col2:
            
            hh_q17 = st.selectbox('', options = ['','Yes', 'No'], key='hh_q17')
 
        st.info('''*If No to question #17, skip question #18 and continue on to question #19.*''')
        
        st.markdown('''---''')
        
        if hh_q17 == 'Yes':
        
            hh18_col1, hh18_col2 = st.columns([2,1]) 
            
            with hh18_col1:
                
                st.write('''18) If Yes to question #17, is senior administrative leadership, physician leadership, 
                     and nursing leadership held directly accountable for hand hygiene performance through 
                     performance reviews or compensation?''')
           
            with hh18_col2:
                
                hh_q18 = st.selectbox('', options = ['','Yes', 'No'], key='hh_q18')

            st.markdown('''---''')
        
        elif hh_q17 == '':
            
            hh_q18 = ''
            st.session_state.hh_q18 = hh_q18

    hh19_col1, hh19_col2 = st.columns([2,1]) 
    
    with hh19_col1:
        
        st.write('''19) Are patients and visitors invited to remind individuals who touch patients or 
             who touch items that will be used by patients to perform hand hygiene?''')
             
    with hh19_col2:    
        
        hh_q19 = st.selectbox('', options = ['','Yes', 'No'], key='hh_q19')

    st.markdown('''---''')
    
    hh20_col1, hh20_col2 = st.columns([2,1]) 
    
    with hh20_col1:
        
        st.write('''20) Have all of the following individuals (or their equivalents) demonstrated a 
             commitment to support hand hygiene improvement in the last year (e.g., a written or 
            verbal commitment delivered to those individuals who touch 
            patients or who touch items that will be used by patients?  
            - Chief Executive Officer    
            - Chief Medical Officer    
            - Chief Nursing Officer''')  
    
    with hh20_col2:
        
        hh_q20 = st.selectbox('', options = ['','Yes', 'No'], key='hh_q20')

    st.markdown('''---''')
    
    if st.button('Calculate Hand Hygiene'):
        
        #section timestamp
        hh_timestamp = datetime.now().strftime('%m-%d-%Y %H:%M %p')

        #-----------------------------------------------------------------#
        # Variables to make logic more concise
        
        #training and education domain section
        train_edu = sum(['Yes' in t for t in [hh_q1, hh_q2, hh_q3]]) #sum of 3
        
        #infrastructure domain section
        infra = sum(['Yes' in i for i in [hh_q4, hh_q5, hh_q6, hh_q7]]) #sum of 4
        
        #monitoring domain section
        monitoring = sum(['Yes' in a for a in [hh_q8, hh_q9, hh_q10]]) #sum 3
        
        #electronic compliance monitoring section
        electronic = sum(['Yes' in e for e in [hh_q11, hh_q12]]) #sum of 2
        
        #direct observation questions
        direct = sum(['Yes' in d for d in [hh_q13, hh_q14]]) #sum of 2
        
        #feedback domain section
        feedback = sum(['Yes' in f for f in [hh_q15, hh_q16, hh_q17, hh_q18]]) #sum of 4
        
        #culture domain section
        culture = sum(['Yes' in c for c in [hh_q19, hh_q20]]) #sum of 2
        
        #count to be applied to the 'Some Achievement' and 'Limited Achievement' scoring
        some_count = sum([monitoring == 3, #monitoring should have 3 Yes answers
                         electronic == 2,  #electronic should have 2 Yes answers
                         direct == 2, #direct should have 2 Yes answers
                         feedback == 4, #feedback should have 4 Yes answers
                         train_edu == 3, #training and education should have 3 Yes answers
                         infra == 4, #infrastructure should have 4 Yes answers
                         culture == 2]) #Culture should have 2 Yes answers
        
        #-----------------------------------------------------------------#
        # LOGIC
        
        #if monitoring has 3 Yes answers, electronic and direct have 2 Yes answers each, feedback has 4 answers,
        # and there are at least 5 Yes answers from training/education + infrastructure + culture
        if (monitoring == 3) & (electronic == 2) & (direct == 2) & (feedback == 4) & (sum([train_edu, infra, culture]) >= 5):
            
            hh_survey_scores = 'Achieved the Standard'
            hh_survey_points = 100
         
        #if monitoring has 2 Yes answers, electronic and direct have 2 Yes answers each, feedback has 4 answers,
        # and there are at least 5 Yes answers from training/education + infrastructure + culture
        elif (monitoring == 2) & (electronic == 2) & (direct == 2) & (feedback == 4) & (sum([train_edu, infra, culture]) >= 5):
            
            hh_survey_scores = 'Considerable Achievement'
            hh_survey_points = 100  
         
        #if two domains in the some_count variable have all Yes answers
        elif some_count == 2:
            
            hh_survey_scores = 'Some Achievement'
            hh_survey_points = 0   
        
        #if 1 or fewer domains in the some_count variable have all Yes answers
        elif some_count <= 1:
            
            hh_survey_scores = 'Limited Achievement'
            hh_survey_points = 0    
        
        #otherwise
        else:
            
            hh_survey_scores = 'Not Applicable'
            hh_survey_points = -1
        
        #store hand hygiene points
        st.session_state.hh_survey_scores = hh_survey_scores
        st.session_state.hh_survey_points = hh_survey_points
        st.session_state['Hand Hygiene'] = hh_survey_points
        
        st.markdown('''----''') 
        
        #display points
        hh_points_col1, hh_points_col2 = st.columns(2)
        
        with hh_points_col1:
            
            st.write('Score')
            st.success(hh_survey_scores)
        
        with hh_points_col2:
            
            st.write('Points')
            
            #replace nan with N/A for revealing the points only*
            if hh_survey_points == -1:
                 st.success('N/A')
            else:
                st.success(hh_survey_points)

    st.markdown("[Return to Top - Hand Hygiene](#hand-hygiene)", unsafe_allow_html=True)
    
st.markdown('''---''')

st.header('CMS Measures')

with st.expander(''):
    
    st.write('''*Submitting -1 will indicate a missing or not applicable value.*''')

    ui_col1, ui_col2, ui_col3 = st.columns(3) 
    
    with ui_col1:
    
        hcomp1 = st.number_input('H-COMP-1', min_value=-1, key='H-COMP-1')

        hcomp2 = st.number_input('H-COMP-2', min_value=-1, key='H-COMP-2')

        hcomp3 = st.number_input('H-COMP-3', min_value=-1, key='H-COMP-3')

        hcomp5 = st.number_input('H-COMP-5', min_value=-1, key='H-COMP-5')

        hcomp6 = st.number_input('H-COMP-6', min_value=-1, key='H-COMP-6')

    with ui_col2:
        
        for_obj = st.number_input('Foreign Object Retained', min_value=-1, key='Foreign Object Retained')

        air_emb = st.number_input('Air Embolism', min_value=-1, key='Air Embolism')

        falls = st.number_input('Falls and Trauma', min_value=-1, key='Falls and Trauma')

        clabsi = st.number_input('CLABSI', min_value=-1, key='CLABSI')   
        
        cauti = st.number_input('CAUTI', min_value=-1, key='CAUTI')  

    with ui_col3:
        
        ssi = st.number_input('SSI', min_value=-1, key='SSI: Colon')

        mrsa = st.number_input('MRSA', min_value=-1, key='MRSA')

        cdiff = st.number_input('C. Diff.',min_value=-1, key='C. Diff.')

        psi4 = st.number_input('PSI 4', min_value=-1, key='PSI 4')

        psi90 = st.number_input('PSI 90', min_value = -1, key='PSI 90')

st.markdown('''---''')
    
if st.button('Calculate Your Points'):
    
    st.markdown('''---''')

    #%% check all pertinent Qs were answered
    if facility == '':
        st.error('Please input your facility first.')
        st.markdown("[Take Me to Facility Selection](#hospital-information)", unsafe_allow_html=True)
        st.stop()
        
    else: #run calculations
    
        points_bank = {'CPOE': st.session_state.CPOE,
                       'BCMA': st.session_state.BCMA,
                       'IPS': st.session_state.IPS,
                       'SP 1': st.session_state['SP 1'],
                       'SP 2': st.session_state['SP 2'],
                       'SP 9': st.session_state['SP 9'],
                       'Hand Hygiene': st.session_state['Hand Hygiene'],
                       'H-COMP-1': st.session_state['H-COMP-1'],
                       'H-COMP-2': st.session_state['H-COMP-2'],
                       'H-COMP-3': st.session_state['H-COMP-3'],
                       'H-COMP-5': st.session_state['H-COMP-5'],
                       'H-COMP-6': st.session_state['H-COMP-6'],
                       'Foreign Object Retained': st.session_state['Foreign Object Retained'],
                       'Air Embolism': st.session_state['Air Embolism'],
                       'Falls and Trauma': st.session_state['Falls and Trauma'],
                       'CLABSI': st.session_state['CLABSI'],
                       'CAUTI': st.session_state['CAUTI'],
                       'SSI: Colon': st.session_state['SSI: Colon'],
                       'MRSA': st.session_state['MRSA'],
                       'C. Diff.': st.session_state['C. Diff.'],
                       'PSI 4': st.session_state['PSI 4'],
                       'PSI 90': st.session_state['PSI 90']}

        #register submission timestamp
        calculation_timestamp = datetime.now().strftime('%m-%d-%Y %H:%M %p')
    
        #%% Final points Calculation
    
        #format points bank into a dataframe, reset the index, and relabel the columns to 'Measure' and 'Points'
        points_df = pd.DataFrame.from_dict(points_bank, orient='index').reset_index().rename(columns={'index':'Measure', 0:'Points'})
        
        #format the calculations_metrics into a dataframe 
        calculation_df = pd.DataFrame.from_dict(calculation_metrics)
        
        #merge in the points bank dataframe
        calculation_df = calculation_df.merge(points_df, on = 'Measure', how = 'left')
        #calculation_df['Points'] = calculation_df['Points'].fillna(-1)

        #-----------------------------------------------------------------#
        #OPPORTUNITY
        #The Opportunity points is the Coefficient of Variation (Standard Deviation/Mean)
        
        #Opportunity points = 1 + (Standard Deviation/Mean) 
        calculation_df['Opportunity Score'] = calculation_df['Standard Deviation']/calculation_df['Mean']
        calculation_df['Opportunity Score'] = calculation_df['Opportunity Score'] + 1
        
        #Opportunity points is on a continuous scale that is capped at three (3). 
        calculation_df.loc[calculation_df['Opportunity Score'] > 3.0, 'Opportunity Score'] = 3.0

        #-----------------------------------------------------------------#
        #EVIDENCE
        #pre-determined; see methodology pg. 15
       
        #-----------------------------------------------------------------#
        #IMPACT
        #pre-determined; see methodology pg. 15
        
        #-----------------------------------------------------------------#
        #WEIGHTING INDIVIDUAL MEASURES
        #standard weight = Evidence + (Opportunity x Impact)
        
        calculation_df['Standard Measure Weight'] = calculation_df['Opportunity Score']*calculation_df['Impact Score']
        calculation_df['Standard Measure Weight'] = calculation_df['Standard Measure Weight'] + calculation_df['Evidence Score']
        
        #make into a percentage 
        calculation_df['Standard Measure Weight'] = calculation_df['Standard Measure Weight']/100
        
        #-----------------------------------------------------------------#
        #Zpoints
        #Z-points are used to standardize data from measures with different performance scales and allow for comparisons.
    
        #PROCESS/STRUCTURAL MEASURES--------------------------------------#
        # Hospital points – Mean) / Standard Deviation
        structural = calculation_df.loc[calculation_df['Domain'] == 'Process/Structural Measures']
        structural['Z-Score'] = (structural['Points'] - structural['Mean']) / structural['Standard Deviation']
        
        #Leapfrog caps negative Z-points at -5.00. 
        structural.loc[structural['Z-Score'] < -5.0, 'Z-Score'] = -5.0
        
        #list of structural measures
        structural_measures = structural['Measure'].tolist()
        
        #OUTCOME MEASURES-------------------------------------------------#
        #(Mean – Hospital points) / Standard Deviation
        outcome = calculation_df.loc[calculation_df['Domain'] == 'Outcome Measures']
        outcome['Z-Score'] = outcome['Mean'] - outcome['Points'] / outcome['Standard Deviation']
        
        #Leapfrog caps negative Z-points at -5.00. 
        outcome.loc[outcome['Z-Score'] < -5.0, 'Z-Score'] = -5.0
      
        #list of outcome measures
        outcome_measures = outcome['Measure'].tolist()

        #if there are no available measures for either domain, throw an error
        structural_points = structural.loc[structural['Points'] > -1]
        outcome_points = outcome.loc[outcome['Points'] > -1]
        if len(structural_points) == 0 or len(outcome_points) == 0:
            st.error('At least one structural and one outcome measure is needed. Calculate the individual measures prior to calculating final points. See chart below for more information.')
            #Make domain + measure table
            domain_df = calculation_df[['Domain', 'Measure']]
            domain_df['Domain'] = domain_df['Domain'].str.replace('Measures', '').str.replace('Process/','')
            st.write(domain_df)
            st.stop()
            
        #DEALING WITH MISSING DATA----------------------------------------#
        #If a hospital is missing a measure points for any measure, the standard weight of that measure is redistributed 
        #to the other measures in the same measure domain. The new weight for each measure within the domain is calculated 
        #by re-apportioning the standard weight assigned to the measure with the missing points to other measures within 
        #the same domain.
        
        #For example, if a hospital is missing a measure points for ICU Physician Staffing because the hospital does not 
        #operate an adult or pediatric medical and/or surgical ICU, the standard weight of 7.3% will be re-apportioned to 
        #the remaining 12 measures within the process/structural measure domain.
        
        #To calculate the new weight of each of the remaining 12 measures in the process/structural measure domain,
        #hospitals can use the formula below or use the Leapfrog Hospital Safety Grade Calculator©, which can be found on 
        #the Safety Grade Review Website. Note that each domain contributes to 50% of the overall letter grade.
        
        #[Standard measure weight / (sum of standard weights for the remaining 12 measures in the process/structural 
        #measure domain)]*50% = updated measure weight
        
        ##Hospitals will be submitting surveys so there should not be any inputed values to move forward or add to calculator

        #Handle missing data via the user inputs (as opposed to prior knowledge of a facility's capabilities)
        
        ## Re-Distribution of Weights Function

        def redistribute(df):
            """Find the missing measures and re-distributes their weights to the remaining measures."""
            #missing measures
            missing_measures = df.loc[df['Points'] == -1]['Measure'].tolist()
            
            for measure in missing_measures:

                #get missing measure's standard measure weight
                std_mea_wght = df.loc[df['Measure'] == measure]['Standard Measure Weight']
                
                #divide it by the sum of the remaining standard weights and multiply it by .5
                remaining_weights = df.loc[df['Measure'] != measure]['Standard Measure Weight'].sum()
                
                updated_weight = (std_mea_wght/remaining_weights)*.5
 
                #drop out the measure to avoid it receiving a re-distributed weight from the next iteration of the loop
                df = df.loc[df['Measure'] != measure]
                
                # to run the length of the index in the proceeding loop
                df = df.reset_index().drop('index', axis = 1)
   
                #the standard weight of that measure is redistributed to the other measures in the same measure domain
                for i in range(df.index.min(), df.index.max()):

                    # make current weight variable
                    current_weight = df.iloc[i]['Standard Measure Weight']

                    # set standard measure weight as current weight + updated weight
                    df.iloc[i].at['Standard Measure Weight'] = current_weight + updated_weight

            return df

        #structural re-distribution
        structural_redist = redistribute(structural)
        
        #outcome re-distrubution
        outcome_redist = redistribute(outcome)
            
        #-----------------------------------------------------------------#
        #NUMERICAL SAFETY points
        
        #PROCESS/STRUCTURAL
        #To calculate a hospital’s numerical safety points, multiply the Z-points of each process/structural measure 
        #by the standard weight assigned to that measure to get the weighted process/structural measure points. 
        structural_redist['Weighted Measure Score'] = structural_redist['Z-Score'] * structural_redist['Standard Measure Weight']

        #If a hospital is missing any outcome measure points, see Dealing with Missing Data to determine the updated 
        #measure weight.
        
        #Then, sum all weighted process/structural measure points to get the hospital’s overall weighted 
        #process/structural measures points.
        process_structural_measures_points = structural_redist['Weighted Measure Score'].sum()
        
        #OUTCOME
        #Multiply the Z-points of each outcome measure by the standard weight assigned to that measure to get the 
        #weighted outcome measure points. 
        outcome_redist['Weighted Measure Score'] = outcome_redist['Z-Score'] * outcome_redist['Standard Measure Weight']

        #If a hospital is missing any outcome measure points, see Dealing with Missing Data to determine the updated 
        #measure weight.
        
        #Then, sum all weighted outcome measure points. This is the hospital’s overall weighted outcome measures points.
        outcome_measures_points = outcome_redist['Weighted Measure Score'].sum()

        #-----------------------------------------------------------------#
        #EXTREME VALUES
        #For hospitals that have an “extreme” value for a particular measure (i.e., a value that exceeds the 99th percentile) 
        #Leapfrog “trims” the reported value to the 99th percentile. For example, a rate of 0.50 per 1,000 patient discharges for 
        #Foreign Object Retained after Surgery is “trimmed” to 0.359 (e.g., the 99th percentile). Only “trimmed” rates are displayed 
        #on the Leapfrog Hospital Safety Grade website. The following table includes the “trim” values for the spring 2021 Leapfrog Hospital Safety Grade.
    
        for i in range(outcome_redist.index.min(), len(outcome_redist.index)):
            if outcome_redist.loc[i,'Weighted Measure Score'] > outcome_redist.loc[i,'99th Percentile']:
                outcome_redist.loc[i,'Weighted Measure Score'] = outcome_redist.loc[i,'99th Percentile']
        
        #-----------------------------------------------------------------#
        #OVERALL SAFETY points
        #Add the overall weighted process/structural measure points and the overall weighted outcome measures points.
        overall_safety_points = round(process_structural_measures_points + outcome_measures_points, 3)
        
        #Add 3.0 to normalize points to a positive distribution. This final numerical points is typically between 1.0 and 4.0.
        final_points = round(overall_safety_points + 3.0, 2)
        
        #-----------------------------------------------------------------#
        #bring the two dataframes back together, if needed
        final_calculation_df = pd.concat([structural_redist, outcome_redist])

        #-----------------------------------------------------------------#
        #OVERALL SAFTY GRADE
    
        grade_cutoffs = pd.DataFrame.from_dict(grade_cutoffs)

        grade_a = grade_cutoffs.loc[grade_cutoffs['grade'] == 'A']['cut-off'][0]
        grade_b = grade_cutoffs.loc[grade_cutoffs['grade'] == 'B']['cut-off'][1]
        grade_c = grade_cutoffs.loc[grade_cutoffs['grade'] == 'C']['cut-off'][2]
        grade_d = grade_cutoffs.loc[grade_cutoffs['grade'] == 'D']['cut-off'][3]
        grade_f = grade_cutoffs.loc[grade_cutoffs['grade'] == 'F']['cut-off'][4]

        if final_points >= grade_a:
            final_grade = 'A'
            
        elif (final_points < grade_a) & (final_points >= grade_b):
            final_grade = 'B'
            
        elif (final_points < grade_b) & (final_points >= grade_c):
            final_grade = 'C'
            
        elif (final_points < grade_c) & (final_points >= grade_d):
            final_grade = 'D'
            
        elif final_points < grade_f:
            final_grade = 'F'
            
        else:
            final_grade = '?'
        
        fscol1, fscol2 = st.columns(2)
        
        with fscol1:
            st.header('''Your Estimated Hospital Safety Grade''')
           
        with fscol2:
            st.header('''Your Estimated Normalized points''')
         
        f1col1, f1col2, f1col3, f1col4 = st.columns(4)
    
        with f1col1:
            st.write('')
        
        with f1col2:
            st.markdown(''' # {}'''.format(final_grade))
        
        with f1col3:
            st.write('')
        
        with f1col4:
            st.markdown(''' # {}'''.format(final_points))
     
        st.markdown('''----''')
        
        #convert -1 to - for display purposes
        display_df = calculation_df[['Measure', 'Points']]
        #set Measure as the index for indexing against
        display_df = display_df.set_index('Measure')
        display_df['Points'] = display_df['Points'].replace(-1, '-')

        #%% section points
        st.header('Your Structural Points')
        
        fcol1, fcol2, fcol3, fcol4 = st.columns(4)
        
        with fcol1:
            sp1_points = st.metric('SP 1', display_df.loc['SP 1']['Points'])
            sp2_points = st.metric('SP 2', display_df.loc['SP 2']['Points'])
            sp9_points = st.metric('SP 9', display_df.loc['SP 9']['Points'])
            
        with fcol2:
            cpoe_points = st.metric('CPOE', display_df.loc['CPOE']['Points'])
            bcma_points = st.metric('BCMA', display_df.loc['BCMA']['Points'])
            ips_points = st.metric('IPS', display_df.loc['IPS']['Points'])
            
        with fcol3:
            hh_points = st.metric('Hand Hygn', display_df.loc['Hand Hygiene']['Points'])
            st.metric('H-COMP-1', display_df.loc['H-COMP-1']['Points']) 
            st.metric('H-COMP-2', display_df.loc['H-COMP-2']['Points'])
            
        with fcol4:
            st.metric('H-COMP-3', display_df.loc['H-COMP-3']['Points'])
            st.metric('H-COMP-5', display_df.loc['H-COMP-5']['Points'])
            st.metric('H-COMP-6', display_df.loc['H-COMP-6']['Points'])
            
        st.header('Your Outcome Points')
        
        iscol1, iscol2, iscol3, iscol4 = st.columns(4)
        
        with iscol1:
            st.metric('Air Embolism', display_df.loc['Air Embolism']['Points'])
            st.metric('CAUTI', display_df.loc['CAUTI']['Points'])
            st.metric('For. Obj. Ret.', display_df.loc['Foreign Object Retained']['Points'])
             
        with iscol2:
            st.metric('Falls/Trauma', display_df.loc['Falls and Trauma']['Points'])
            st.metric('SSI', display_df.loc['SSI: Colon']['Points'])
            st.metric('C. Diff.', display_df.loc['C. Diff.']['Points'])   
            
        with iscol3:
            st.metric('CLABSI', display_df.loc['CLABSI']['Points'])
            st.metric('MRSA', display_df.loc['MRSA']['Points'])
    
        with iscol4:
            st.metric('PSI 4', display_df.loc['PSI 4']['Points'])
            st.metric('PSI 90', display_df.loc['PSI 90']['Points'])
                 
st.markdown('''----''')

#initialize for handling prior to button click per section
if 'CPOE' not in st.session_state:
    st.session_state.CPOE = 15

if 'BCMA' not in st.session_state:
    st.session_state.BCMA = 25

if 'IPS' not in st.session_state:
    st.session_state.IPS = -1

if 'SP 1' not in st.session_state:
    st.session_state['SP 1'] = 0

if 'SP 2' not in st.session_state:
    st.session_state['SP 2'] = 0

if 'SP 9' not in st.session_state:
    st.session_state['SP 9'] = 0.0

if 'Hand Hygiene' not in st.session_state:
    st.session_state['Hand Hygiene'] = 0
    

section_scores = {'Section' : ['Facility',
                               'CPOE',
                               'BCMA',
                               'IPS',
                               'SP 1',
                               'SP 2',
                               'SP 9',
                               'Hand Hygiene',
                               'H-COMP-1',
                               'H-COMP-2',
                               'H-COMP-3',
                               'H-COMP-5',
                               'H-COMP-6',
                               'Foreign Object Retained',
                               'Air Embolism',
                               'Falls and Trauma',
                               'CLABSI',
                               'CAUTI',
                               'SSI: Colon',
                               'MRSA',
                               'C. Diff.',
                               'PSI 4',
                               'PSI 90'],
                  'Result' : [st.session_state.facility,
                              st.session_state.CPOE,
                              st.session_state.BCMA,
                              st.session_state.IPS,
                              st.session_state['SP 1'],
                              st.session_state['SP 2'],
                              st.session_state['SP 9'],
                              st.session_state['Hand Hygiene'],
                              st.session_state['H-COMP-1'],
                              st.session_state['H-COMP-2'],
                              st.session_state['H-COMP-3'],
                              st.session_state['H-COMP-5'],
                              st.session_state['H-COMP-6'],
                              st.session_state['Foreign Object Retained'],
                              st.session_state['Air Embolism'],
                              st.session_state['Falls and Trauma'],
                              st.session_state['CLABSI'],
                              st.session_state['CAUTI'],
                              st.session_state['SSI: Colon'],
                              st.session_state['MRSA'],
                              st.session_state['C. Diff.'],
                              st.session_state['PSI 4'],
                              st.session_state['PSI 90']
                              ]}

#%% Create the sidebar points bank
st.sidebar.header('Points Bank')
section_scores_df = pd.DataFrame.from_dict(section_scores)
section_scores_df['Result'] = section_scores_df['Result'].replace(-1.0, '')
for i in range(0, len(section_scores_df)):
    st.sidebar.write(section_scores_df.loc[i, 'Section'] + ': ' + str(section_scores_df.loc[i, 'Result']))


st.markdown('''
     ### Additional Resources 
     **Calculating Z-points, Weight, & Weighting Individual Measures.** Please refer to the 
     [Scoring Methodology](https://www.hospitalsafetygrade.org/media/file/Safety-Grade-Methodology-Spring-20222.pdf) 
     for more details.  
     ''')
     





