# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 16:32:18 2021

@author: reb00762
"""

from numpy import nan

def leapfrog_variables():

    '''
    Returns
    -------
    grade_cutoffs : dict
        Leapfrog grade letters based on final score.
    facilities : list
        List of inpatient facilities for use in the dropdown selector.
    calculation_metrics : dict
        Metrics provided by Leapfrog for use in final calculations.
    '''

    #list of facilities to use in the facility dropdown selector

    facilities = ['',
                  'Alfa',
                  'Bravo', 
                  'Charlie', 
                  'Delta', 
                  'Echo', 
                  'Foxtrot', 
                  'Golf', 
                  'Hotel', 
                  'India', 
                  'Juliett', 
                  'Kilo', 
                  'Lima', 
                  'Mike', 
                  'November', 
                  'Oscar', 
                  'Papa', 
                  'Quebec', 
                  'Romeo', 
                  'Sierra', 
                  'Tango', 
                  'Uniform', 
                  'Victor', 
                  'Whiskey', 
                  'X-ray', 
                  'Yankee', 
                  'Zulu']

    #grade cutoffs in dict format
    grade_cutoffs = {'grade': {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'F'}, 
                     'cut-off': {0: 3.159, 1: 2.972, 2: 2.506, 3: 2.04, 4: 2.039}}

    # standard deviation, weights, evidence, opportunity, and impact score values in dict format
    calculation_metrics = {'Domain': {0: 'Process/Structural Measures', 1: 'Process/Structural Measures', 2: 'Process/Structural Measures', 3: 'Process/Structural Measures', 4: 'Process/Structural Measures', 5: 'Process/Structural Measures', 6: 'Process/Structural Measures', 7: 'Process/Structural Measures', 8: 'Process/Structural Measures', 9: 'Process/Structural Measures', 10: 'Process/Structural Measures', 11: 'Process/Structural Measures', 12: 'Outcome Measures', 13: 'Outcome Measures', 14: 'Outcome Measures', 15: 'Outcome Measures', 16: 'Outcome Measures', 17: 'Outcome Measures', 18: 'Outcome Measures', 19: 'Outcome Measures', 20: 'Outcome Measures', 21: 'Outcome Measures'}, 
                           'Measure': {0: 'CPOE', 1: 'BCMA', 2: 'IPS', 3: 'SP 1', 4: 'SP 2', 5: 'SP 9', 6: 'Hand Hygiene', 7: 'H-COMP-1', 8: 'H-COMP-2', 9: 'H-COMP-3', 10: 'H-COMP-5', 11: 'H-COMP-6', 12: 'Foreign Object Retained', 13: 'Air Embolism', 14: 'Falls and Trauma', 15: 'CLABSI', 16: 'CAUTI', 17: 'SSI: Colon', 18: 'MRSA', 19: 'C. Diff.', 20: 'PSI 4', 21: 'PSI 90'}, 
                           'Evidence Score': {0: 2, 1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 2, 15: 2, 16: 2, 17: 2, 18: 2, 19: 2, 20: 1, 21: 1}, 
                           'Opportunity Score': {0: 1.262402987649783, 1: 1.2589744843538442, 2: 1.68915576314035, 3: 1.0632379428633674, 4: 1.1115209778708008, 5: 1.0720276842832799, 6: 1.4409561619373477, 7: 1.0244734735813734, 8: 1.0232391567627868, 9: 1.0426797078353034, 10: 1.046232823391834, 11: 1.0384013523297628, 12: 3.0, 13: 3.0, 14: 1.9056098441406282, 15: 1.8306986709416622, 16: 1.758887568299321, 17: 1.8131764796014485, 18: 1.7777935641749558, 19: 1.6758827709873023, 20: 1.1145392223087562, 21: 1.1922918579353619}, 
                           'Impact Score': {0: 3, 1: 3, 2: 3, 3: 2, 4: 2, 5: 3, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 2, 13: 1, 14: 3, 15: 3, 16: 3, 17: 2, 18: 3, 19: 3, 20: 2, 21: 2}, 
                           'Standard Measure Weight': {0: 0.05854029601935698, 1: 0.05843610659286414, 2: 0.07149114288720028, 3: 0.03162604290581276, 4: 0.032602186561789384, 5: 0.04264786806179343, 6: 0.04938275351411716, 7: 0.030841081789711344, 8: 0.030816804641790683, 9: 0.031210296747671416, 10: 0.03128211664360337, 11: 0.031123303634289043, 12: 0.04291956016034748, 13: 0.024525462948769988, 14: 0.04731452312076706, 15: 0.045936805239619904, 16: 0.04461610905982864, 17: 0.03449751618373986, 18: 0.04496375749712746, 19: 0.04308878585469399, 20: 0.01979879310196829, 21: 0.15233868683313734}, 
                           'Mean': {0: 85.77376033057851, 1: 83.25189524465885, 2: 62.82208588957055, 3: 116.8508817635263, 4: 116.4879759519038, 5: 98.1641683366732, 6: 74.36372745490982, 7: 91.10162461113032, 8: 90.99758036640166, 9: 84.37953681299689, 10: 77.66297960594538, 11: 86.51227099896302, 12: 0.016430392832529304, 13: 0.0004028925619834712, 14: 0.42414600550964243, 15: 0.8096514203177656, 16: 0.7521154513888892, 17: 0.80327108433735, 18: 0.8403254182406917, 19: 0.5381886662059434, 20: 159.66751322751315, 21: 1.0024345730027542}, 'Standard Deviation': {0: 22.507290972700247, 1: 21.560116642465783, 2: 43.294202543295604, 3: 7.389409384495966, 4: 12.990852988346655, 5: 7.070537724884645, 6: 32.791143845872, 7: 2.2295732031407054, 8: 2.114707035169091, 9: 3.6012939784569364, 10: 3.5905788202052804, 11: 3.322188199479109, 12: 0.05472132855173372, 13: 0.0037655460606468923, 14: 0.3841107979424573, 15: 0.6725763587839969, 16: 0.5707710659848603, 17: 0.6532011525270844, 18: 0.6535997021202381, 19: 0.3637524470292333, 20: 18.28819279305242, 21: 0.1927600065013407}, 
                           '99th Percentile': {0: nan, 1: nan, 2: nan, 3: nan, 4: nan, 5: nan, 6: nan, 7: nan, 8: nan, 9: nan, 10: nan, 11: nan, 12: 0.359, 13: 0.037, 14: 1.727, 15: 2.716, 16: 2.491, 17: 2.817, 18: 2.927, 19: 1.77, 20: 215.05, 21: nan}}
    
    return (grade_cutoffs, facilities, calculation_metrics)